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
            if first:
                return first.image_url
        except Exception:
            pass

        # Intelligent category & brand specific high-definition image mapping
        title_lower = (self.title or '').lower()
        cat_lower = (self.category.name if self.category else '').lower()

        # 1. Audio & Headphones (Checked first to avoid 'phone' matching 'headphone')
        if 'airpods' in title_lower or 'buds' in title_lower or 'earbuds' in title_lower or 'wf-1000' in title_lower:
            return 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80'
        if 'wh-1000' in title_lower or 'headphone' in title_lower or 'accentum' in title_lower or 'sennheiser' in title_lower:
            return 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80'
        if 'speaker' in title_lower or 'marshall' in title_lower or 'jbl' in title_lower or 'soundbar' in title_lower:
            return 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&q=80'
        if 'audio' in cat_lower or 'headphone' in cat_lower or 'headset' in title_lower:
            return 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80'

        # 2. Laptops & Computers
        if 'macbook' in title_lower or ('apple' in title_lower and 'laptop' in cat_lower):
            return 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&q=80'
        if 'thinkpad' in title_lower or ('lenovo' in title_lower and 'laptop' in cat_lower):
            return 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&q=80'
        if 'dell' in title_lower or 'xps' in title_lower or 'inspiron' in title_lower:
            return 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&q=80'
        if 'rog' in title_lower or 'tuf' in title_lower or ('gaming' in title_lower and 'laptop' in cat_lower):
            return 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&q=80'
        if 'laptop' in cat_lower or 'computer' in cat_lower:
            return 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80'

        # 3. Smartphones & Tablets
        if 'iphone' in title_lower:
            return 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&q=80'
        if 'galaxy' in title_lower or 's24' in title_lower or 'nord' in title_lower:
            return 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&q=80'
        if 'ipad' in title_lower or 'tab' in title_lower or 'tablet' in cat_lower:
            return 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&q=80'
        if 'smartphone' in cat_lower:
            return 'https://images.unsplash.com/photo-1511707171634-5f897ff02560?w=800&q=80'

        # 4. Cameras
        if 'action' in title_lower or 'gopro' in title_lower or 'insta360' in title_lower:
            return 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&q=80'
        if 'pocket' in title_lower or 'gimbal' in title_lower or 'dji' in title_lower:
            return 'https://images.unsplash.com/photo-1587749091717-b7324c4e0952?w=800&q=80'
        if 'camera' in cat_lower or 'photography' in cat_lower or 'lens' in title_lower:
            return 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&q=80'

        # 5. Monitors & Displays
        if 'curved' in title_lower or 'ultrawide' in title_lower or 'odyssey' in title_lower or 'g9' in title_lower:
            return 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80'
        if 'monitor' in cat_lower or 'display' in cat_lower:
            return 'https://images.unsplash.com/photo-1547082299-de196ea013d6?w=800&q=80'

        # 6. Computer Peripherals
        if 'keyboard' in title_lower or 'keychron' in title_lower or 'tkl' in title_lower:
            return 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80'
        if 'mouse' in title_lower or 'deathadder' in title_lower or 'mx master' in title_lower:
            return 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=80'
        if 'dock' in title_lower or 'hub' in title_lower or 'stream deck' in title_lower:
            return 'https://images.unsplash.com/photo-1616440347437-b1c73416efc2?w=800&q=80'
        if 'peripheral' in cat_lower or 'webcam' in title_lower:
            return 'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=800&q=80'

        # 7. Smart Wearables
        if 'apple watch' in title_lower:
            return 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80'
        if 'garmin' in title_lower or 'forerunner' in title_lower or 'epix' in title_lower:
            return 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&q=80'
        if 'watch' in cat_lower or 'wearable' in cat_lower or 'band' in title_lower:
            return 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&q=80'

        # 8. Gaming & Consoles
        if 'playstation' in title_lower or 'ps5' in title_lower or 'dualsense' in title_lower:
            return 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&q=80'
        if 'xbox' in title_lower or 'controller' in title_lower:
            return 'https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=800&q=80'
        if 'switch' in title_lower or 'nintendo' in title_lower or 'ally' in title_lower:
            return 'https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=800&q=80'
        if 'console' in cat_lower or 'gaming' in cat_lower:
            return 'https://images.unsplash.com/photo-1622979135225-d2ba269bc1df?w=800&q=80'

        # 9. Office & Study Furniture
        if 'desk' in title_lower or 'table' in title_lower:
            return 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=800&q=80'
        if 'chair' in title_lower or 'ergosmart' in title_lower or 'featherlite' in title_lower:
            return 'https://images.unsplash.com/photo-1580481077111-2092c246f406?w=800&q=80'
        if 'furniture' in cat_lower:
            return 'https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=800&q=80'

        # 10. Smart Home & Appliances
        if 'light' in title_lower or 'philips' in title_lower or 'bulb' in title_lower:
            return 'https://images.unsplash.com/photo-1550985616-10810253b84d?w=800&q=80'
        if 'purifier' in title_lower or 'vacuum' in title_lower or 'dyson' in title_lower:
            return 'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&q=80'
        if 'echo' in title_lower or 'nest' in title_lower or 'hub' in title_lower:
            return 'https://images.unsplash.com/photo-1543512214-318c7553f230?w=800&q=80'
        if 'appliance' in cat_lower or 'smart home' in cat_lower:
            return 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80'

        return 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80'

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
