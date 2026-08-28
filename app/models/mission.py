from datetime import datetime, timezone
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
