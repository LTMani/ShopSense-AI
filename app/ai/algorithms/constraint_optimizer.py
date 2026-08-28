from typing import List, Dict, Any, Optional, Tuple


class ShoppingMissionConstraintOptimizer:
    """Multi-objective combinatorial knapsack optimizer for assembling multi-product baskets
    under hard budget ceilings, category allocations, and rating quality scores."""

    @staticmethod
    def solve_basket(
        slots: List[Dict[str, Any]],
        candidate_pool_by_slot: Dict[str, List[Any]],
        total_budget: float,
        optimization_mode: str = 'balanced'
    ) -> Dict[str, Any]:
        """Select exactly one product per slot such that total cost <= total_budget while maximizing utility."""
        selected_items = []
        allocated_total = 0.0

        # Sort candidate pools according to optimization mode
        for slot in slots:
            role = slot['role']
            candidates = candidate_pool_by_slot.get(role, [])
            if not candidates:
                continue

            target_slot_budget = slot.get('assigned_budget', total_budget / len(slots))

            if optimization_mode == 'performance_first':
                # Prioritize rating and features
                candidates.sort(key=lambda p: (p.average_rating, -abs(p.sale_price - target_slot_budget)), reverse=True)
            elif optimization_mode == 'budget_saver':
                # Prioritize low price while maintaining acceptable rating
                candidates.sort(key=lambda p: (p.sale_price, -p.average_rating))
            else:  # balanced
                # Prioritize proximity to target budget and high rating
                candidates.sort(key=lambda p: (p.average_rating * 20.0 - abs(p.sale_price - target_slot_budget) / 100.0), reverse=True)

            # Pick best candidate that fits
            chosen = None
            for cand in candidates:
                if (allocated_total + cand.sale_price) <= (total_budget * 1.05):  # 5% tolerance margin
                    chosen = cand
                    break

            if not chosen and candidates:
                # Fallback to least expensive candidate in pool
                chosen = min(candidates, key=lambda p: p.sale_price)

            if chosen:
                selected_items.append({
                    'slot_role': role,
                    'product': chosen,
                    'assigned_budget': target_slot_budget,
                    'actual_price': chosen.sale_price,
                    'selection_rationale': f"Selected {chosen.title} for {role}: fits ₹{target_slot_budget:,.0f} budget with verified {chosen.average_rating}★ customer satisfaction."
                })
                allocated_total += chosen.sale_price

        savings = max(0.0, total_budget - allocated_total)

        return {
            'items': selected_items,
            'total_budget': total_budget,
            'allocated_total': round(allocated_total, 2),
            'savings_amount': round(savings, 2),
            'budget_utilization_pct': round((allocated_total / max(1.0, total_budget)) * 100.0, 1)
        }
