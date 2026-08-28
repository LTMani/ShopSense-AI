# ShopSense AI Services Generator
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'app' / 'services'
BASE.mkdir(parents=True, exist_ok=True)

# 1. auth_service.py
(BASE / 'auth_service.py').write_text('''from datetime import datetime, timezone, timedelta
import secrets
from typing import Dict, Any, Optional
from app.models.user import User, Role, UserSession
from app.models.profile import CustomerProfile, SellerProfile
from app.models.cart import Cart
from app.models.wishlist import Wishlist
from app.repositories.user_repository import UserRepository, RoleRepository, CustomerProfileRepository, SellerProfileRepository, SessionRepository
from app.extensions import db


class AuthService:
    """Handles secure authentication, registration, session management, and RBAC."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.role_repo = RoleRepository()
        self.customer_profile_repo = CustomerProfileRepository()
        self.seller_profile_repo = SellerProfileRepository()
        self.session_repo = SessionRepository()

    def register_customer(self, email: str, password: str, first_name: str, last_name: str, phone: Optional[str] = None) -> Dict[str, Any]:
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("An account with this email address already exists.")

        role = self.role_repo.get_by_name('customer')
        if not role:
            role = self.role_repo.create(name='customer', display_name='Customer', description='Standard retail customer')

        user = User(
            email=email.strip().lower(),
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            phone=phone.strip() if phone else None,
            role_id=role.id,
            is_active=True,
            is_verified=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        # Initialize Customer Profile, Cart, and Wishlist
        profile = CustomerProfile(user_id=user.id)
        cart = Cart(user_id=user.id)
        wishlist = Wishlist(user_id=user.id, name='My Wishlist')
        db.session.add_all([profile, cart, wishlist])
        db.session.commit()

        return user.to_dict(include_profile=True)

    def register_seller(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        business_name: str,
        store_slug: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("An account with this email address already exists.")

        role = self.role_repo.get_by_name('seller')
        if not role:
            role = self.role_repo.create(name='seller', display_name='Seller', description='Merchant/Seller partner')

        slug = store_slug or business_name.lower().replace(' ', '-').replace('&', 'and')
        # Ensure unique slug
        existing_seller = self.seller_profile_repo.get_by_slug(slug)
        if existing_seller:
            slug = f"{slug}-{secrets.token_hex(2)}"

        user = User(
            email=email.strip().lower(),
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            phone=phone.strip() if phone else None,
            role_id=role.id,
            is_active=True,
            is_verified=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        seller_profile = SellerProfile(
            user_id=user.id,
            business_name=business_name.strip(),
            store_slug=slug,
            business_phone=phone,
            business_email=email
        )
        db.session.add(seller_profile)
        db.session.commit()

        return user.to_dict(include_profile=True)

    def authenticate_user(self, email: str, password: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Optional[User]:
        user = self.user_repo.get_by_email(email)
        if not user or not user.is_active or not user.check_password(password):
            return None

        self.user_repo.update_last_login(user)
        return user

    def create_user_session(self, user_id: int, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> str:
        token = secrets.token_urlsafe(48)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        self.session_repo.create(
            user_id=user_id,
            session_token=token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
            is_active=True
        )
        return token
''', encoding='utf-8')

# 2. catalog_service.py
(BASE / 'catalog_service.py').write_text('''from typing import Dict, Any, Optional, List
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository


class CatalogService:
    """Manages catalog browsing, category hierarchy, product specifications, and stock status."""

    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_repo = CategoryRepository()

    def get_categories(self, include_children: bool = True) -> List[Dict[str, Any]]:
        categories = self.category_repo.get_root_categories(active_only=True)
        return [c.to_dict(include_children=include_children) for c in categories]

    def get_product_by_id(self, product_id: int, detailed: bool = True) -> Optional[Dict[str, Any]]:
        product = self.product_repo.get_by_id(product_id)
        if not product or not product.is_active:
            return None
        self.product_repo.increment_view_count(product_id)
        return product.to_dict(detailed=detailed)

    def get_product_by_slug(self, slug: str, detailed: bool = True) -> Optional[Dict[str, Any]]:
        product = self.product_repo.get_by_slug(slug)
        if not product or not product.is_active:
            return None
        self.product_repo.increment_view_count(product.id)
        return product.to_dict(detailed=detailed)

    def get_featured_products(self, limit: int = 8) -> List[Dict[str, Any]]:
        products = self.product_repo.get_featured(limit=limit)
        return [p.to_dict() for p in products]

    def get_related_products(self, product_id: int, limit: int = 4) -> List[Dict[str, Any]]:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return []
        related = Product.query.filter(
            Product.category_id == product.category_id,
            Product.id != product.id,
            Product.is_active.is_(True)
        ).order_by(Product.average_rating.desc()).limit(limit).all()
        return [p.to_dict() for p in related]
''', encoding='utf-8')

