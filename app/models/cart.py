from datetime import datetime, timezone
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
