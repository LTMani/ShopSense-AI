from typing import Dict, Any, List, Optional
from app.models.product import Product
from app.models.analytics import ProductPerformanceScore
from app.models.inventory import ProductInventory


class SellerDiagnosticEngine:
    """Root-cause diagnostic reasoner explaining sales fluctuations, traffic drops, and inventory bottlenecks."""

    @classmethod
    def diagnose_product_performance(
        cls,
        product: Product,
        inventory: Optional[ProductInventory] = None,
        performance: Optional[ProductPerformanceScore] = None
    ) -> Dict[str, Any]:
        findings = []
        recommendations = []
        severity = 'normal'

        # 1. Inventory Check
        if inventory:
            if inventory.available_quantity <= 0:
                findings.append("Product is currently OUT OF STOCK, causing 100% loss of potential conversion.")
                recommendations.append("Initiate immediate supplier reorder.")
                severity = 'critical'
            elif inventory.available_quantity <= inventory.safety_stock:
                findings.append(f"Stock level is low ({inventory.available_quantity} units remaining, safety stock is {inventory.safety_stock}).")
                recommendations.append("Reorder stock before lead-time depletion.")
                severity = 'high'
            elif inventory.days_of_supply > 90:
                findings.append(f"Excess inventory detected ({inventory.days_of_supply} days of supply on hand).")
                recommendations.append("Consider a 10-15% promotional discount or product bundle.")

        # 2. Performance and Sales Velocity
        if performance:
            if performance.is_dead_stock:
                findings.append(f"Flagged as DEAD STOCK: No sales recorded in the last {performance.days_since_last_sale} days.")
                recommendations.append("Execute clearance markdown or bundle with a high-velocity product.")
                severity = 'high'
            if performance.conversion_score < 40:
                findings.append("Low conversion rate relative to page views. Visitors view the item but drop off before cart addition.")
                recommendations.append("Optimize product imagery, lower price point, or address common customer complaints in description.")

        # 3. Reviews & Aspect Sentiment
        aspects = product.get_aspect_sentiment_dict()
        for aspect_name, score in aspects.items():
            if score < 60:
                findings.append(f"Negative review sentiment on '{aspect_name}' ({score}% satisfaction).")
                recommendations.append(f"Review customer feedback regarding {aspect_name} to improve batch quality or adjust specifications.")

        if not findings:
            findings.append("Product is performing stably with healthy sales velocity and balanced inventory.")
            recommendations.append("Maintain current pricing and inventory replenishment cadence.")

        return {
            'product_id': product.id,
            'product_title': product.title,
            'severity': severity,
            'findings': findings,
            'recommendations': recommendations
        }
