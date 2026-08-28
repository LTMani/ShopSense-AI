import json
from typing import Dict, Any, Optional, List
from app.models.product import Product
from app.models.conversation import Conversation, ConversationMessage
from app.repositories.conversation_repository import ConversationRepository, ConversationMessageRepository
from app.repositories.product_repository import ProductRepository
from app.ai.gateway import get_ai_gateway
from app.ai.nlp.entity_extractor import EntityExtractor
from app.ai.copilot.ranking_engine import CopilotRankingEngine
from app.ai.copilot.explanation_generator import ExplanationGenerator
from app.extensions import db


class CopilotService:
    """AI Shopping Copilot managing multi-turn conversational requirements, adaptive ranking, and explanations."""

    def __init__(self):
        self.conv_repo = ConversationRepository()
        self.msg_repo = ConversationMessageRepository()
        self.product_repo = ProductRepository()

    def process_message(
        self,
        user_id: int,
        conversation_id: Optional[int],
        user_message: str
    ) -> Dict[str, Any]:
        # 1. Retrieve or Create Conversation Session
        if conversation_id:
            conversation = self.conv_repo.get_by_id(conversation_id)
        else:
            conversation = self.conv_repo.create(
                user_id=user_id,
                copilot_type='customer_shopping',
                session_title=user_message[:50] + ('...' if len(user_message) > 50 else '')
            )

        context = conversation.get_context_dict()

        # 2. Extract entities and constraints from current message + prior context
        new_entities = EntityExtractor.extract_entities(user_message)
        
        # Merge context statefully
        if new_entities.get('budget'):
            context['budget'] = new_entities['budget']
        if new_entities.get('category'):
            context['category'] = new_entities['category']
        if new_entities.get('brand'):
            context['brand'] = new_entities['brand']
        
        priorities = context.get('priorities', [])
        for u in new_entities.get('usage', []):
            if u not in priorities:
                priorities.append(u)
        context['priorities'] = priorities

        conversation.set_context_dict(context)

        # 3. Save User Message
        self.msg_repo.create(
            conversation_id=conversation.id,
            sender='user',
            content=user_message
        )

        # 4. Search Candidate Products from Internal Database
        budget = context.get('budget')
        category_name = context.get('category')
        query_text = user_message if not category_name else category_name

        candidates = Product.query.filter_by(is_active=True).all()
        if category_name:
            candidates = [p for p in candidates if p.category and category_name.lower() in p.category.name.lower()] or candidates

        # 5. Adaptive Ranking and Scoring
        ranked = CopilotRankingEngine.rank_candidates(
            products=candidates,
            budget=budget,
            priorities=priorities,
            primary_usage=priorities[0] if priorities else 'general'
        )

        top_matches = ranked[:5]
        recommended_ids = [r['product'].id for r in top_matches]

        # 6. Generate AI Conversational Response & Explanations
        ai_gateway = get_ai_gateway()
        top_product = top_matches[0]['product'] if top_matches else None
        
        explanation = ""
        if top_product:
            explanation = ExplanationGenerator.generate_explanation(
                product=top_product,
                match_score=top_matches[0]['match_score'],
                reasons=top_matches[0]['reasons'],
                user_budget=budget,
                priorities=priorities
            )

        system_prompt = (
            "You are ShopSense AI Copilot, a friendly, knowledgeable, and precise shopping assistant. "
            "Help the user find the best products from the catalog. Highlight why the best match fits their budget and needs."
        )
        ai_resp = ai_gateway.generate(user_message, system_prompt=system_prompt)
        assistant_content = ai_resp['content']

        # 7. Save Assistant Message
        assistant_msg = self.msg_repo.create(
            conversation_id=conversation.id,
            sender='assistant',
            content=assistant_content,
            extracted_requirements=json.dumps(context),
            recommended_product_ids=json.dumps(recommended_ids),
            explanation_text=explanation,
            confidence_score=0.92,
            latency_ms=ai_resp.get('latency_ms', 0)
        )

        db.session.commit()

        return {
            'conversation_id': conversation.id,
            'message': assistant_msg.to_dict(),
            'extracted_context': context,
            'recommended_products': [
                {
                    'product': r['product'].to_dict(),
                    'match_score': r['match_score'],
                    'badge': r.get('badge'),
                    'reasons': r['reasons']
                } for r in top_matches
            ],
            'explanation': explanation
        }
