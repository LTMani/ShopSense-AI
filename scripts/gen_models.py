# ShopSense AI Models Generator
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'app' / 'models'
BASE.mkdir(parents=True, exist_ok=True)

# 1. user.py
(BASE / 'user.py').write_text('''from datetime import datetime, timezone
from flask_login import UserMixin
from app.extensions import db, bcrypt


class Role(db.Model):
    """User role definition for role-based access control (RBAC)."""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    users = db.relationship('User', back_populates='role', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description
        }


class User(UserMixin, db.Model):
    """Core user model representing customers, sellers, and administrators."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='RESTRICT'), nullable=False, index=True)
    
    last_login_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    role = db.relationship('Role', back_populates='users')
    customer_profile = db.relationship('CustomerProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    seller_profile = db.relationship('SellerProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    sessions = db.relationship('UserSession', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    orders = db.relationship('Order', back_populates='user', lazy='dynamic')
    reviews = db.relationship('Review', back_populates='user', lazy='dynamic')
    cart = db.relationship('Cart', back_populates='user', uselist=False, cascade='all, delete-orphan')
    wishlist = db.relationship('Wishlist', back_populates='user', uselist=False, cascade='all, delete-orphan')
    missions = db.relationship('ShoppingMission', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    conversations = db.relationship('Conversation', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    browsing_events = db.relationship('BrowsingEvent', back_populates='user', lazy='dynamic')
    search_history = db.relationship('SearchHistory', back_populates='user', lazy='dynamic')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_seller(self):
        return self.role and self.role.name == 'seller'

    @property
    def is_customer(self):
        return self.role and self.role.name == 'customer'

    @property
    def is_admin(self):
        return self.role and self.role.name == 'admin'

    def set_password(self, raw_password):
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    def to_dict(self, include_profile=False):
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'role': self.role.name if self.role else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_profile:
            if self.is_customer and self.customer_profile:
                data['customer_profile'] = self.customer_profile.to_dict()
            elif self.is_seller and self.seller_profile:
                data['seller_profile'] = self.seller_profile.to_dict()
        return data


class UserSession(db.Model):
    """User login session audit record for tracking activity and active tokens."""
    __tablename__ = 'user_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    session_token = db.Column(db.String(128), unique=True, nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_activity_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='sessions')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'is_active': self.is_active,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
''', encoding='utf-8')

# 2. profile.py
(BASE / 'profile.py').write_text('''from datetime import datetime, timezone
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
''', encoding='utf-8')

# 3. category.py
(BASE / 'category.py').write_text('''from datetime import datetime, timezone
from app.extensions import db


class Category(db.Model):
    """Hierarchical product category entity supporting nested catalog classification."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    icon_name = db.Column(db.String(50), default='package', nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Self-referential hierarchy
    parent = db.relationship('Category', remote_side=[id], backref=db.backref('children', lazy='dynamic'))
    products = db.relationship('Product', back_populates='category', lazy='dynamic')

    def to_dict(self, include_children=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'icon_name': self.icon_name,
            'image_url': self.image_url,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'display_order': self.display_order
        }
        if include_children:
            data['children'] = [child.to_dict() for child in self.children.filter_by(is_active=True).all()]
        return data
''', encoding='utf-8')

# 4. product.py
(BASE / 'product.py').write_text('''from datetime import datetime, timezone
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
        primary = self.images.filter_by(is_primary=True).first()
        if primary:
            return primary.image_url
        first = self.images.first()
        return first.image_url if first else '/static/img/placeholder.svg'

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
            'discount_percentage': round(self.discount_percentage, 1),
            'weight_kg': self.weight_kg,
            'warranty_months': self.warranty_months,
            'average_rating': round(self.average_rating, 2),
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
''', encoding='utf-8')

