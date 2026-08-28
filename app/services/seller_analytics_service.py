from datetime import date, datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy import func
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.analytics import SellerMetricDaily, ProductPerformanceScore
from app.repositories.analytics_repository import SellerMetricDailyRepository, ProductPerformanceRepository
from app.extensions import db


class SellerAnalyticsService:
    """Computes real-time dynamic analytics, revenue trends, conversion funnels, and performance grades."""

    def __init__(self):
        self.metrics_repo = SellerMetricDailyRepository()
        self.performance_repo = ProductPerformanceRepository()

    def get_seller_dashboard_kpis(self, seller_id: int) -> Dict[str, Any]:
        # 1. Total revenue and orders from real OrderItem records
        summary = db.session.query(
            func.count(OrderItem.id).label('total_units'),
            func.sum(OrderItem.total_price).label('total_revenue'),
            func.sum((OrderItem.unit_price - OrderItem.unit_cost) * OrderItem.quantity).label('total_profit')
        ).filter(OrderItem.seller_id == seller_id).first()

        total_units = int(summary.total_units or 0)
        total_revenue = float(summary.total_revenue or 0.0)
        total_profit = float(summary.total_profit or 0.0)

        # 2. Total active products count
        active_products = Product.query.filter_by(seller_id=seller_id, is_active=True).count()

        # 3. Aggregate 30-day trend
        daily_metrics = self.metrics_repo.get_latest_metrics(seller_id, days=30)
        
        revenue_trend = [
            {'date': m.metric_date.isoformat(), 'revenue': round(m.total_revenue, 2), 'orders': m.total_orders}
            for m in daily_metrics
        ]

        return {
            'total_revenue': round(total_revenue, 2),
            'total_profit': round(total_profit, 2),
            'units_sold': total_units,
            'active_products_count': active_products,
            'average_order_value': round(total_revenue / max(1, total_units), 2),
            'revenue_trend': revenue_trend
        }

    def get_product_performance_ranking(self, seller_id: int) -> List[Dict[str, Any]]:
        scores = self.performance_repo.filter_by(seller_id=seller_id)
        return [s.to_dict() for s in scores]
