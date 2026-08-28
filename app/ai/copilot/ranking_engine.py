from typing import List, Dict, Any, Optional
from app.models.product import Product


class CopilotRankingEngine:
    """Multi-criteria ranking engine scoring candidate products based on budget fit, specs, and ratings."""

    @classmethod
    def rank_candidates(
        cls,
        products: List[Product],
        budget: Optional[float] = None,
        priorities: Optional[List[str]] = None,
        primary_usage: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if not products:
            return []

        priorities = priorities or []
        results = []

        for p in products:
            score = 70.0  # baseline
            reasons = []

            # 1. Budget scoring
            if budget and budget > 0:
                price = p.current_price
                if price <= budget:
                    ratio = price / budget
                    if ratio >= 0.65:
                        score += 15.0
                        reasons.append(f"Well within your target budget of ₹{budget:,.0f}")
                    else:
                        score += 10.0
                        reasons.append("Great budget savings option")
                else:
                    over_ratio = (price - budget) / budget
                    penalty = min(35.0, over_ratio * 40.0)
                    score -= penalty
                    if over_ratio < 0.10:
                        reasons.append("Slightly above budget but high specification match")
                    else:
                        reasons.append("Above target budget")

            # 2. Rating & Review Sentiment
            if p.average_rating >= 4.5:
                score += 8.0
                reasons.append(f"Exceptional rating ({p.average_rating}★ from {p.total_reviews_count} buyers)")
            elif p.average_rating >= 4.0:
                score += 5.0
                reasons.append(f"Highly rated ({p.average_rating}★)")

            # 3. Usage & Priority match
            aspects = p.get_aspect_sentiment_dict()
            usage_str = (p.target_usage or '').lower()
            features_str = ' '.join(p.get_key_features_list()).lower()

            for prio in priorities:
                prio_lower = prio.lower()
                if prio_lower in usage_str or prio_lower in features_str:
                    score += 6.0
                    reasons.append(f"Optimized for {prio}")
                if prio_lower in aspects:
                    a_score = aspects[prio_lower]
                    if a_score >= 80:
                        score += 5.0
                        reasons.append(f"Strong verified sentiment for {prio} ({a_score}%)")

            # Clamp score between 10 and 99
            final_score = max(10.0, min(98.0, score))
            results.append({
                'product': p,
                'match_score': round(final_score, 1),
                'reasons': reasons[:4]
            })

        results.sort(key=lambda x: x['match_score'], reverse=True)

        # Assign badges
        if results:
            results[0]['badge'] = 'Best Match'
            
            # Find Best Value (highest score / price ratio)
            cheapest = sorted(results, key=lambda x: x['product'].current_price)
            if len(cheapest) > 1 and cheapest[0] != results[0]:
                cheapest[0]['badge'] = 'Best Value'

            # Find Best Battery / Best Performance if applicable
            for r in results:
                if 'badge' not in r:
                    aspects = r['product'].get_aspect_sentiment_dict()
                    if aspects.get('battery', 0) >= 88:
                        r['badge'] = 'Best Battery'
                        break
                    elif aspects.get('performance', 0) >= 90:
                        r['badge'] = 'Top Performance'
                        break

        return results