# 5. inventory.py
(BASE / 'inventory.py').write_text('''from datetime import datetime, timezone
from app.extensions import db


class ProductInventory(db.Model):
    """Real-time inventory levels, safety thresholds, reorder points, and lead time tracking."""
    __tablename__ = 'product_inventories'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    
    available_quantity = db.Column(db.Integer, default=0, nullable=False, index=True)
    reserved_quantity = db.Column(db.Integer, default=0, nullable=False)
    safety_stock = db.Column(db.Integer, default=10, nullable=False)
    reorder_point = db.Column(db.Integer, default=20, nullable=False)
    reorder_quantity = db.Column(db.Integer, default=50, nullable=False)
    supplier_lead_time_days = db.Column(db.Integer, default=7, nullable=False)
    unit_holding_cost = db.Column(db.Float, default=15.0, nullable=False)
    
    daily_sales_velocity = db.Column(db.Float, default=0.0, nullable=False)
    days_of_supply = db.Column(db.Float, default=999.0, nullable=False)
    stock_status = db.Column(db.String(30), default='in_stock', nullable=False)
    last_restocked_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    product = db.relationship('Product', back_populates='inventory')
    seller = db.relationship('SellerProfile', back_populates='inventory_items')
    transactions = db.relationship('InventoryTransaction', back_populates='inventory', cascade='all, delete-orphan', lazy='dynamic')
    alerts = db.relationship('InventoryAlert', back_populates='inventory', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def total_on_hand(self):
        return self.available_quantity + self.reserved_quantity

    def calculate_days_of_supply(self):
        if self.daily_sales_velocity <= 0.001:
            return 999.0
        return round(self.available_quantity / self.daily_sales_velocity, 1)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_title': self.product.title if self.product else None,
            'product_sku': self.product.sku if self.product else None,
            'seller_id': self.seller_id,
            'available_quantity': self.available_quantity,
            'reserved_quantity': self.reserved_quantity,
            'total_on_hand': self.total_on_hand,
            'safety_stock': self.safety_stock,
            'reorder_point': self.reorder_point,
            'reorder_quantity': self.reorder_quantity,
            'supplier_lead_time_days': self.supplier_lead_time_days,
            'daily_sales_velocity': round(self.daily_sales_velocity, 2),
            'days_of_supply': self.calculate_days_of_supply(),
            'stock_status': self.stock_status,
            'last_restocked_at': self.last_restocked_at.isoformat() if self.last_restocked_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class InventoryTransaction(db.Model):
    """Audit ledger for all stock adjustments, purchases, returns, and damages."""
    __tablename__ = 'inventory_transactions'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('product_inventories.id', ondelete='CASCADE'), nullable=False, index=True)
    transaction_type = db.Column(db.String(50), nullable=False)
    quantity_change = db.Column(db.Integer, nullable=False)
    quantity_after = db.Column(db.Integer, nullable=False)
    reference_id = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    inventory = db.relationship('ProductInventory', back_populates='transactions')

    def to_dict(self):
        return {
            'id': self.id,
            'inventory_id': self.inventory_id,
            'transaction_type': self.transaction_type,
            'quantity_change': self.quantity_change,
            'quantity_after': self.quantity_after,
            'reference_id': self.reference_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class InventoryAlert(db.Model):
    """Automated proactive notification for stockout risks, dead stock, and reorder triggers."""
    __tablename__ = 'inventory_alerts'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('product_inventories.id', ondelete='CASCADE'), nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), default='medium', nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    action_recommended = db.Column(db.String(255), nullable=True)
    is_resolved = db.Column(db.Boolean, default=False, nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    inventory = db.relationship('ProductInventory', back_populates='alerts')

    def to_dict(self):
        return {
            'id': self.id,
            'inventory_id': self.inventory_id,
            'product_title': self.inventory.product.title if self.inventory and self.inventory.product else None,
            'product_sku': self.inventory.product.sku if self.inventory and self.inventory.product else None,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'title': self.title,
            'message': self.message,
            'action_recommended': self.action_recommended,
            'is_resolved': self.is_resolved,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
''', encoding='utf-8')

# 6. price.py
(BASE / 'price.py').write_text('''from datetime import datetime, timezone
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
''', encoding='utf-8')

