from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Tuple


class CustomerRFMClusteringEngine:
    """Computes Recency, Frequency, and Monetary scores and assigns customer behavioral cohorts."""

    @staticmethod
    def calculate_rfm_scores(
        customers_data: List[Dict[str, Any]],
        reference_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        if not customers_data:
            return []

        # Sort and assign 1-5 rank percentiles
        n = len(customers_data)
        
        # Sort by recency (lower days is better -> higher score)
        recency_sorted = sorted(customers_data, key=lambda c: c['days_since_last_order'])
        # Sort by frequency (higher orders is better)
        frequency_sorted = sorted(customers_data, key=lambda c: c['order_count'], reverse=True)
        # Sort by monetary (higher spend is better)
        monetary_sorted = sorted(customers_data, key=lambda c: c['total_spent'], reverse=True)

        r_scores = {c['user_id']: 5 - int(4.0 * i / max(1, n)) for i, c in enumerate(recency_sorted)}
        f_scores = {c['user_id']: 5 - int(4.0 * i / max(1, n)) for i, c in enumerate(frequency_sorted)}
        m_scores = {c['user_id']: 5 - int(4.0 * i / max(1, n)) for i, c in enumerate(monetary_sorted)}

        results = []
        for c in customers_data:
            uid = c['user_id']
            r = r_scores[uid]
            f = f_scores[uid]
            m = m_scores[uid]
            segment, strategy = CustomerRFMClusteringEngine._determine_segment(r, f, m)

            results.append({
                'user_id': uid,
                'name': c.get('name', 'Customer'),
                'r_score': r,
                'f_score': f,
                'm_score': m,
                'rfm_composite': f"{r}{f}{m}",
                'segment': segment,
                'strategy': strategy,
                'estimated_ltv': round(c['total_spent'] * (1.2 + 0.1 * f), 2)
            })

        return results

    @staticmethod
    def _determine_segment(r: int, f: int, m: int) -> Tuple[str, str]:
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions", "Offer exclusive VIP previews, reward loyalty with priority support, and request testimonials."
        elif r >= 3 and f >= 3:
            return "Loyal Customers", "Upsell higher-margin products and enroll in reward points programs."
        elif r >= 4 and f <= 2:
            return "New High-Potential", "Send welcome onboarding series, offer second-purchase discount vouchers."
        elif r <= 2 and f >= 3:
            return "At-Risk Customers", "Send win-back campaigns, personalized reactivation discounts, and feedback surveys."
        elif m >= 4 and f <= 2:
            return "Big Spenders / Bargain Hunters", "Promote new premium hardware arrivals and bundled high-value accessories."
        else:
            return "Hibernating Shoppers", "Re-engage via seasonal clearance promotions or new product releases."
