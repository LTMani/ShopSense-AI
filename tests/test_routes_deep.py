import pytest


class TestRoutesDeepSuite:
    """Comprehensive test matrix covering all Flask web views and API response status codes."""

    def test_marketplace_public_pages(self, client):
        public_endpoints = [
            '/',
            '/products',
            '/search?q=headphones',
            '/compare',
            '/copilot',
            '/login',
            '/register',
            '/seller/register',
            '/settings',
            '/health'
        ]
        for ep in public_endpoints:
            res = client.get(ep)
            assert res.status_code == 200, f"Failed on endpoint: {ep}"

    def test_product_detail_page(self, client, app):
        with app.app_context():
            from app.models.product import Product
            p = Product.query.filter_by(is_active=True).first()
            slug = p.slug

        res = client.get(f'/products/{slug}')
        assert res.status_code == 200
        assert p.title.encode('utf-8') in res.data or p.brand.encode('utf-8') in res.data

    def test_authenticated_customer_pages(self, auth_customer_client):
        customer_endpoints = [
            '/customer/dashboard',
            '/customer/profile',
            '/missions',
            '/cart',
            '/wishlist',
            '/orders'
        ]
        for ep in customer_endpoints:
            res = auth_customer_client.get(ep)
            assert res.status_code == 200, f"Customer failed on endpoint: {ep}"

    def test_authenticated_seller_pages(self, auth_seller_client):
        seller_endpoints = [
            '/seller/dashboard',
            '/seller/products',
            '/seller/inventory',
            '/seller/analytics',
            '/seller/forecasting',
            '/seller/pricing',
            '/seller/customers',
            '/seller/copilot',
            '/seller/settings'
        ]
        for ep in seller_endpoints:
            res = auth_seller_client.get(ep)
            assert res.status_code == 200, f"Seller failed on endpoint: {ep}"
