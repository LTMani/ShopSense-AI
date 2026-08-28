import re
from typing import Dict, Any, Optional, List
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.ai.nlp.entity_extractor import EntityExtractor
from app.ai.nlp.vector_similarity import VectorSimilarityEngine
from app.ai.nlp.tokenizer import TextTokenizer


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

        # Clean query text for search: remove numbers, currency symbols, and budget indicator words
        clean_text_query = query
        if query:
            tokens = TextTokenizer.tokenize(query, remove_stopwords=True)
            # Remove numeric strings
            clean_tokens = [t for t in tokens if not t.isdigit() and t not in ('under', 'below', 'budget', 'rs', 'inr')]
            clean_text_query = " ".join(clean_tokens)

        # 2. Database candidate search
        search_result = self.product_repo.search_products(
            query_text=clean_text_query,
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
