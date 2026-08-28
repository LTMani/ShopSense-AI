from app.services.recommendation_service import RecommendationService
from app.services.comparison_service import ComparisonService
from app.models.product import Product


def test_smart_alternatives(app):
    with app.app_context():
        rec_svc = RecommendationService()
        product = Product.query.filter_by(is_active=True).first()
        alts = rec_svc.get_smart_alternatives(product.id)
        assert 'budget_alternatives' in alts
        assert 'premium_upgrades' in alts


def test_product_comparison(app):
    with app.app_context():
        comp_svc = ComparisonService()
        prods = Product.query.filter_by(is_active=True).limit(2).all()
        pids = [p.id for p in prods]

        res = comp_svc.compare_products(pids)
        assert len(res['products']) == 2
        assert 'attributes_matrix' in res
        assert 'aspects_matrix' in res
        assert len(res['verdict']) > 0