# 7. review.py
(BASE / 'review.py').write_text('''from datetime import datetime, timezone
import json
from app.extensions import db


class Review(db.Model):
    """Customer product review with overall score, verified purchase status, and AI aspect sentiments."""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_verified_purchase = db.Column(db.Boolean, default=True, nullable=False)
    
    sentiment_polarity = db.Column(db.Float, default=0.0, nullable=False)
    sentiment_label = db.Column(db.String(20), default='neutral', nullable=False)
    extracted_praises = db.Column(db.Text, nullable=True, default='[]')
    extracted_complaints = db.Column(db.Text, nullable=True, default='[]')
    
    helpful_votes = db.Column(db.Integer, default=0, nullable=False)
    unhelpful_votes = db.Column(db.Integer, default=0, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    product = db.relationship('Product', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
    aspect_ratings = db.relationship('ReviewAspectRating', back_populates='review', cascade='all, delete-orphan', lazy='dynamic')

    def get_praises_list(self):
        try:
            return json.loads(self.extracted_praises or '[]')
        except Exception:
            return []

    def set_praises_list(self, praises):
        self.extracted_praises = json.dumps(praises if isinstance(praises, list) else [])

    def get_complaints_list(self):
        try:
            return json.loads(self.extracted_complaints or '[]')
        except Exception:
            return []

    def set_complaints_list(self, complaints):
        self.extracted_complaints = json.dumps(complaints if isinstance(complaints, list) else [])

    def to_dict(self, include_aspects=True):
        data = {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else 'Verified Buyer',
            'rating': self.rating,
            'title': self.title,
            'content': self.content,
            'is_verified_purchase': self.is_verified_purchase,
            'sentiment_polarity': round(self.sentiment_polarity, 2),
            'sentiment_label': self.sentiment_label,
            'praises': self.get_praises_list(),
            'complaints': self.get_complaints_list(),
            'helpful_votes': self.helpful_votes,
            'unhelpful_votes': self.unhelpful_votes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_aspects:
            data['aspect_ratings'] = [a.to_dict() for a in self.aspect_ratings.all()]
        return data


class ReviewAspectRating(db.Model):
    """Aspect-level sentiment ratings (e.g., Battery: 88%, Sound: 92%, Build: 75%)."""
    __tablename__ = 'review_aspect_ratings'

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id', ondelete='CASCADE'), nullable=False, index=True)
    aspect_name = db.Column(db.String(60), nullable=False, index=True)
    sentiment_score = db.Column(db.Float, nullable=False)
    sentiment_label = db.Column(db.String(20), nullable=False)
    mention_snippet = db.Column(db.String(255), nullable=True)

    review = db.relationship('Review', back_populates='aspect_ratings')

    def to_dict(self):
        return {
            'id': self.id,
            'aspect_name': self.aspect_name,
            'sentiment_score': round(self.sentiment_score, 2),
            'sentiment_label': self.sentiment_label,
            'mention_snippet': self.mention_snippet
        }


class ReviewHelpfulness(db.Model):
    """Tracks unique user votes on review helpfulness."""
    __tablename__ = 'review_helpfulness'

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    is_helpful = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
''', encoding='utf-8')

# 8. cart.py
(BASE / 'cart.py').write_text('''from datetime import datetime, timezone
from app.extensions import db


class Cart(db.Model):
    """Customer active shopping cart with intelligent budget and compatibility checks."""
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='cart')
    items = db.relationship('CartItem', back_populates='cart', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def total_items_count(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal_amount(self):
        return sum(item.total_price for item in self.items.all())

    def to_dict(self, include_items=True):
        items_list = [item.to_dict() for item in self.items.all()] if include_items else []
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_items_count': self.total_items_count,
            'subtotal_amount': round(self.subtotal_amount, 2),
            'items': items_list,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class CartItem(db.Model):
    """Cart item record with product reference and quantity."""
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    cart = db.relationship('Cart', back_populates='items')
    product = db.relationship('Product', back_populates='cart_items')

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'unit_price': round(self.unit_price, 2),
            'total_price': round(self.total_price, 2),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
''', encoding='utf-8')

# 9. wishlist.py
(BASE / 'wishlist.py').write_text('''from datetime import datetime, timezone
from app.extensions import db


class Wishlist(db.Model):
    """Customer wishlist with intelligent price tracking and stock change alerts."""
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), default='My Wishlist', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='wishlist')
    items = db.relationship('WishlistItem', back_populates='wishlist', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def total_items_count(self):
        return self.items.count()

    def to_dict(self, include_items=True):
        items_list = [item.to_dict() for item in self.items.all()] if include_items else []
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'total_items_count': self.total_items_count,
            'items': items_list,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class WishlistItem(db.Model):
    """Individual saved product in wishlist with price-added record and target alert price."""
    __tablename__ = 'wishlist_items'

    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlists.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    price_when_added = db.Column(db.Float, nullable=False)
    target_alert_price = db.Column(db.Float, nullable=True)
    notify_on_price_drop = db.Column(db.Boolean, default=True, nullable=False)
    notify_on_back_in_stock = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    wishlist = db.relationship('Wishlist', back_populates='items')
    product = db.relationship('Product')

    @property
    def current_price(self):
        return self.product.current_price if self.product else self.price_when_added

    @property
    def price_drop_amount(self):
        if not self.product:
            return 0.0
        diff = self.price_when_added - self.product.current_price
        return max(0.0, diff)

    def to_dict(self):
        return {
            'id': self.id,
            'wishlist_id': self.wishlist_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'price_when_added': round(self.price_when_added, 2),
            'current_price': round(self.current_price, 2),
            'price_drop_amount': round(self.price_drop_amount, 2),
            'has_price_dropped': self.price_drop_amount > 0,
            'target_alert_price': self.target_alert_price,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
''', encoding='utf-8')