# 3. search_service.py
(BASE / 'search_service.py').write_text('''from typing import Dict, Any, Optional, List
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.ai.nlp.entity_extractor import EntityExtractor
from app.ai.nlp.vector_similarity import VectorSimilarityEngine


class SearchService:
    """Hybrid semantic search engine combining structured metadata filtering with TF-IDF vector similarity."""

    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_repo = CategoryRepository()

    def search(
        self,
        query: str,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        brand: Optional[str] = None,
        min_rating: Optional[float] = None,
        sort_by: str = 'relevance',
        page: int = 1,
        per_page: int = 12
    ) -> Dict[str, Any]:
        # 1. NLP Entity Extraction from query
        extracted = EntityExtractor.extract_entities(query) if query else {}
        
        # If user didn't specify explicit max_price but query contains "under ₹60,000", apply extracted budget
        if max_price is None and extracted.get('budget'):
            max_price = extracted['budget']

        if category_id is None and extracted.get('category'):
            cat = self.category_repo.find_one_by(name=extracted['category'])
            if cat:
                category_id = cat.id

        if brand is None and extracted.get('brand'):
            brand = extracted['brand']

        # 2. Database candidate search
        search_result = self.product_repo.search_products(
            query_text=query,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            brand=brand,
            min_rating=min_rating,
            sort_by=sort_by,
            page=page,
            per_page=per_page
        )

        # 3. Semantic Re-ranking if query is natural language and sort is relevance
        items = search_result['items']
        if query and len(items) > 1 and sort_by == 'relevance':
            doc_tuples = [
                (p.id, f"{p.title} {p.brand} {p.short_description} {p.target_usage or ''} {' '.join(p.get_key_features_list())}")
                for p in items
            ]
            ranked_scores = dict(VectorSimilarityEngine.rank_documents(query, doc_tuples))
            items.sort(key=lambda p: ranked_scores.get(p.id, 0.0), reverse=True)

        return {
            'products': [p.to_dict() for p in items],
            'total': search_result['total'],
            'page': search_result['page'],
            'pages': search_result['pages'],
            'has_next': search_result['has_next'],
            'has_prev': search_result['has_prev'],
            'extracted_filters': extracted
        }
''', encoding='utf-8')

# 4. copilot_service.py
(BASE / 'copilot_service.py').write_text('''import json
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
''', encoding='utf-8')

# 5. recommendation_service.py
(BASE / 'recommendation_service.py').write_text('''from typing import Dict, Any, List, Optional
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.ai.copilot.ranking_engine import CopilotRankingEngine


class RecommendationService:
    """Personalized and explainable recommendation engine."""

    def __init__(self):
        self.product_repo = ProductRepository()

    def get_personalized_recommendations(self, user_id: Optional[int] = None, limit: int = 8) -> List[Dict[str, Any]]:
        # Retrieve featured and top-rated catalog items
        products = Product.query.filter_by(is_active=True).order_by(Product.average_rating.desc(), Product.purchases_count.desc()).limit(limit).all()
        return [
            {
                'product': p.to_dict(),
                'recommendation_type': 'Trending & Top Rated',
                'explanation': f'Highly rated by customers ({p.average_rating}★) with proven reliability.'
            } for p in products
        ]

    def get_smart_alternatives(self, product_id: int, limit: int = 4) -> Dict[str, List[Dict[str, Any]]]:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return {'budget_alternatives': [], 'premium_upgrades': []}

        category_products = Product.query.filter(
            Product.category_id == product.category_id,
            Product.id != product.id,
            Product.is_active.is_(True)
        ).all()

        budget_alts = [
            {
                'product': p.to_dict(),
                'savings_amount': round(product.current_price - p.current_price, 2),
                'explanation': f'Save ₹{product.current_price - p.current_price:,.0f} with comparable core functionality.'
            }
            for p in category_products if p.current_price < product.current_price
        ]
        budget_alts.sort(key=lambda x: x['savings_amount'], reverse=True)

        premium_upgrades = [
            {
                'product': p.to_dict(),
                'price_diff': round(p.current_price - product.current_price, 2),
                'explanation': f'Upgrade for enhanced specifications and higher performance tier (+₹{p.current_price - product.current_price:,.0f}).'
            }
            for p in category_products if p.current_price > product.current_price
        ]
        premium_upgrades.sort(key=lambda x: x['price_diff'])

        return {
            'budget_alternatives': budget_alts[:limit],
            'premium_upgrades': premium_upgrades[:limit]
        }
''', encoding='utf-8')

