from typing import List, Dict, Any, Tuple, Set
from collections import defaultdict


class MarketBasketAssociationEngine:
    """Mines transaction co-occurrences using Apriori association rules (Support, Confidence, Lift)."""

    @classmethod
    def find_associated_products(
        cls,
        target_product_id: int,
        transaction_baskets: List[List[int]],
        min_support: float = 0.01,
        min_confidence: float = 0.15
    ) -> List[Dict[str, Any]]:
        total_tx = len(transaction_baskets)
        if total_tx == 0:
            return []

        item_counts: Dict[int, int] = defaultdict(int)
        pair_counts: Dict[Tuple[int, int], int] = defaultdict(int)

        for basket in transaction_baskets:
            unique_items = list(set(basket))
            for item in unique_items:
                item_counts[item] += 1

            for i in range(len(unique_items)):
                for j in range(i + 1, len(unique_items)):
                    pair = (min(unique_items[i], unique_items[j]), max(unique_items[i], unique_items[j]))
                    pair_counts[pair] += 1

        target_count = item_counts.get(target_product_id, 0)
        if target_count == 0:
            return []

        target_support = target_count / total_tx
        recommendations = []

        for pair, co_count in pair_counts.items():
            if target_product_id in pair:
                other_id = pair[1] if pair[0] == target_product_id else pair[0]
                other_count = item_counts[other_id]

                support = co_count / total_tx
                confidence = co_count / target_count
                other_support = other_count / total_tx
                lift = confidence / max(0.0001, other_support)

                if support >= min_support and confidence >= min_confidence:
                    recommendations.append({
                        'product_id': other_id,
                        'support': round(support, 4),
                        'confidence': round(confidence, 4),
                        'lift': round(lift, 2),
                        'co_occurrence_count': co_count
                    })

        # Sort by lift and confidence
        recommendations.sort(key=lambda r: (r['lift'], r['confidence']), reverse=True)
        return recommendations[:6]
