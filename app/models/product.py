from datetime import datetime, timezone
import json
from app.extensions import db


class Product(db.Model):
    """Core product entity with specification attributes, pricing, ratings, and search metadata."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    slug = db.Column(db.String(280), unique=True, nullable=False, index=True)
    brand = db.Column(db.String(100), nullable=False, index=True)
    model_number = db.Column(db.String(100), nullable=True)
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    
    short_description = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Financial fields
    base_price = db.Column(db.Float, nullable=False, index=True)
    sale_price = db.Column(db.Float, nullable=False, index=True)
    cost_price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, default=0.0, nullable=False)
    
    # Physical and logistics specs
    weight_kg = db.Column(db.Float, default=1.0, nullable=False)
    dimensions_cm = db.Column(db.String(100), nullable=True)
    warranty_months = db.Column(db.Integer, default=12, nullable=False)
    
    # Stats
    average_rating = db.Column(db.Float, default=0.0, nullable=False, index=True)
    total_reviews_count = db.Column(db.Integer, default=0, nullable=False)
    views_count = db.Column(db.Integer, default=0, nullable=False)
    purchases_count = db.Column(db.Integer, default=0, nullable=False)
    wishlist_count = db.Column(db.Integer, default=0, nullable=False)
    
    # AI and Semantic metadata
    target_usage = db.Column(db.String(200), nullable=True)
    key_features = db.Column(db.Text, nullable=True, default='[]')
    compatibility_tags = db.Column(db.Text, nullable=True, default='[]')
    aspect_sentiment_summary = db.Column(db.Text, nullable=True, default='{}')
    
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    is_featured = db.Column(db.Boolean, default=False, nullable=False, index=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    category = db.relationship('Category', back_populates='products')
    seller = db.relationship('SellerProfile', back_populates='products')
    attributes = db.relationship('ProductAttribute', back_populates='product', cascade='all, delete-orphan', lazy='dynamic')
    images = db.relationship('ProductImage', back_populates='product', cascade='all, delete-orphan', lazy='dynamic')
    inventory = db.relationship('ProductInventory', back_populates='product', uselist=False, cascade='all, delete-orphan')
    price_history = db.relationship('ProductPriceHistory', back_populates='product', cascade='all, delete-orphan', lazy='dynamic')
    reviews = db.relationship('Review', back_populates='product', cascade='all, delete-orphan', lazy='dynamic')
    cart_items = db.relationship('CartItem', back_populates='product', lazy='dynamic')
    order_items = db.relationship('OrderItem', back_populates='product', lazy='dynamic')
    performance_score = db.relationship('ProductPerformanceScore', back_populates='product', uselist=False, cascade='all, delete-orphan')
    forecasts = db.relationship('DemandForecast', back_populates='product', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def current_price(self):
        return self.sale_price if self.sale_price and self.sale_price < self.base_price else self.base_price

    @property
    def primary_image_url(self):
        try:
            primary = self.images.filter_by(is_primary=True).first()
            if primary:
                return primary.image_url
            first = self.images.first()
            return first.image_url if first else '/static/img/placeholder.svg'
        except Exception:
            return '/static/img/placeholder.svg'

    def get_key_features_list(self):
        try:
            return json.loads(self.key_features or '[]')
        except Exception:
            return []

    def set_key_features_list(self, features):
        self.key_features = json.dumps(features if isinstance(features, list) else [])

    def get_compatibility_tags_list(self):
        try:
            return json.loads(self.compatibility_tags or '[]')
        except Exception:
            return []

    def set_compatibility_tags_list(self, tags):
        self.compatibility_tags = json.dumps(tags if isinstance(tags, list) else [])

    def get_aspect_sentiment_dict(self):
        try:
            return json.loads(self.aspect_sentiment_summary or '{}')
        except Exception:
            return {}

    def to_dict(self, detailed=False):
        data = {
            'id': self.id,
            'sku': self.sku,
            'title': self.title,
            'slug': self.slug,
            'brand': self.brand,
            'model_number': self.model_number,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'category_slug': self.category.slug if self.category else None,
            'seller_id': self.seller_id,
            'seller_name': self.seller.business_name if self.seller else None,
            'short_description': self.short_description,
            'base_price': round(self.base_price, 2),
            'sale_price': round(self.sale_price, 2),
            'current_price': round(self.current_price, 2),
            'discount_percentage': round(self.discount_percentage or 0.0, 1),
            'weight_kg': self.weight_kg,
            'warranty_months': self.warranty_months,
            'average_rating': round(self.average_rating or 0.0, 2),
            'total_reviews_count': self.total_reviews_count,
            'views_count': self.views_count,
            'purchases_count': self.purchases_count,
            'target_usage': self.target_usage,
            'key_features': self.get_key_features_list(),
            'compatibility_tags': self.get_compatibility_tags_list(),
            'aspect_sentiments': self.get_aspect_sentiment_dict(),
            'primary_image_url': self.primary_image_url,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'stock_quantity': self.inventory.available_quantity if self.inventory else 0,
            'in_stock': (self.inventory.available_quantity > 0) if self.inventory else False
        }
        if detailed:
            data['description'] = self.description
            data['dimensions_cm'] = self.dimensions_cm
            data['attributes'] = [attr.to_dict() for attr in self.attributes.all()]
            data['images'] = [img.to_dict() for img in self.images.all()]
        return data


class ProductAttribute(db.Model):
    """Dynamic key-value technical specifications for products."""
    __tablename__ = 'product_attributes'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    attribute_group = db.Column(db.String(100), default='General', nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    value = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(30), nullable=True)
    is_filterable = db.Column(db.Boolean, default=True, nullable=False)
    is_key_spec = db.Column(db.Boolean, default=False, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)

    product = db.relationship('Product', back_populates='attributes')

    def to_dict(self):
        return {
            'id': self.id,
            'attribute_group': self.attribute_group,
            'name': self.name,
            'value': self.value,
            'unit': self.unit,
            'is_key_spec': self.is_key_spec
        }


class ProductImage(db.Model):
    """Product gallery image records with ordering and primary flags."""
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    image_url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(255), nullable=True)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    product = db.relationship('Product', back_populates='images')

    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'alt_text': self.alt_text,
            'is_primary': self.is_primary,
            'display_order': self.display_order
        }
