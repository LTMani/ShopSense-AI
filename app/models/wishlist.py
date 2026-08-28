from datetime import datetime, timezone
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

    @property
    def has_price_dropped(self):
        return self.price_drop_amount > 0

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
