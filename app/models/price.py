from datetime import datetime, timezone
from app.extensions import db


class ProductPriceHistory(db.Model):
    """Historical record of price fluctuations for elasticity modeling and price-drop alerts."""
    __tablename__ = 'product_price_histories'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    base_price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    effective_price = db.Column(db.Float, nullable=False)
    change_reason = db.Column(db.String(100), default='regular_update', nullable=False)
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    product = db.relationship('Product', back_populates='price_history')

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'base_price': round(self.base_price, 2),
            'sale_price': round(self.sale_price, 2),
            'effective_price': round(self.effective_price, 2),
            'change_reason': self.change_reason,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }


class PricePromotionRule(db.Model):
    """Seller dynamic pricing and discount rule."""
    __tablename__ = 'price_promotion_rules'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False)
    discount_value = db.Column(db.Float, nullable=False)
    minimum_order_value = db.Column(db.Float, default=0.0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    starts_at = db.Column(db.DateTime, nullable=True)
    ends_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'seller_id': self.seller_id,
            'name': self.name,
            'rule_type': self.rule_type,
            'discount_value': self.discount_value,
            'is_active': self.is_active,
            'starts_at': self.starts_at.isoformat() if self.starts_at else None,
            'ends_at': self.ends_at.isoformat() if self.ends_at else None
        }
