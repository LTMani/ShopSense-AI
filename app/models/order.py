from datetime import datetime, timezone
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
            'subtotal_amount': round(self.subtotal_amount or 0.0, 2),
            'discount_amount': round(self.discount_amount or 0.0, 2),
            'tax_amount': round(self.tax_amount or 0.0, 2),
            'shipping_fee': round(self.shipping_fee or 0.0, 2),
            'total_amount': round(self.total_amount or 0.0, 2),
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