# 10. order.py
(BASE / 'order.py').write_text('''from datetime import datetime, timezone
import json
from app.extensions import db


class Order(db.Model):
    """Simulated internal commerce order with item lines, tax, shipping, and fulfillment lifecycle."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False, index=True)
    
    status = db.Column(db.String(40), default='pending', nullable=False, index=True)
    subtotal_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0, nullable=False)
    tax_amount = db.Column(db.Float, default=0.0, nullable=False)
    shipping_fee = db.Column(db.Float, default=0.0, nullable=False)
    total_amount = db.Column(db.Float, nullable=False, index=True)
    
    payment_method = db.Column(db.String(50), default='simulated_upi', nullable=False)
    payment_status = db.Column(db.String(30), default='paid', nullable=False)
    
    shipping_name = db.Column(db.String(150), nullable=False)
    shipping_phone = db.Column(db.String(30), nullable=True)
    shipping_address_line1 = db.Column(db.String(255), nullable=False)
    shipping_address_line2 = db.Column(db.String(255), nullable=True)
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_state = db.Column(db.String(100), nullable=False)
    shipping_postal_code = db.Column(db.String(20), nullable=False)
    shipping_country = db.Column(db.String(100), default='India', nullable=False)
    
    delivered_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan', lazy='dynamic')
    status_history = db.relationship('OrderStatusHistory', back_populates='order', cascade='all, delete-orphan', lazy='dynamic')

    def to_dict(self, include_items=True):
        data = {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'customer_name': self.user.full_name if self.user else self.shipping_name,
            'status': self.status,
            'subtotal_amount': round(self.subtotal_amount, 2),
            'discount_amount': round(self.discount_amount, 2),
            'tax_amount': round(self.tax_amount, 2),
            'shipping_fee': round(self.shipping_fee, 2),
            'total_amount': round(self.total_amount, 2),
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'shipping_address': {
                'name': self.shipping_name,
                'line1': self.shipping_address_line1,
                'city': self.shipping_city,
                'state': self.shipping_state,
                'postal_code': self.shipping_postal_code,
                'country': self.shipping_country
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.items.all()]
        return data


class OrderItem(db.Model):
    """Line item in a customer order with seller attribution and cost analysis."""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id', ondelete='RESTRICT'), nullable=False, index=True)
    
    product_title = db.Column(db.String(255), nullable=False)
    product_sku = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    unit_cost = db.Column(db.Float, default=0.0, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    item_status = db.Column(db.String(30), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')
    seller = db.relationship('SellerProfile')

    @property
    def gross_profit(self):
        return (self.unit_price - self.unit_cost) * self.quantity

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'seller_id': self.seller_id,
            'product_title': self.product_title,
            'product_sku': self.product_sku,
            'quantity': self.quantity,
            'unit_price': round(self.unit_price, 2),
            'unit_cost': round(self.unit_cost, 2),
            'total_price': round(self.total_price, 2),
            'gross_profit': round(self.gross_profit, 2),
            'item_status': self.item_status
        }


class OrderStatusHistory(db.Model):
    """Audit log for order lifecycle transitions."""
    __tablename__ = 'order_status_histories'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    status = db.Column(db.String(40), nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    order = db.relationship('Order', back_populates='status_history')
''', encoding='utf-8')

