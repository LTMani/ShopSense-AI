from typing import Dict, Any, List
from app.models.analytics import CustomerSegment
from app.repositories.analytics_repository import CustomerSegmentRepository


class CustomerSegmentationService:
    """RFM (Recency, Frequency, Monetary) customer segmentation and cohort intelligence."""

    def __init__(self):
        self.segment_repo = CustomerSegmentRepository()

    def get_all_segments(self) -> List[Dict[str, Any]]:
        segments = self.segment_repo.get_all()
        if not segments:
            # Seed default RFM segments if not present
            defaults = [
                CustomerSegment(name='Champions', description='Bought recently, buy often, and spend the most.', recommended_strategy='Reward with exclusive early access and VIP perks.', member_count=18, average_spend=45200.0),
                CustomerSegment(name='Loyal Customers', description='Buy regularly and responsive to promotions.', recommended_strategy='Upsell premium tiers and request product reviews.', member_count=42, average_spend=28400.0),
                CustomerSegment(name='High Potential', description='Recent buyers with above-average spend.', recommended_strategy='Offer complementary accessories and membership programs.', member_count=35, average_spend=18500.0),
                CustomerSegment(name='At Risk', description='Purchased frequently in past but have lapsed in recent months.', recommended_strategy='Send win-back personalized price-drop campaigns.', member_count=22, average_spend=12000.0),
                CustomerSegment(name='Bargain Hunters', description='High price sensitivity, primarily buy during discounts.', recommended_strategy='Target with clearance sales and bundle discounts.', member_count=65, average_spend=6400.0),
                CustomerSegment(name='New Shoppers', description='First purchase made within the last 30 days.', recommended_strategy='Provide onboarding assistance and follow-up support.', member_count=50, average_spend=8900.0)
            ]
            self.segment_repo.bulk_create(defaults)
            segments = defaults

        return [s.to_dict() for s in segments]

    def get_customer_segments(self, seller_id: Any = None) -> List[Dict[str, Any]]:
        return self.get_all_segments()
