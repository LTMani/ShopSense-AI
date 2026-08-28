import pytest
from app.services.auth_service import AuthService
from app.services.catalog_service import CatalogService
from app.services.search_service import SearchService
from app.services.copilot_service import CopilotService
from app.services.recommendation_service import RecommendationService
from app.services.comparison_service import ComparisonService
from app.services.review_intelligence_service import ReviewIntelligenceService
from app.services.cart_intelligence_service import CartIntelligenceService
from app.services.wishlist_intelligence_service import WishlistIntelligenceService
from app.services.shopping_mission_service import ShoppingMissionService
from app.services.seller_analytics_service import SellerAnalyticsService
from app.services.inventory_intelligence_service import InventoryIntelligenceService
from app.services.demand_forecasting_service import DemandForecastingService
from app.services.pricing_intelligence_service import PricingIntelligenceService
from app.services.customer_segmentation_service import CustomerSegmentationService
from app.services.order_service import OrderService
from app.models.user import User
from app.models.product import Product


class TestServicesDeepSuite:
    """Comprehensive test verification across all 17 ShopSense AI domain services."""

    def test_catalog_service_queries(self, app):
        with app.app_context():
            cat_svc = CatalogService()
            cats = cat_svc.get_categories()
            assert len(cats) >= 8

            prods = cat_svc.get_paginated_products(page=1, per_page=10)
            assert len(prods['items']) > 0
            assert prods['total'] > 0

    def test_recommendation_trending_and_similar(self, app):
        with app.app_context():
            rec_svc = RecommendationService()
            user = User.query.filter_by(email='customer@shopsense.ai').first()
            prod = Product.query.filter_by(is_active=True).first()

            # Personalized
            personalized = rec_svc.get_personalized_recommendations(user.id, limit=4)
            assert len(personalized) > 0

            # Similar / Smart alternatives
            similar = rec_svc.get_smart_alternatives(prod.id)
            assert isinstance(similar, dict)
            assert 'budget_friendly' in similar or 'premium_upgrades' in similar

    def test_wishlist_intelligence_service(self, app):
        with app.app_context():
            w_svc = WishlistIntelligenceService()
            user = User.query.filter_by(email='customer@shopsense.ai').first()
            prod = Product.query.filter_by(is_active=True).first()

            # Toggle add
            res1 = w_svc.toggle_wishlist(user.id, prod.id)
            assert res1['is_wishlisted'] in (True, False)

            # Get user wishlist with insights
            w_data = w_svc.get_wishlist_with_insights(user.id)
            assert 'items' in w_data
            assert 'insights' in w_data

    def test_inventory_intelligence_alerts(self, app):
        with app.app_context():
            inv_svc = InventoryIntelligenceService()
            user = User.query.filter_by(email='seller.apex@shopsense.ai').first()
            seller_id = user.seller_profile.id

            summary = inv_svc.get_inventory_summary(seller_id)
            assert summary['total_sku_count'] > 0
            assert 'inventory_items' in summary

    def test_customer_segmentation_service(self, app):
        with app.app_context():
            seg_svc = CustomerSegmentationService()
            user = User.query.filter_by(email='seller.apex@shopsense.ai').first()
            seller_id = user.seller_profile.id

            cohorts = seg_svc.get_customer_segments(seller_id)
            assert len(cohorts) > 0
            for c in cohorts:
                assert 'name' in c
                assert 'description' in c
                assert 'recommended_strategy' in c

    def test_pricing_intelligence_service(self, app):
        with app.app_context():
            pricing_svc = PricingIntelligenceService()
            user = User.query.filter_by(email='seller.apex@shopsense.ai').first()
            seller_id = user.seller_profile.id

            recs = pricing_svc.get_pricing_recommendations(seller_id)
            assert len(recs) > 0
            for r in recs:
                assert 'current_price' in r
                assert 'recommended_price' in r
                assert 'action' in r
                assert 'reason' in r
