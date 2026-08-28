from app.services.seller_analytics_service import SellerAnalyticsService
from app.services.inventory_intelligence_service import InventoryIntelligenceService
from app.services.demand_forecasting_service import DemandForecastingService
from app.services.pricing_intelligence_service import PricingIntelligenceService
from app.ai.seller.seller_copilot_service import SellerCopilotService
from app.models.user import User
from app.models.product import Product


def test_seller_kpis_and_inventory(app):
    with app.app_context():
        user = User.query.filter_by(email='seller.apex@shopsense.ai').first()
        seller_id = user.seller_profile.id

        analytics_svc = SellerAnalyticsService()
        kpis = analytics_svc.get_seller_dashboard_kpis(seller_id)
        assert kpis['total_revenue'] > 0
        assert kpis['units_sold'] > 0

        inv_svc = InventoryIntelligenceService()
        summary = inv_svc.get_inventory_summary(seller_id)
        assert summary['total_sku_count'] > 0


def test_demand_forecasting_and_seller_copilot(app):
    with app.app_context():
        user = User.query.filter_by(email='seller.apex@shopsense.ai').first()
        seller_id = user.seller_profile.id
        product = Product.query.filter_by(seller_id=seller_id).first()

        # Demand forecast
        forecast_svc = DemandForecastingService()
        forecast = forecast_svc.generate_product_forecast(product.id, horizon_days=14)
        assert forecast['horizon_days'] == 14
        assert len(forecast['daily_projections']) == 14

        # Seller Copilot
        copilot_svc = SellerCopilotService()
        result = copilot_svc.process_seller_query(seller_id, "Why did sales decrease this month?")
        assert 'response' in result
        assert len(result['response']) > 0
