from typing import Dict, Any, List


class ConversionFunnelAnalyzer:
    """Multi-stage conversion funnel analytics across browsing, evaluation, carting, and purchasing."""

    @staticmethod
    def analyze_funnel(
        impressions: int,
        product_views: int,
        cart_adds: int,
        checkout_starts: int,
        orders_completed: int
    ) -> Dict[str, Any]:
        impr = max(1, impressions)
        views = max(0, product_views)
        adds = max(0, cart_adds)
        starts = max(0, checkout_starts)
        completed = max(0, orders_completed)

        view_rate = round((views / impr) * 100.0, 2)
        cart_rate = round((adds / max(1, views)) * 100.0, 2)
        checkout_rate = round((starts / max(1, adds)) * 100.0, 2)
        purchase_rate = round((completed / max(1, starts)) * 100.0, 2)
        overall_conversion = round((completed / impr) * 100.0, 2)

        dropoffs = [
            {'stage': 'Impression to View', 'dropoff_pct': round(100.0 - view_rate, 1)},
            {'stage': 'View to Cart Add', 'dropoff_pct': round(100.0 - cart_rate, 1)},
            {'stage': 'Cart to Checkout', 'dropoff_pct': round(100.0 - checkout_rate, 1)},
            {'stage': 'Checkout to Order', 'dropoff_pct': round(100.0 - purchase_rate, 1)}
        ]

        # Identify biggest bottleneck
        biggest_dropoff = max(dropoffs, key=lambda x: x['dropoff_pct'])

        recommendations = []
        if cart_rate < 12.0:
            recommendations.append("Low View-to-Cart rate: Enhance product images, highlight aspect review scores, and clarify key technical specifications.")
        if checkout_rate < 40.0:
            recommendations.append("High Cart Abandonment: Offer free shipping thresholds, display trust badges, and suggest relevant accessories in-cart.")
        if purchase_rate < 70.0:
            recommendations.append("Checkout drop-off: Streamline checkout form fields and provide flexible simulated payment alternatives.")

        if not recommendations:
            recommendations.append("Funnel health is strong across all commercial stages. Focus on driving top-of-funnel catalog traffic.")

        return {
            'stages': [
                {'name': 'Catalog Impressions', 'count': impr, 'conversion_from_prev': 100.0},
                {'name': 'Product Detail Views', 'count': views, 'conversion_from_prev': view_rate},
                {'name': 'Add to Cart', 'count': adds, 'conversion_from_prev': cart_rate},
                {'name': 'Checkout Initiated', 'count': starts, 'conversion_from_prev': checkout_rate},
                {'name': 'Orders Completed', 'count': completed, 'conversion_from_prev': purchase_rate}
            ],
            'overall_conversion_rate': overall_conversion,
            'primary_bottleneck': biggest_dropoff['stage'],
            'bottleneck_dropoff_pct': biggest_dropoff['dropoff_pct'],
            'recommendations': recommendations
        }
