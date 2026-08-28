from datetime import datetime, timezone
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
