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


from app.models.category import Category
from app.models.product import Product, ProductImage
from app.models.inventory import ProductInventory
from app.extensions import db
import secrets
import json


@seller_api_bp.route('/products/add', methods=['POST'])
@login_required
@seller_required
def api_add_product():
    data = request.get_json(silent=True) or request.form or {}
    seller_id = current_user.seller_profile.id

    title = str(data.get('title', '')).strip()
    brand = str(data.get('brand', 'Generic')).strip()
    try:
        category_id = int(data.get('category_id', 1))
    except (ValueError, TypeError):
        category_id = 1

    try:
        base_price = float(data.get('base_price', 0))
    except (ValueError, TypeError):
        base_price = 0.0

    try:
        sale_price = float(data.get('sale_price') or base_price)
    except (ValueError, TypeError):
        sale_price = base_price

    try:
        cost_price = float(data.get('cost_price') or (sale_price * 0.70))
    except (ValueError, TypeError):
        cost_price = sale_price * 0.70

    try:
        stock_qty = int(data.get('stock_quantity', 50))
    except (ValueError, TypeError):
        stock_qty = 50

    target_usage = data.get('target_usage', 'office, productivity')
    description = data.get('description', f"High quality {brand} product engineered for {target_usage}.")
    features = data.get('key_features', [f"{brand} premium build", "1-year warranty"])
    if isinstance(features, str):
        features = [f.strip() for f in features.split(',') if f.strip()]

    if not title or base_price <= 0:
        return jsonify({'error': 'Title and positive base price are required'}), 400

    sku_suffix = secrets.token_hex(3).upper()
    sku = f"SKU-{sku_suffix}"
    slug_base = title.lower().replace(' ', '-').replace('/', '-')
    slug = f"{slug_base}-{sku_suffix.lower()}"

    product = Product(
        sku=sku,
        title=title,
        slug=slug,
        brand=brand or 'Generic',
        model_number=f"MOD-{sku_suffix}",
        category_id=category_id,
        seller_id=seller_id,
        short_description=description[:200] if description else f"Premium {title}",
        description=description or f"Complete specifications for {title}.",
        base_price=base_price,
        sale_price=sale_price,
        cost_price=cost_price,
        discount_percentage=round(((base_price - sale_price) / base_price) * 100, 1) if base_price > sale_price else 0.0,
        weight_kg=1.0,
        warranty_months=12,
        average_rating=4.5,
        total_reviews_count=1,
        views_count=10,
        purchases_count=0,
        target_usage=target_usage,
        is_active=True,
        is_featured=False
    )
    product.set_key_features_list(features)
    product.aspect_sentiment_summary = json.dumps({'battery': 85, 'performance': 90, 'build_quality': 88, 'value': 92})
    db.session.add(product)
    db.session.flush()

    inventory = ProductInventory(
        product_id=product.id,
        seller_id=seller_id,
        available_quantity=stock_qty,
        reserved_quantity=0,
        safety_stock=10,
        reorder_point=20,
        reorder_quantity=50,
        supplier_lead_time_days=7,
        daily_sales_velocity=1.0,
        stock_status='in_stock' if stock_qty > 15 else ('low_stock' if stock_qty > 0 else 'out_of_stock')
    )
    db.session.add(inventory)

    img = ProductImage(
        product_id=product.id,
        image_url=product.primary_image_url,
        alt_text=f"{product.title} view",
        is_primary=True,
        display_order=0
    )
    db.session.add(img)
    db.session.commit()

    return jsonify({'success': True, 'product': product.to_dict()})
