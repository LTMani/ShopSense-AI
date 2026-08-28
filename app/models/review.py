from datetime import datetime, timezone
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
