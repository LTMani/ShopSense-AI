from datetime import datetime, timezone
import json
from app.extensions import db


class CustomerProfile(db.Model):
    """Customer behavioral preferences, demographics, and personalization metadata."""
    __tablename__ = 'customer_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    
    preferred_categories = db.Column(db.Text, nullable=True, default='[]')
    budget_tier = db.Column(db.String(30), default='balanced', nullable=False)
    price_sensitivity_score = db.Column(db.Float, default=0.5, nullable=False)
    primary_usage = db.Column(db.String(100), nullable=True)
    preferred_brands = db.Column(db.Text, nullable=True, default='[]')
    
    shipping_address_line1 = db.Column(db.String(255), nullable=True)
    shipping_address_line2 = db.Column(db.String(255), nullable=True)
    shipping_city = db.Column(db.String(100), nullable=True)
    shipping_state = db.Column(db.String(100), nullable=True)
    shipping_postal_code = db.Column(db.String(20), nullable=True)
    shipping_country = db.Column(db.String(100), default='India', nullable=False)
    
    rfm_segment = db.Column(db.String(50), default='New Customer', nullable=False)
    lifetime_spend = db.Column(db.Float, default=0.0, nullable=False)
    total_orders_count = db.Column(db.Integer, default=0, nullable=False)
    total_reviews_count = db.Column(db.Integer, default=0, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='customer_profile')

    def get_preferred_categories_list(self):
        try:
            return json.loads(self.preferred_categories or '[]')
        except Exception:
            return []

    def set_preferred_categories_list(self, categories):
        self.preferred_categories = json.dumps(categories if isinstance(categories, list) else [])

    def get_preferred_brands_list(self):
        try:
            return json.loads(self.preferred_brands or '[]')
        except Exception:
            return []

    def set_preferred_brands_list(self, brands):
        self.preferred_brands = json.dumps(brands if isinstance(brands, list) else [])

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'preferred_categories': self.get_preferred_categories_list(),
            'budget_tier': self.budget_tier,
            'price_sensitivity_score': self.price_sensitivity_score,
            'primary_usage': self.primary_usage,
            'preferred_brands': self.get_preferred_brands_list(),
            'shipping_city': self.shipping_city,
            'shipping_state': self.shipping_state,
            'shipping_postal_code': self.shipping_postal_code,
            'shipping_country': self.shipping_country,
            'rfm_segment': self.rfm_segment,
            'lifetime_spend': round(self.lifetime_spend, 2),
            'total_orders_count': self.total_orders_count,
            'total_reviews_count': self.total_reviews_count
        }


class SellerProfile(db.Model):
    """Seller business profile, store configuration, ratings, and operational status."""
    __tablename__ = 'seller_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    
    business_name = db.Column(db.String(150), nullable=False, index=True)
    store_slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    store_description = db.Column(db.Text, nullable=True)
    tax_identifier = db.Column(db.String(50), nullable=True)
    business_phone = db.Column(db.String(30), nullable=True)
    business_email = db.Column(db.String(255), nullable=True)
    
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), default='India', nullable=False)
    
    average_rating = db.Column(db.Float, default=0.0, nullable=False)
    total_ratings_count = db.Column(db.Integer, default=0, nullable=False)
    is_verified_seller = db.Column(db.Boolean, default=True, nullable=False)
    commission_rate = db.Column(db.Float, default=0.08, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='seller_profile')
    products = db.relationship('Product', back_populates='seller', lazy='dynamic', cascade='all, delete-orphan')
    inventory_items = db.relationship('ProductInventory', back_populates='seller', lazy='dynamic')
    daily_metrics = db.relationship('SellerMetricDaily', back_populates='seller', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'store_slug': self.store_slug,
            'store_description': self.store_description,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'average_rating': round(self.average_rating, 2),
            'total_ratings_count': self.total_ratings_count,
            'is_verified_seller': self.is_verified_seller,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