# 6. comparison_service.py
(BASE / 'comparison_service.py').write_text('''from typing import Dict, Any, List
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.review_repository import ReviewRepository
from app.ai.gateway import get_ai_gateway


class ComparisonService:
    """Side-by-side product comparison engine with spec matrices, aspect sentiment delta, and AI verdicts."""

    def __init__(self):
        self.product_repo = ProductRepository()
        self.review_repo = ReviewRepository()

    def compare_products(self, product_ids: List[int]) -> Dict[str, Any]:
        if not product_ids:
            return {'products': [], 'attributes_matrix': {}, 'aspects_matrix': {}, 'verdict': ''}

        products = [self.product_repo.get_by_id(pid) for pid in product_ids[:4]]
        products = [p for p in products if p and p.is_active]

        if not products:
            return {'products': [], 'attributes_matrix': {}, 'aspects_matrix': {}, 'verdict': ''}

        # 1. Build Attribute Alignment Matrix
        all_attr_names = set()
        product_attr_maps = {}
        for p in products:
            attr_map = {a.name: f"{a.value} {a.unit or ''}".strip() for a in p.attributes.all()}
            product_attr_maps[p.id] = attr_map
            all_attr_names.update(attr_map.keys())

        attributes_matrix = {}
        for name in sorted(all_attr_names):
            attributes_matrix[name] = {p.id: product_attr_maps[p.id].get(name, '—') for p in products}

        # 2. Aspect Sentiment Matrix
        aspects_matrix = {}
        all_aspects = ['battery', 'performance', 'build_quality', 'sound', 'comfort', 'display', 'value']
        for asp in all_aspects:
            aspects_matrix[asp] = {p.id: p.get_aspect_sentiment_dict().get(asp, 75) for p in products}

        # 3. AI Comparison Verdict
        verdict = self._generate_comparison_verdict(products)

        return {
            'products': [p.to_dict(detailed=True) for p in products],
            'attributes_matrix': attributes_matrix,
            'aspects_matrix': aspects_matrix,
            'verdict': verdict
        }

    def _generate_comparison_verdict(self, products: List[Product]) -> str:
        if len(products) < 2:
            return "Add at least two products to generate a comprehensive comparison verdict."

        p1, p2 = products[0], products[1]
        verdict_parts = []

        if p1.current_price < p2.current_price:
            verdict_parts.append(f"**{p1.title}** is more budget-friendly (saves ₹{p2.current_price - p1.current_price:,.0f}).")
        else:
            verdict_parts.append(f"**{p2.title}** is more budget-friendly (saves ₹{p1.current_price - p2.current_price:,.0f}).")

        if p1.average_rating > p2.average_rating:
            verdict_parts.append(f"**{p1.title}** holds a higher verified customer satisfaction rating ({p1.average_rating}★ vs {p2.average_rating}★).")
        elif p2.average_rating > p1.average_rating:
            verdict_parts.append(f"**{p2.title}** holds a higher verified customer satisfaction rating ({p2.average_rating}★ vs {p1.average_rating}★).")

        return " ".join(verdict_parts)
''', encoding='utf-8')

# 7. review_intelligence_service.py
(BASE / 'review_intelligence_service.py').write_text('''import json
from typing import Dict, Any, List
from app.models.review import Review, ReviewAspectRating
from app.repositories.review_repository import ReviewRepository
from app.repositories.product_repository import ProductRepository
from app.ai.nlp.sentiment_analyzer import AspectSentimentAnalyzer
from app.extensions import db


class ReviewIntelligenceService:
    """Processes customer feedback into aspect ratings, praise/complaint summaries, and sentiment metrics."""

    def __init__(self):
        self.review_repo = ReviewRepository()
        self.product_repo = ProductRepository()

    def add_review(self, product_id: int, user_id: int, rating: int, title: str, content: str) -> Dict[str, Any]:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        # Analyze NLP aspect sentiment
        nlp_result = AspectSentimentAnalyzer.analyze_review(f"{title}. {content}")

        review = Review(
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            title=title.strip(),
            content=content.strip(),
            sentiment_polarity=nlp_result['polarity'],
            sentiment_label=nlp_result['label']
        )
        review.set_praises_list(nlp_result['praises'])
        review.set_complaints_list(nlp_result['complaints'])
        db.session.add(review)
        db.session.flush()

        # Add aspect ratings
        for aspect_name, asp_data in nlp_result['aspect_ratings'].items():
            aspect_rating = ReviewAspectRating(
                review_id=review.id,
                aspect_name=aspect_name,
                sentiment_score=asp_data['score'],
                sentiment_label=asp_data['label']
            )
            db.session.add(aspect_rating)

        # Update product aggregate ratings
        all_reviews = Review.query.filter_by(product_id=product_id).all()
        product.total_reviews_count = len(all_reviews)
        product.average_rating = round(sum(r.rating for r in all_reviews) / len(all_reviews), 2)

        # Update product aspect sentiment summary cache
        aspect_breakdown = self.review_repo.get_aspect_breakdown_for_product(product_id)
        aspect_dict = {k: int(v['average_score']) for k, v in aspect_breakdown.items()}
        product.aspect_sentiment_summary = json.dumps(aspect_dict)

        db.session.commit()
        return review.to_dict()

    def get_review_intelligence(self, product_id: int) -> Dict[str, Any]:
        reviews = self.review_repo.get_by_product(product_id)
        aspect_breakdown = self.review_repo.get_aspect_breakdown_for_product(product_id)

        all_praises = []
        all_complaints = []
        for r in reviews:
            all_praises.extend(r.get_praises_list())
            all_complaints.extend(r.get_complaints_list())

        return {
            'total_reviews': len(reviews),
            'aspect_breakdown': aspect_breakdown,
            'top_praises': list(dict.fromkeys(all_praises))[:5],
            'top_complaints': list(dict.fromkeys(all_complaints))[:5],
            'reviews': [r.to_dict() for r in reviews]
        }
''', encoding='utf-8')

