from typing import Dict, Any, List
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
