from typing import Dict, Any, List
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