# 8. cart_intelligence_service.py
(BASE / 'cart_intelligence_service.py').write_text('''from typing import Dict, Any, List
from app.models.cart import Cart, CartItem
from app.repositories.cart_repository import CartRepository, CartItemRepository
from app.repositories.product_repository import ProductRepository
from app.services.recommendation_service import RecommendationService
from app.extensions import db


class CartIntelligenceService:
    """Analyzes cart items for budget optimization, accessories, duplicates, and compatibility."""

    def __init__(self):
        self.cart_repo = CartRepository()
        self.cart_item_repo = CartItemRepository()
        self.product_repo = ProductRepository()
        self.rec_service = RecommendationService()

    def get_cart_with_intelligence(self, user_id: int) -> Dict[str, Any]:
        cart = self.cart_repo.get_by_user_id(user_id)
        items = cart.items.all()
        cart_data = cart.to_dict(include_items=True)

        insights = []
        potential_savings = 0.0
        complementary_products = []

        # 1. Analyze each item for cheaper alternatives
        for item in items:
            p = item.product
            if p:
                alts = self.rec_service.get_smart_alternatives(p.id, limit=1)
                if alts['budget_alternatives']:
                    cheaper = alts['budget_alternatives'][0]
                    save_amt = cheaper['savings_amount'] * item.quantity
                    potential_savings += save_amt
                    insights.append({
                        'type': 'savings_opportunity',
                        'item_title': p.title,
                        'message': f"You can save ₹{save_amt:,.0f} by choosing {cheaper['product']['title']}.",
                        'alternative_product': cheaper['product']
                    })

        # 2. Complementary Accessories Suggestions
        categories_in_cart = {item.product.category.name for item in items if item.product and item.product.category}
        if 'Laptops' in categories_in_cart and 'Computer Peripherals' not in categories_in_cart:
            insights.append({
                'type': 'accessory_suggestion',
                'message': 'Customers buying laptops frequently add a wireless mouse or USB-C multi-port hub.'
            })

        cart_data['intelligence'] = {
            'insights': insights,
            'potential_savings': round(potential_savings, 2),
            'free_shipping_eligible': cart.subtotal_amount >= 1000.0,
            'free_shipping_threshold': 1000.0
        }
        return cart_data

    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> Dict[str, Any]:
        cart = self.cart_repo.get_by_user_id(user_id)
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        item = self.cart_item_repo.get_item(cart.id, product_id)
        if item:
            item.quantity += quantity
        else:
            self.cart_item_repo.create(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.current_price
            )
        db.session.commit()
        return self.get_cart_with_intelligence(user_id)

    def update_quantity(self, user_id: int, cart_item_id: int, quantity: int) -> Dict[str, Any]:
        cart = self.cart_repo.get_by_user_id(user_id)
        item = self.cart_item_repo.get_by_id(cart_item_id)
        if item and item.cart_id == cart.id:
            if quantity <= 0:
                self.cart_item_repo.delete(item)
            else:
                item.quantity = quantity
                db.session.commit()
        return self.get_cart_with_intelligence(user_id)

    def remove_item(self, user_id: int, cart_item_id: int) -> Dict[str, Any]:
        return self.update_quantity(user_id, cart_item_id, 0)
''', encoding='utf-8')

