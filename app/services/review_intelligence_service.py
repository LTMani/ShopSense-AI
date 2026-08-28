import json
from typing import Dict, Any, List
from app.models.review import Review, ReviewAspectRating
from app.repositories.review_repository import ReviewRepository
from app.repositories.product_repository import ProductRepository
from app.ai.nlp.sentiment_analyzer import AspectSentimentAnalyzer
from app.extensions import db


class ReviewIntelligenceService:
    """Processes customer feedback into aspect ratings, praise/complaint summaries, and sentiment metrics."""

    def __init__(self):
        self.review_repo = ReviewRepository()
        self.product_repo = ProductRepository()

    def add_review(self, product_id: int, user_id: int, rating: int, title: str, content: str) -> Dict[str, Any]:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        # Analyze NLP aspect sentiment
        nlp_result = AspectSentimentAnalyzer.analyze_review(f"{title}. {content}")

        review = Review(
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            title=title.strip(),
            content=content.strip(),
            sentiment_polarity=nlp_result['polarity'],
            sentiment_label=nlp_result['label']
        )
        review.set_praises_list(nlp_result['praises'])
        review.set_complaints_list(nlp_result['complaints'])
        db.session.add(review)
        db.session.flush()

        # Add aspect ratings
        for aspect_name, asp_data in nlp_result['aspect_ratings'].items():
            aspect_rating = ReviewAspectRating(
                review_id=review.id,
                aspect_name=aspect_name,
                sentiment_score=asp_data['score'],
                sentiment_label=asp_data['label']
            )
            db.session.add(aspect_rating)

        # Update product aggregate ratings
        all_reviews = Review.query.filter_by(product_id=product_id).all()
        product.total_reviews_count = len(all_reviews)
        product.average_rating = round(sum(r.rating for r in all_reviews) / len(all_reviews), 2)

        # Update product aspect sentiment summary cache
        aspect_breakdown = self.review_repo.get_aspect_breakdown_for_product(product_id)
        aspect_dict = {k: int(v['average_score']) for k, v in aspect_breakdown.items()}
        product.aspect_sentiment_summary = json.dumps(aspect_dict)

        db.session.commit()
        return review.to_dict()

    def get_review_intelligence(self, product_id: int) -> Dict[str, Any]:
        reviews = self.review_repo.get_by_product(product_id)
        aspect_breakdown = self.review_repo.get_aspect_breakdown_for_product(product_id)

        all_praises = []
        all_complaints = []
        for r in reviews:
            all_praises.extend(r.get_praises_list())
            all_complaints.extend(r.get_complaints_list())

        return {
            'total_reviews': len(reviews),
            'aspect_breakdown': aspect_breakdown,
            'top_praises': list(dict.fromkeys(all_praises))[:5],
            'top_complaints': list(dict.fromkeys(all_complaints))[:5],
            'reviews': [r.to_dict() for r in reviews]
        }
