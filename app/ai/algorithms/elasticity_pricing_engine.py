from typing import Dict, Any, List, Optional, Tuple


class DynamicPricingElasticityEngine:
    """Computes price elasticity of demand (PED), profit-maximizing optimal pricing,
    and automated dead-stock liquidation markdowns."""

    @staticmethod
    def calculate_price_elasticity(
        historical_price_points: List[Tuple[float, int]]
    ) -> float:
        """Calculate Price Elasticity of Demand (PED) = (% Change in Qty) / (% Change in Price)."""
        if len(historical_price_points) < 2:
            return -1.5  # Standard elastic default

        p1, q1 = historical_price_points[0]
        p2, q2 = historical_price_points[-1]

        if p1 == p2 or (p1 + p2) == 0:
            return -1.5

        pct_change_q = (q2 - q1) / max(1.0, (q1 + q2) / 2.0)
        pct_change_p = (p2 - p1) / max(1.0, (p1 + p2) / 2.0)

        if pct_change_p == 0:
            return -1.5

        ped = pct_change_q / pct_change_p
        return round(ped, 2)

    @classmethod
    def recommend_optimal_price(
        cls,
        current_price: float,
        cost_price: float,
        current_stock: int,
        days_without_sale: int,
        competitor_price: Optional[float] = None,
        min_margin_pct: float = 0.12
    ) -> Dict[str, Any]:
        """Calculates optimal price recommendations balancing margin floor and stock clearance velocity."""
        margin_floor = cost_price * (1.0 + min_margin_pct)
        action = "maintain"
        reason = "Current price maintains healthy margins and steady sales velocity."
        recommended_price = current_price

        # Rule 1: Severe Dead Stock liquidation (> 60 days without sales)
        if days_without_sale >= 60 and current_stock > 10:
            action = "liquidate_markdown"
            recommended_price = max(margin_floor, current_price * 0.82)
            reason = f"Dead stock detected ({days_without_sale} days no sales, {current_stock} units tied up). Markdown to liquidate capital."

        # Rule 2: Moderate Stagnation (> 30 days without sales)
        elif days_without_sale >= 30 and current_stock > 5:
            action = "promotional_discount"
            recommended_price = max(margin_floor, current_price * 0.90)
            reason = "Slow inventory turnover. A 10% promotional discount will stimulate conversion."

        # Rule 3: High demand with critically low stock (< 5 units remaining, sold recently)
        elif days_without_sale <= 7 and current_stock <= 5 and current_stock > 0:
            action = "margin_expansion"
            recommended_price = round(current_price * 1.05, 2)
            reason = "High velocity and scarce remaining inventory. 5% price premium expands margin while slowing stockout."

        # Rule 4: Undercut by direct competitor
        elif competitor_price and competitor_price < current_price and competitor_price >= margin_floor:
            action = "match_competitor"
            recommended_price = round(competitor_price * 0.99, 2)
            reason = f"Competitor priced at ₹{competitor_price:,.0f}. Minor price match to capture buy box."

        delta = round(recommended_price - current_price, 2)

        return {
            'current_price': current_price,
            'cost_price': cost_price,
            'recommended_price': round(recommended_price, 2),
            'price_change_amount': delta,
            'price_change_percent': round((delta / current_price) * 100.0, 1),
            'action': action,
            'reason': reason,
            'margin_floor': round(margin_floor, 2)
        }