# 11. tracking.py
(BASE / 'tracking.py').write_text('''from datetime import datetime, timezone
import json
from app.extensions import db


class BrowsingEvent(db.Model):
    """Commerce behavioral event tracking product views, category browsing, and engagement time."""
    __tablename__ = 'browsing_events'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    session_id = db.Column(db.String(128), nullable=False, index=True)
    event_type = db.Column(db.String(50), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True, index=True)
    dwell_time_seconds = db.Column(db.Integer, default=0, nullable=False)
    metadata_payload = db.Column(db.Text, nullable=True, default='{}')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = db.relationship('User', back_populates='browsing_events')
    product = db.relationship('Product')
    category = db.relationship('Category')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'product_id': self.product_id,
            'category_id': self.category_id,
            'dwell_time_seconds': self.dwell_time_seconds,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SearchHistory(db.Model):
    """Search query logs with result counts, clicked products, and search intent tokens."""
    __tablename__ = 'search_histories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    session_id = db.Column(db.String(128), nullable=False, index=True)
    raw_query = db.Column(db.String(255), nullable=False, index=True)
    extracted_intent = db.Column(db.String(100), nullable=True)
    extracted_category = db.Column(db.String(100), nullable=True)
    extracted_budget = db.Column(db.Float, nullable=True)
    results_count = db.Column(db.Integer, default=0, nullable=False)
    clicked_product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = db.relationship('User', back_populates='search_history')

    def to_dict(self):
        return {
            'id': self.id,
            'raw_query': self.raw_query,
            'results_count': self.results_count,
            'extracted_intent': self.extracted_intent,
            'extracted_budget': self.extracted_budget,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ProductComparison(db.Model):
    """Side-by-side product comparison session log."""
    __tablename__ = 'product_comparisons'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    session_id = db.Column(db.String(128), nullable=False, index=True)
    product_ids = db.Column(db.Text, nullable=False)
    winning_product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET NULL'), nullable=True)
    ai_verdict = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def get_product_ids_list(self):
        try:
            return json.loads(self.product_ids or '[]')
        except Exception:
            return []
''', encoding='utf-8')

# 12. mission.py
(BASE / 'mission.py').write_text('''from datetime import datetime, timezone
import json
from app.extensions import db


class ShoppingMission(db.Model):
    """Multi-product basket goal builder (e.g. 'Build college study setup under ₹30,000')."""
    __tablename__ = 'shopping_missions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    mission_prompt = db.Column(db.Text, nullable=False)
    target_budget = db.Column(db.Float, nullable=False)
    allocated_total = db.Column(db.Float, default=0.0, nullable=False)
    savings_amount = db.Column(db.Float, default=0.0, nullable=False)
    
    status = db.Column(db.String(30), default='draft', nullable=False)
    optimization_mode = db.Column(db.String(40), default='balanced', nullable=False)
    ai_rationale = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='missions')
    items = db.relationship('ShoppingMissionItem', back_populates='mission', cascade='all, delete-orphan', lazy='dynamic')

    def to_dict(self, include_items=True):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'mission_prompt': self.mission_prompt,
            'target_budget': round(self.target_budget, 2),
            'allocated_total': round(self.allocated_total, 2),
            'savings_amount': round(self.savings_amount, 2),
            'status': self.status,
            'optimization_mode': self.optimization_mode,
            'ai_rationale': self.ai_rationale,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.items.all()]
        return data


class ShoppingMissionItem(db.Model):
    """Product slot in a shopping mission basket with role and rationale."""
    __tablename__ = 'shopping_mission_items'

    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('shopping_missions.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False, index=True)
    slot_role = db.Column(db.String(80), nullable=False)
    assigned_budget = db.Column(db.Float, nullable=False)
    actual_price = db.Column(db.Float, nullable=False)
    selection_rationale = db.Column(db.String(255), nullable=True)
    is_essential = db.Column(db.Boolean, default=True, nullable=False)
    is_selected = db.Column(db.Boolean, default=True, nullable=False)

    mission = db.relationship('ShoppingMission', back_populates='items')
    product = db.relationship('Product')

    def to_dict(self):
        return {
            'id': self.id,
            'mission_id': self.mission_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'slot_role': self.slot_role,
            'assigned_budget': round(self.assigned_budget, 2),
            'actual_price': round(self.actual_price, 2),
            'selection_rationale': self.selection_rationale,
            'is_essential': self.is_essential,
            'is_selected': self.is_selected
        }
''', encoding='utf-8')