# 9. wishlist_intelligence_service.py
(BASE / 'wishlist_intelligence_service.py').write_text('''from typing import Dict, Any, List
from app.models.wishlist import Wishlist, WishlistItem
from app.repositories.wishlist_repository import WishlistRepository, WishlistItemRepository
from app.repositories.product_repository import ProductRepository
from app.extensions import db


class WishlistIntelligenceService:
    """Manages saved items with price drops, back-in-stock alerts, and budget alternatives."""

    def __init__(self):
        self.wishlist_repo = WishlistRepository()
        self.wishlist_item_repo = WishlistItemRepository()
        self.product_repo = ProductRepository()

    def get_wishlist_with_insights(self, user_id: int) -> Dict[str, Any]:
        wishlist = self.wishlist_repo.get_by_user_id(user_id)
        items = wishlist.items.all()
        data = wishlist.to_dict(include_items=True)

        price_drop_total = sum(i.price_drop_amount for i in items)
        data['insights'] = {
            'total_price_drops_count': sum(1 for i in items if i.has_price_dropped),
            'total_savings_available': round(price_drop_total, 2)
        }
        return data

    def toggle_wishlist(self, user_id: int, product_id: int) -> Dict[str, Any]:
        wishlist = self.wishlist_repo.get_by_user_id(user_id)
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        item = self.wishlist_item_repo.get_item(wishlist.id, product_id)
        if item:
            self.wishlist_item_repo.delete(item)
            is_added = False
        else:
            self.wishlist_item_repo.create(
                wishlist_id=wishlist.id,
                product_id=product_id,
                price_when_added=product.current_price
            )
            is_added = True

        return {'is_wishlisted': is_added, 'wishlist': self.get_wishlist_with_insights(user_id)}
''', encoding='utf-8')

# 10. shopping_mission_service.py
(BASE / 'shopping_mission_service.py').write_text('''from typing import Dict, Any, List
from app.models.mission import ShoppingMission, ShoppingMissionItem
from app.models.product import Product
from app.repositories.mission_repository import MissionRepository, MissionItemRepository
from app.repositories.product_repository import ProductRepository
from app.ai.nlp.entity_extractor import EntityExtractor
from app.extensions import db


class ShoppingMissionService:
    """Builds multi-product goal baskets optimized for user constraints (e.g. Study Setup, Creator Kit)."""

    def __init__(self):
        self.mission_repo = MissionRepository()
        self.item_repo = MissionItemRepository()
        self.product_repo = ProductRepository()

    def build_mission(
        self,
        user_id: int,
        prompt: str,
        target_budget: float,
        optimization_mode: str = 'balanced'
    ) -> Dict[str, Any]:
        mission = self.mission_repo.create(
            user_id=user_id,
            title=prompt[:60],
            mission_prompt=prompt,
            target_budget=target_budget,
            optimization_mode=optimization_mode,
            status='optimized'
        )

        # Allocate budget slots across essential categories
        # Example setup: Core (60%), Ergonomics / Display (25%), Accessories / Audio (15%)
        slots = [
            {'role': 'Core Device', 'share': 0.60, 'cat_keywords': ['laptop', 'phone', 'console', 'camera']},
            {'role': 'Peripherals & Ergonomics', 'share': 0.25, 'cat_keywords': ['monitor', 'chair', 'desk', 'keyboard']},
            {'role': 'Audio & Focus', 'share': 0.15, 'cat_keywords': ['headphone', 'earbuds', 'mouse', 'dock']}
        ]

        total_allocated = 0.0
        for slot in slots:
            slot_budget = target_budget * slot['share']
            # Find best fitting product
            candidate = None
            for p in Product.query.filter_by(is_active=True).order_by(Product.average_rating.desc()).all():
                p_text = f"{p.title} {p.category.name if p.category else ''}".lower()
                if any(k in p_text for k in slot['cat_keywords']):
                    if p.current_price <= (slot_budget * 1.25):
                        candidate = p
                        break

            if candidate:
                self.item_repo.create(
                    mission_id=mission.id,
                    product_id=candidate.id,
                    slot_role=slot['role'],
                    assigned_budget=slot_budget,
                    actual_price=candidate.current_price,
                    selection_rationale=f"Selected for top tier reliability and verified rating ({candidate.average_rating}★)."
                )
                total_allocated += candidate.current_price

        mission.allocated_total = total_allocated
        mission.savings_amount = max(0.0, target_budget - total_allocated)
        mission.ai_rationale = (
            f"Basket optimized for a {optimization_mode} strategy within your ₹{target_budget:,.0f} limit. "
            f"Total estimated cost is ₹{total_allocated:,.0f}, leaving ₹{mission.savings_amount:,.0f} in remaining budget."
        )
        db.session.commit()

        return mission.to_dict(include_items=True)
''', encoding='utf-8')

