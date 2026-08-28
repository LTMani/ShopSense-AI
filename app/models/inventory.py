from datetime import datetime, timezone
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