# 13. conversation.py
(BASE / 'conversation.py').write_text('''from datetime import datetime, timezone
import json
from app.extensions import db


class Conversation(db.Model):
    """Chat session for AI Customer Shopping Copilot or Seller Intelligence Copilot."""
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    copilot_type = db.Column(db.String(30), default='customer_shopping', nullable=False, index=True)
    session_title = db.Column(db.String(150), default='New Shopping Assistant Session', nullable=False)
    context_state = db.Column(db.Text, nullable=True, default='{}')
    is_archived = db.Column(db.Boolean, default=False, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='conversations')
    messages = db.relationship('ConversationMessage', back_populates='conversation', cascade='all, delete-orphan', lazy='dynamic')

    def get_context_dict(self):
        try:
            return json.loads(self.context_state or '{}')
        except Exception:
            return {}

    def set_context_dict(self, context_dict):
        self.context_state = json.dumps(context_dict if isinstance(context_dict, dict) else {})

    def to_dict(self, include_messages=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'copilot_type': self.copilot_type,
            'session_title': self.session_title,
            'context': self.get_context_dict(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_messages:
            data['messages'] = [m.to_dict() for m in self.messages.order_by(ConversationMessage.created_at.asc()).all()]
        return data


class ConversationMessage(db.Model):
    """Single message entry in AI conversation with structured recommendation payload."""
    __tablename__ = 'conversation_messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False, index=True)
    sender = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    extracted_requirements = db.Column(db.Text, nullable=True, default='{}')
    recommended_product_ids = db.Column(db.Text, nullable=True, default='[]')
    explanation_text = db.Column(db.Text, nullable=True)
    confidence_score = db.Column(db.Float, default=1.0, nullable=False)
    latency_ms = db.Column(db.Integer, default=0, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    conversation = db.relationship('Conversation', back_populates='messages')

    def get_extracted_requirements_dict(self):
        try:
            return json.loads(self.extracted_requirements or '{}')
        except Exception:
            return {}

    def get_recommended_product_ids_list(self):
        try:
            return json.loads(self.recommended_product_ids or '[]')
        except Exception:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender': self.sender,
            'content': self.content,
            'extracted_requirements': self.get_extracted_requirements_dict(),
            'recommended_product_ids': self.get_recommended_product_ids_list(),
            'explanation_text': self.explanation_text,
            'confidence_score': round(self.confidence_score, 2),
            'latency_ms': self.latency_ms,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AIInteractionLog(db.Model):
    """Audit log for telemetry on AI latency, token usage, model accuracy, and fallback rates."""
    __tablename__ = 'ai_interaction_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    feature = db.Column(db.String(60), nullable=False, index=True)
    provider = db.Column(db.String(40), nullable=False)
    model_name = db.Column(db.String(80), nullable=False)
    prompt_tokens = db.Column(db.Integer, default=0, nullable=False)
    completion_tokens = db.Column(db.Integer, default=0, nullable=False)
    latency_ms = db.Column(db.Integer, default=0, nullable=False)
    success = db.Column(db.Boolean, default=True, nullable=False)
    error_message = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
''', encoding='utf-8')

# 14. forecast.py
(BASE / 'forecast.py').write_text('''from datetime import datetime, timezone
import json
from app.extensions import db


class DemandForecast(db.Model):
    """Time-series demand forecast projection generated by historical sales models."""
    __tablename__ = 'demand_forecasts'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    
    forecast_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    horizon_days = db.Column(db.Integer, default=14, nullable=False)
    forecast_model = db.Column(db.String(50), default='holt_winters_hybrid', nullable=False)
    
    current_stock = db.Column(db.Integer, nullable=False)
    predicted_demand_total = db.Column(db.Integer, nullable=False)
    predicted_daily_rate = db.Column(db.Float, nullable=False)
    confidence_interval_low = db.Column(db.Integer, nullable=False)
    confidence_interval_high = db.Column(db.Integer, nullable=False)
    
    stockout_predicted = db.Column(db.Boolean, default=False, nullable=False)
    estimated_days_to_stockout = db.Column(db.Float, nullable=True)
    recommended_reorder_qty = db.Column(db.Integer, default=0, nullable=False)
    daily_projections = db.Column(db.Text, nullable=False, default='[]')
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    product = db.relationship('Product', back_populates='forecasts')
    seller = db.relationship('SellerProfile')

    def get_daily_projections_list(self):
        try:
            return json.loads(self.daily_projections or '[]')
        except Exception:
            return []

    def set_daily_projections_list(self, projections):
        self.daily_projections = json.dumps(projections if isinstance(projections, list) else [])

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_title': self.product.title if self.product else None,
            'product_sku': self.product.sku if self.product else None,
            'seller_id': self.seller_id,
            'forecast_date': self.forecast_date.isoformat() if self.forecast_date else None,
            'horizon_days': self.horizon_days,
            'forecast_model': self.forecast_model,
            'current_stock': self.current_stock,
            'predicted_demand_total': self.predicted_demand_total,
            'predicted_daily_rate': round(self.predicted_daily_rate, 2),
            'confidence_interval_low': self.confidence_interval_low,
            'confidence_interval_high': self.confidence_interval_high,
            'stockout_predicted': self.stockout_predicted,
            'estimated_days_to_stockout': self.estimated_days_to_stockout,
            'recommended_reorder_qty': self.recommended_reorder_qty,
            'daily_projections': self.get_daily_projections_list()
        }


class ForecastEvaluation(db.Model):
    """Backtesting accuracy evaluation metrics (MAPE, RMSE, MAE) for forecasting models."""
    __tablename__ = 'forecast_evaluations'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    model_name = db.Column(db.String(50), nullable=False)
    mape = db.Column(db.Float, nullable=False)
    rmse = db.Column(db.Float, nullable=False)
    mae = db.Column(db.Float, nullable=False)
    sample_points = db.Column(db.Integer, nullable=False)
    evaluated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
''', encoding='utf-8')