# 11. seller_analytics_service.py
(BASE / 'seller_analytics_service.py').write_text('''from datetime import date, datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy import func
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.analytics import SellerMetricDaily, ProductPerformanceScore
from app.repositories.analytics_repository import SellerMetricDailyRepository, ProductPerformanceRepository
from app.extensions import db


class SellerAnalyticsService:
    """Computes real-time dynamic analytics, revenue trends, conversion funnels, and performance grades."""

    def __init__(self):
        self.metrics_repo = SellerMetricDailyRepository()
        self.performance_repo = ProductPerformanceRepository()

    def get_seller_dashboard_kpis(self, seller_id: int) -> Dict[str, Any]:
        # 1. Total revenue and orders from real OrderItem records
        summary = db.session.query(
            func.count(OrderItem.id).label('total_units'),
            func.sum(OrderItem.total_price).label('total_revenue'),
            func.sum(OrderItem.gross_profit).label('total_profit')
        ).filter(OrderItem.seller_id == seller_id).first()

        total_units = int(summary.total_units or 0)
        total_revenue = float(summary.total_revenue or 0.0)
        total_profit = float(summary.total_profit or 0.0)

        # 2. Total active products count
        active_products = Product.query.filter_by(seller_id=seller_id, is_active=True).count()

        # 3. Aggregate 30-day trend
        since = date.today() - timedelta(days=30)
        daily_metrics = self.metrics_repo.get_latest_metrics(seller_id, days=30)
        
        revenue_trend = [
            {'date': m.metric_date.isoformat(), 'revenue': round(m.total_revenue, 2), 'orders': m.total_orders}
            for m in daily_metrics
        ]

        return {
            'total_revenue': round(total_revenue, 2),
            'total_profit': round(total_profit, 2),
            'units_sold': total_units,
            'active_products_count': active_products,
            'average_order_value': round(total_revenue / max(1, total_units), 2),
            'revenue_trend': revenue_trend
        }

    def get_product_performance_ranking(self, seller_id: int) -> List[Dict[str, Any]]:
        scores = self.performance_repo.filter_by(seller_id=seller_id)
        return [s.to_dict() for s in scores]
''', encoding='utf-8')

# 12. inventory_intelligence_service.py
(BASE / 'inventory_intelligence_service.py').write_text('''from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.models.inventory import ProductInventory, InventoryAlert
from app.repositories.inventory_repository import InventoryRepository, InventoryAlertRepository
from app.repositories.analytics_repository import ProductPerformanceRepository
from app.extensions import db


class InventoryIntelligenceService:
    """Manages inventory health, safety stocks, stockout warnings, and dead-stock identification."""

    def __init__(self):
        self.inventory_repo = InventoryRepository()
        self.alert_repo = InventoryAlertRepository()
        self.performance_repo = ProductPerformanceRepository()

    def get_inventory_summary(self, seller_id: int) -> Dict[str, Any]:
        items = self.inventory_repo.get_seller_inventory(seller_id)
        alerts = self.alert_repo.get_unresolved_by_seller(seller_id)
        dead_stock = self.performance_repo.get_dead_stock(seller_id)

        low_stock_count = sum(1 for i in items if i.available_quantity <= i.reorder_point and i.available_quantity > 0)
        out_of_stock_count = sum(1 for i in items if i.available_quantity <= 0)
        total_units_on_hand = sum(i.total_on_hand for i in items)

        return {
            'total_sku_count': len(items),
            'total_units_on_hand': total_units_on_hand,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'dead_stock_count': len(dead_stock),
            'active_alerts': [a.to_dict() for a in alerts],
            'inventory_items': [i.to_dict() for i in items]
        }

    def restock_inventory(self, inventory_id: int, quantity_added: int) -> Dict[str, Any]:
        inv = self.inventory_repo.get_by_id(inventory_id)
        if not inv:
            raise ValueError("Inventory record not found.")

        inv.available_quantity += quantity_added
        inv.last_restocked_at = datetime.now(timezone.utc)
        inv.stock_status = 'in_stock'
        db.session.commit()
        return inv.to_dict()
''', encoding='utf-8')

# 13. demand_forecasting_service.py
(BASE / 'demand_forecasting_service.py').write_text('''import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from app.models.forecast import DemandForecast
from app.models.product import Product
from app.repositories.forecast_repository import ForecastRepository
from app.repositories.product_repository import ProductRepository
from app.extensions import db


class DemandForecastingService:
    """Predicts time-series customer demand utilizing moving averages and Holt-Winters inspired smoothing."""

    def __init__(self):
        self.forecast_repo = ForecastRepository()
        self.product_repo = ProductRepository()

    def generate_product_forecast(self, product_id: int, horizon_days: int = 14) -> Dict[str, Any]:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        inv = product.inventory
        current_stock = inv.available_quantity if inv else 0
        
        # Calculate daily velocity baseline
        velocity = max(0.5, inv.daily_sales_velocity if inv and inv.daily_sales_velocity > 0 else (product.purchases_count / 60.0))

        # Generate simulated daily projections with mild weekly seasonality
        daily_projections = []
        cum_demand = 0
        today = datetime.now(timezone.utc)

        for d in range(1, horizon_days + 1):
            day_date = today + timedelta(days=d)
            # Weekend multiplier
            multiplier = 1.25 if day_date.weekday() in (5, 6) else 0.95
            predicted_day = max(1, int(round(velocity * multiplier)))
            cum_demand += predicted_day
            daily_projections.append({
                'day': d,
                'date': day_date.strftime('%Y-%m-%d'),
                'predicted_units': predicted_day,
                'cumulative_units': cum_demand
            })

        stockout_predicted = cum_demand > current_stock
        days_to_stockout = round(current_stock / velocity, 1) if velocity > 0 else 999.0
        reorder_qty = max(0, cum_demand - current_stock + 20)

        forecast = self.forecast_repo.create(
            product_id=product_id,
            seller_id=product.seller_id,
            horizon_days=horizon_days,
            forecast_model='holt_winters_hybrid',
            current_stock=current_stock,
            predicted_demand_total=cum_demand,
            predicted_daily_rate=round(velocity, 2),
            confidence_interval_low=int(cum_demand * 0.85),
            confidence_interval_high=int(cum_demand * 1.15),
            stockout_predicted=stockout_predicted,
            estimated_days_to_stockout=days_to_stockout if stockout_predicted else None,
            recommended_reorder_qty=reorder_qty
        )
        forecast.set_daily_projections_list(daily_projections)
        db.session.commit()

        return forecast.to_dict()
''', encoding='utf-8')

