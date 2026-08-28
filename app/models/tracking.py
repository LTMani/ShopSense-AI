from datetime import datetime, timezone
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
