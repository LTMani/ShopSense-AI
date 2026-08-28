from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.middleware.auth_middleware import seller_required
from app.services.seller_analytics_service import SellerAnalyticsService
from app.services.inventory_intelligence_service import InventoryIntelligenceService
from app.services.demand_forecasting_service import DemandForecastingService
from app.services.pricing_intelligence_service import PricingIntelligenceService
from app.services.customer_segmentation_service import CustomerSegmentationService
from app.ai.seller.seller_copilot_service import SellerCopilotService

seller_api_bp = Blueprint('seller_api', __name__, url_prefix='/api/seller')
analytics_service = SellerAnalyticsService()
inventory_service = InventoryIntelligenceService()
forecast_service = DemandForecastingService()
pricing_service = PricingIntelligenceService()
segment_service = CustomerSegmentationService()
seller_copilot_service = SellerCopilotService()


@seller_api_bp.route('/kpis', methods=['GET'])
@login_required
@seller_required
def api_seller_kpis():
    seller_id = current_user.seller_profile.id
    data = analytics_service.get_seller_dashboard_kpis(seller_id)
    return jsonify(data)


@seller_api_bp.route('/forecast/<int:product_id>', methods=['GET'])
@login_required
@seller_required
def api_product_forecast(product_id):
    horizon = request.args.get('horizon', default=14, type=int)
    data = forecast_service.generate_product_forecast(product_id, horizon_days=horizon)
    return jsonify(data)


@seller_api_bp.route('/inventory/restock', methods=['POST'])
@login_required
@seller_required
def api_restock():
    data = request.get_json() or {}
    inv_id = int(data.get('inventory_id', 0))
    qty = int(data.get('quantity', 0))
    if qty <= 0:
        return jsonify({'error': 'Quantity must be greater than 0'}), 400

    updated = inventory_service.restock_inventory(inv_id, qty)
    return jsonify({'success': True, 'inventory': updated})


@seller_api_bp.route('/copilot/chat', methods=['POST'])
@login_required
@seller_required
def api_seller_copilot_chat():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Query cannot be empty'}), 400

    seller_id = current_user.seller_profile.id
    result = seller_copilot_service.process_seller_query(seller_id, query)
    return jsonify(result)