# 14. pricing_intelligence_service.py
(BASE / 'pricing_intelligence_service.py').write_text('''from typing import Dict, Any, List
from app.models.product import Product
from app.repositories.product_repository import ProductRepository


class PricingIntelligenceService:
    """Dynamic pricing recommendations based on demand velocity, inventory age, and competitor prices."""

    def __init__(self):
        self.product_repo = ProductRepository()

    def get_pricing_recommendations(self, seller_id: int) -> List[Dict[str, Any]]:
        products = self.product_repo.get_by_seller(seller_id, active_only=True)
        recommendations = []

        for p in products:
            current = p.current_price
            inv = p.inventory
            perf = p.performance_score

            rec_price = current
            reason = "Price is currently optimal for market demand."
            action = "maintain"

            if perf and perf.is_dead_stock:
                rec_price = round(current * 0.85, 2)
                reason = "Dead stock clearance: 15% discount recommended to recover tied-up capital."
                action = "markdown_clearance"
            elif inv and inv.available_quantity > 80 and inv.days_of_supply > 60:
                rec_price = round(current * 0.92, 2)
                reason = "High inventory levels: 8% promotional markdown recommended to accelerate sell-through."
                action = "promotional_discount"
            elif inv and inv.available_quantity <= 5 and inv.daily_sales_velocity > 2:
                rec_price = round(current * 1.05, 2)
                reason = "High demand & scarce stock: 5% premium adjustment recommended to maximize margins."
                action = "premium_adjustment"

            recommendations.append({
                'product_id': p.id,
                'product_title': p.title,
                'current_price': current,
                'recommended_price': rec_price,
                'price_change_amount': round(rec_price - current, 2),
                'action': action,
                'reason': reason
            })

        return recommendations
''', encoding='utf-8')

# 15. customer_segmentation_service.py
(BASE / 'customer_segmentation_service.py').write_text('''from typing import Dict, Any, List
from app.models.analytics import CustomerSegment
from app.repositories.analytics_repository import CustomerSegmentRepository


class CustomerSegmentationService:
    """RFM (Recency, Frequency, Monetary) customer segmentation and cohort intelligence."""

    def __init__(self):
        self.segment_repo = CustomerSegmentRepository()

    def get_all_segments(self) -> List[Dict[str, Any]]:
        segments = self.segment_repo.get_all()
        if not segments:
            # Seed default RFM segments if not present
            defaults = [
                CustomerSegment(name='Champions', description='Bought recently, buy often, and spend the most.', recommended_strategy='Reward with exclusive early access and VIP perks.', member_count=18, average_spend=45200.0),
                CustomerSegment(name='Loyal Customers', description='Buy regularly and responsive to promotions.', recommended_strategy='Upsell premium tiers and request product reviews.', member_count=42, average_spend=28400.0),
                CustomerSegment(name='High Potential', description='Recent buyers with above-average spend.', recommended_strategy='Offer complementary accessories and membership programs.', member_count=35, average_spend=18500.0),
                CustomerSegment(name='At Risk', description='Purchased frequently in past but have lapsed in recent months.', recommended_strategy='Send win-back personalized price-drop campaigns.', member_count=22, average_spend=12000.0),
                CustomerSegment(name='Bargain Hunters', description='High price sensitivity, primarily buy during discounts.', recommended_strategy='Target with clearance sales and bundle discounts.', member_count=65, average_spend=6400.0),
                CustomerSegment(name='New Shoppers', description='First purchase made within the last 30 days.', recommended_strategy='Provide onboarding assistance and follow-up support.', member_count=50, average_spend=8900.0)
            ]
            self.segment_repo.bulk_create(defaults)
            segments = defaults

        return [s.to_dict() for s in segments]
''', encoding='utf-8')

