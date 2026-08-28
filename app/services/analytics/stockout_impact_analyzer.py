from typing import Dict, Any, List


class StockoutImpactAnalyzer:
    """Quantifies lost revenue, margin erosion, and velocity penalty incurred from stockouts."""

    @staticmethod
    def calculate_stockout_loss(
        daily_velocity: float,
        unit_sale_price: float,
        unit_cost_price: float,
        stockout_days: int,
        search_impression_volume: int = 100
    ) -> Dict[str, Any]:
        velocity = max(0.0, daily_velocity)
        price = max(0.0, unit_sale_price)
        cost = max(0.0, unit_cost_price)
        unit_margin = max(0.0, price - cost)
        days = max(0, stockout_days)

        lost_units = round(velocity * days, 1)
        lost_gross_revenue = round(lost_units * price, 2)
        lost_gross_profit = round(lost_units * unit_margin, 2)

        # Estimate search abandonment impact
        estimated_abandoned_searches = int(search_impression_volume * (days / 30.0))

        # Strategic guidance
        urgency = "LOW"
        if lost_gross_revenue > 100000.0 or days > 14:
            urgency = "CRITICAL"
        elif lost_gross_revenue > 30000.0 or days > 7:
            urgency = "HIGH"
        elif lost_gross_revenue > 5000.0:
            urgency = "MEDIUM"

        return {
            'stockout_days': days,
            'estimated_lost_units': lost_units,
            'estimated_lost_revenue': lost_gross_revenue,
            'estimated_lost_profit': lost_gross_profit,
            'estimated_search_bounces': estimated_abandoned_searches,
            'impact_urgency': urgency,
            'mitigation_strategy': f"Urgency: {urgency}. Expedite supplier reorder by reducing lead time buffer and raising safety stock to prevent recurrent revenue leakage."
        }
