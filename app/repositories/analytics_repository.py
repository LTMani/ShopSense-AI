from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta, timezone
from sqlalchemy import func
from app.models.analytics import SellerMetricDaily, CustomerSegment, ProductPerformanceScore
from app.repositories.base import BaseRepository
from app.extensions import db


class SellerMetricDailyRepository(BaseRepository[SellerMetricDaily]):
    def __init__(self):
        super().__init__(SellerMetricDaily)

    def get_metrics_range(self, seller_id: int, start_date: date, end_date: date) -> List[SellerMetricDaily]:
        return SellerMetricDaily.query.filter(
            SellerMetricDaily.seller_id == seller_id,
            SellerMetricDaily.metric_date >= start_date,
            SellerMetricDaily.metric_date <= end_date
        ).order_by(SellerMetricDaily.metric_date.asc()).all()

    def get_latest_metrics(self, seller_id: int, days: int = 30) -> List[SellerMetricDaily]:
        start = date.today() - timedelta(days=days)
        return SellerMetricDaily.query.filter(
            SellerMetricDaily.seller_id == seller_id,
            SellerMetricDaily.metric_date >= start
        ).order_by(SellerMetricDaily.metric_date.asc()).all()


class CustomerSegmentRepository(BaseRepository[CustomerSegment]):
    def __init__(self):
        super().__init__(CustomerSegment)


class ProductPerformanceRepository(BaseRepository[ProductPerformanceScore]):
    def __init__(self):
        super().__init__(ProductPerformanceScore)

    def get_dead_stock(self, seller_id: Optional[int] = None) -> List[ProductPerformanceScore]:
        query = ProductPerformanceScore.query.filter_by(is_dead_stock=True)
        if seller_id:
            query = query.filter_by(seller_id=seller_id)
        return query.order_by(ProductPerformanceScore.overall_score.asc()).all()

    def get_top_performers(self, seller_id: Optional[int] = None, limit: int = 10) -> List[ProductPerformanceScore]:
        query = ProductPerformanceScore.query
        if seller_id:
            query = query.filter_by(seller_id=seller_id)
        return query.order_by(ProductPerformanceScore.overall_score.desc()).limit(limit).all()
