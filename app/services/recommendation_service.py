from typing import Dict, Any, List, Optional
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
