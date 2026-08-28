from typing import Optional, List, Dict, Any
from sqlalchemy import func
from app.models.review import Review, ReviewAspectRating, ReviewHelpfulness
from app.repositories.base import BaseRepository
from app.extensions import db


class ReviewRepository(BaseRepository[Review]):
    def __init__(self):
        super().__init__(Review)

    def get_by_product(self, product_id: int, limit: int = 50) -> List[Review]:
        return Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).limit(limit).all()

    def get_by_user(self, user_id: int) -> List[Review]:
        return Review.query.filter_by(user_id=user_id).order_by(Review.created_at.desc()).all()

    def get_aspect_breakdown_for_product(self, product_id: int) -> Dict[str, Dict[str, Any]]:
        aspects = db.session.query(
            ReviewAspectRating.aspect_name,
            func.avg(ReviewAspectRating.sentiment_score).label('avg_score'),
            func.count(ReviewAspectRating.id).label('mention_count')
        ).join(Review).filter(Review.product_id == product_id).group_by(ReviewAspectRating.aspect_name).all()

        breakdown = {}
        for a in aspects:
            breakdown[a.aspect_name] = {
                'average_score': round(float(a.avg_score or 0.0) * 100, 1),
                'mention_count': a.mention_count,
                'sentiment': 'positive' if (a.avg_score or 0) >= 0.6 else ('neutral' if (a.avg_score or 0) >= 0.4 else 'negative')
            }
        return breakdown


class ReviewAspectRepository(BaseRepository[ReviewAspectRating]):
    def __init__(self):
        super().__init__(ReviewAspectRating)