# 15. analytics.py
(BASE / 'analytics.py').write_text('''from datetime import datetime, timezone, date
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
''', encoding='utf-8')

# 16. audit.py
(BASE / 'audit.py').write_text('''from datetime import datetime, timezone
from app.extensions import db


class AuditLog(db.Model):
    """System-wide security and operational audit trail."""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    action = db.Column(db.String(100), nullable=False, index=True)
    entity_type = db.Column(db.String(60), nullable=True)
    entity_id = db.Column(db.String(60), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SystemSetting(db.Model):
    """Configurable system runtime settings and platform toggles."""
    __tablename__ = 'system_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    data_type = db.Column(db.String(20), default='string', nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def get_typed_value(self):
        if self.data_type == 'integer':
            return int(self.value)
        elif self.data_type == 'float':
            return float(self.value)
        elif self.data_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes')
        return self.value
''', encoding='utf-8')

# 17. __init__.py
(BASE / '__init__.py').write_text('''from app.models.user import User, Role, UserSession
from app.models.profile import CustomerProfile, SellerProfile
from app.models.category import Category
from app.models.product import Product, ProductAttribute, ProductImage
from app.models.inventory import ProductInventory, InventoryTransaction, InventoryAlert
from app.models.price import ProductPriceHistory, PricePromotionRule
from app.models.review import Review, ReviewAspectRating, ReviewHelpfulness
from app.models.cart import Cart, CartItem
from app.models.wishlist import Wishlist, WishlistItem
from app.models.order import Order, OrderItem, OrderStatusHistory
from app.models.tracking import BrowsingEvent, SearchHistory, ProductComparison
from app.models.mission import ShoppingMission, ShoppingMissionItem
from app.models.conversation import Conversation, ConversationMessage, AIInteractionLog
from app.models.forecast import DemandForecast, ForecastEvaluation
from app.models.analytics import SellerMetricDaily, CustomerSegment, ProductPerformanceScore
from app.models.audit import AuditLog, SystemSetting

__all__ = [
    'User',
    'Role',
    'UserSession',
    'CustomerProfile',
    'SellerProfile',
    'Category',
    'Product',
    'ProductAttribute',
    'ProductImage',
    'ProductInventory',
    'InventoryTransaction',
    'InventoryAlert',
    'ProductPriceHistory',
    'PricePromotionRule',
    'Review',
    'ReviewAspectRating',
    'ReviewHelpfulness',
    'Cart',
    'CartItem',
    'Wishlist',
    'WishlistItem',
    'Order',
    'OrderItem',
    'OrderStatusHistory',
    'BrowsingEvent',
    'SearchHistory',
    'ProductComparison',
    'ShoppingMission',
    'ShoppingMissionItem',
    'Conversation',
    'ConversationMessage',
    'AIInteractionLog',
    'DemandForecast',
    'ForecastEvaluation',
    'SellerMetricDaily',
    'CustomerSegment',
    'ProductPerformanceScore',
    'AuditLog',
    'SystemSetting'
]
''', encoding='utf-8')

print('All 17 model modules written successfully!')
