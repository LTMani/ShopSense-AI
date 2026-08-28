from app.services.catalog_service import CatalogService
from app.services.search_service import SearchService


def test_catalog_categories_and_products(app):
    with app.app_context():
        catalog = CatalogService()
        categories = catalog.get_categories()
        assert len(categories) >= 8

        featured = catalog.get_featured_products(limit=5)
        assert len(featured) > 0


def test_natural_language_search(app):
    with app.app_context():
        search_svc = SearchService()
        # Search query with budget ceiling and keyword
        res = search_svc.search(query='laptop under 60000 coding')
        assert res['total'] > 0
        assert len(res['products']) > 0
        assert res['extracted_filters'].get('budget') == 60000.0
