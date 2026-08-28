from datetime import datetime, timezone, date
import json
from app.extensions import db


class SellerMetricDaily(db.Model):
    """Daily aggregated commercial metrics for sellers calculated dynamically from order events."""
    __tablename__ = 'seller_metrics_daily'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    metric_date = db.Column(db.Date, nullable=False, index=True)
    
    total_revenue = db.Column(db.Float, default=0.0, nullable=False)
    gross_profit = db.Column(db.Float, default=0.0, nullable=False)
    total_orders = db.Column(db.Integer, default=0, nullable=False)
    units_sold = db.Column(db.Integer, default=0, nullable=False)
    page_views = db.Column(db.Integer, default=0, nullable=False)
    conversion_rate = db.Column(db.Float, default=0.0, nullable=False)
    average_order_value = db.Column(db.Float, default=0.0, nullable=False)
    returns_count = db.Column(db.Integer, default=0, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    seller = db.relationship('SellerProfile', back_populates='daily_metrics')

    def to_dict(self):
        return {
            'id': self.id,
            'seller_id': self.seller_id,
            'metric_date': self.metric_date.isoformat() if self.metric_date else None,
            'total_revenue': round(self.total_revenue, 2),
            'gross_profit': round(self.gross_profit, 2),
            'total_orders': self.total_orders,
            'units_sold': self.units_sold,
            'page_views': self.page_views,
            'conversion_rate': round(self.conversion_rate, 2),
            'average_order_value': round(self.average_order_value, 2),
            'returns_count': self.returns_count
        }


class CustomerSegment(db.Model):
    """Segment definition for customer cohort intelligence (RFM clustering)."""
    __tablename__ = 'customer_segments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    min_orders = db.Column(db.Integer, default=0, nullable=False)
    min_spend = db.Column(db.Float, default=0.0, nullable=False)
    recency_days_max = db.Column(db.Integer, default=365, nullable=False)
    recommended_strategy = db.Column(db.String(255), nullable=True)
    member_count = db.Column(db.Integer, default=0, nullable=False)
    average_spend = db.Column(db.Float, default=0.0, nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'recommended_strategy': self.recommended_strategy,
            'member_count': self.member_count,
            'average_spend': round(self.average_spend, 2)
        }


class ProductPerformanceScore(db.Model):
    """Consolidated product performance index based on traffic, conversion, margins, reviews, and returns."""
    __tablename__ = 'product_performance_scores'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    
    overall_score = db.Column(db.Float, default=50.0, nullable=False)
    sales_velocity_score = db.Column(db.Float, default=50.0, nullable=False)
    conversion_score = db.Column(db.Float, default=50.0, nullable=False)
    rating_sentiment_score = db.Column(db.Float, default=50.0, nullable=False)
    profitability_score = db.Column(db.Float, default=50.0, nullable=False)
    
    performance_grade = db.Column(db.String(10), default='B', nullable=False)
    is_dead_stock = db.Column(db.Boolean, default=False, nullable=False, index=True)
    days_since_last_sale = db.Column(db.Integer, default=0, nullable=False)
    action_recommendation = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    product = db.relationship('Product', back_populates='performance_score')

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_title': self.product.title if self.product else None,
            'overall_score': round(self.overall_score, 1),
            'sales_velocity_score': round(self.sales_velocity_score, 1),
            'conversion_score': round(self.conversion_score, 1),
            'rating_sentiment_score': round(self.rating_sentiment_score, 1),
            'profitability_score': round(self.profitability_score, 1),
            'performance_grade': self.performance_grade,
            'is_dead_stock': self.is_dead_stock,
            'days_since_last_sale': self.days_since_last_sale,
            'action_recommendation': self.action_recommendation
        }
