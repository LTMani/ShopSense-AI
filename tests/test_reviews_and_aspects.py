from app.services.review_intelligence_service import ReviewIntelligenceService
from app.models.product import Product
from app.models.user import User


def test_review_aspect_sentiment_extraction(app):
    with app.app_context():
        rev_svc = ReviewIntelligenceService()
        product = Product.query.filter_by(is_active=True).first()
        user = User.query.filter_by(email='customer@shopsense.ai').first()

        review = rev_svc.add_review(
            product_id=product.id,
            user_id=user.id,
            rating=5,
            title="Superb battery backup and crystal sound!",
            content="The battery lasts over 12 hours easily. Audio is crisp with great deep bass. Very comfortable."
        )

        assert review['sentiment_label'] == 'positive'
        assert review['sentiment_polarity'] > 0.0

        intel = rev_svc.get_review_intelligence(product.id)
        assert 'aspect_breakdown' in intel
        assert intel['total_reviews'] > 0
