from datetime import datetime, date, timezone
from typing import List, Dict, Any
from collections import defaultdict


class CustomerCohortRetentionAnalyzer:
    """Builds weekly and monthly customer acquisition retention grids and repeat purchase telemetry."""

    @staticmethod
    def calculate_monthly_cohorts(orders_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Map customers to acquisition month
        customer_first_month: Dict[int, str] = {}
        monthly_activity: Dict[str, Dict[int, float]] = defaultdict(lambda: defaultdict(float))

        for order in sorted(orders_data, key=lambda o: o['created_at']):
            uid = order['user_id']
            created_dt = order['created_at']
            if isinstance(created_dt, str):
                created_dt = datetime.fromisoformat(created_dt)

            month_str = created_dt.strftime('%Y-%m')
            if uid not in customer_first_month:
                customer_first_month[uid] = month_str

            monthly_activity[month_str][uid] += float(order.get('total_amount', 0.0))

        # Build cohort matrix
        cohort_groups: Dict[str, List[int]] = defaultdict(list)
        for uid, acq_month in customer_first_month.items():
            cohort_groups[acq_month].append(uid)

        all_months = sorted(monthly_activity.keys())
        results = []

        for acq_month, cohort_users in sorted(cohort_groups.items()):
            initial_size = len(cohort_users)
            retention_row = []

            for active_month in all_months:
                if active_month < acq_month:
                    continue
                
                active_count = sum(1 for uid in cohort_users if uid in monthly_activity[active_month])
                pct = round((active_count / max(1, initial_size)) * 100.0, 1)
                retention_row.append({
                    'month': active_month,
                    'active_users': active_count,
                    'retention_pct': pct
                })

            results.append({
                'cohort_month': acq_month,
                'cohort_size': initial_size,
                'retention_timeline': retention_row
            })

        return results