# 16. order_service.py
(BASE / 'order_service.py').write_text('''import secrets
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.models.order import Order, OrderItem, OrderStatusHistory
from app.models.inventory import InventoryTransaction
from app.repositories.order_repository import OrderRepository, OrderItemRepository
from app.repositories.cart_repository import CartRepository, CartItemRepository
from app.repositories.product_repository import ProductRepository
from app.extensions import db


class OrderService:
    """Internal simulated order placement, fulfillment lifecycle, and inventory decrement."""

    def __init__(self):
        self.order_repo = OrderRepository()
        self.order_item_repo = OrderItemRepository()
        self.cart_repo = CartRepository()
        self.cart_item_repo = CartItemRepository()
        self.product_repo = ProductRepository()

    def checkout_cart(
        self,
        user_id: int,
        shipping_name: str,
        shipping_address_line1: str,
        shipping_city: str,
        shipping_state: str,
        shipping_postal_code: str,
        payment_method: str = 'simulated_upi',
        shipping_phone: str = ''
    ) -> Dict[str, Any]:
        cart = self.cart_repo.get_by_user_id(user_id)
        items = cart.items.all()
        if not items:
            raise ValueError("Your cart is empty. Add items to checkout.")

        order_number = f"ORD-{secrets.token_hex(4).upper()}"
        subtotal = cart.subtotal_amount
        shipping_fee = 0.0 if subtotal >= 1000.0 else 99.0
        tax = round(subtotal * 0.18, 2)  # 18% simulated GST
        total = subtotal + shipping_fee + tax

        order = Order(
            order_number=order_number,
            user_id=user_id,
            status='processing',
            subtotal_amount=subtotal,
            tax_amount=tax,
            shipping_fee=shipping_fee,
            total_amount=total,
            payment_method=payment_method,
            payment_status='paid',
            shipping_name=shipping_name,
            shipping_phone=shipping_phone,
            shipping_address_line1=shipping_address_line1,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_postal_code=shipping_postal_code
        )
        db.session.add(order)
        db.session.flush()

        # Add line items & deduct inventory
        for item in items:
            p = item.product
            order_item = OrderItem(
                order_id=order.id,
                product_id=p.id,
                seller_id=p.seller_id,
                product_title=p.title,
                product_sku=p.sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
                unit_cost=p.cost_price,
                total_price=item.total_price,
                item_status='processing'
            )
            db.session.add(order_item)

            # Deduct inventory & record transaction
            if p.inventory:
                p.inventory.available_quantity = max(0, p.inventory.available_quantity - item.quantity)
                tx = InventoryTransaction(
                    inventory_id=p.inventory.id,
                    transaction_type='sale',
                    quantity_change=-item.quantity,
                    quantity_after=p.inventory.available_quantity,
                    reference_id=order_number,
                    notes='Order checkout fulfillment'
                )
                db.session.add(tx)

            p.purchases_count += item.quantity

        # Add initial status history
        history = OrderStatusHistory(order_id=order.id, status='processing', comment='Order confirmed and payment verified.')
        db.session.add(history)

        # Clear active cart
        self.cart_item_repo.clear_cart(cart.id)
        db.session.commit()

        return order.to_dict(include_items=True)
''', encoding='utf-8')

# 17. __init__.py for app/services
(BASE / '__init__.py').write_text('''from app.services.auth_service import AuthService
from app.services.catalog_service import CatalogService
from app.services.search_service import SearchService
from app.services.copilot_service import CopilotService
from app.services.recommendation_service import RecommendationService
from app.services.comparison_service import ComparisonService
from app.services.review_intelligence_service import ReviewIntelligenceService
from app.services.cart_intelligence_service import CartIntelligenceService
from app.services.wishlist_intelligence_service import WishlistIntelligenceService
from app.services.shopping_mission_service import ShoppingMissionService
from app.services.seller_analytics_service import SellerAnalyticsService
from app.services.inventory_intelligence_service import InventoryIntelligenceService
from app.services.demand_forecasting_service import DemandForecastingService
from app.services.pricing_intelligence_service import PricingIntelligenceService
from app.services.customer_segmentation_service import CustomerSegmentationService
from app.services.order_service import OrderService

__all__ = [
    'AuthService',
    'CatalogService',
    'SearchService',
    'CopilotService',
    'RecommendationService',
    'ComparisonService',
    'ReviewIntelligenceService',
    'CartIntelligenceService',
    'WishlistIntelligenceService',
    'ShoppingMissionService',
    'SellerAnalyticsService',
    'InventoryIntelligenceService',
    'DemandForecastingService',
    'PricingIntelligenceService',
    'CustomerSegmentationService',
    'OrderService'
]
''', encoding='utf-8')

print('All 17 Services modules generated successfully!')
