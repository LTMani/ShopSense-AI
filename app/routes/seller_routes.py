from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.middleware.auth_middleware import seller_required
from app.services.seller_analytics_service import SellerAnalyticsService
from app.services.inventory_intelligence_service import InventoryIntelligenceService
from app.services.pricing_intelligence_service import PricingIntelligenceService
from app.services.customer_segmentation_service import CustomerSegmentationService
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository

seller_bp = Blueprint('seller_views', __name__)
analytics_service = SellerAnalyticsService()
inventory_service = InventoryIntelligenceService()
pricing_service = PricingIntelligenceService()
segment_service = CustomerSegmentationService()
product_repo = ProductRepository()
order_repo = OrderRepository()


@seller_bp.route('/seller/login')
def seller_login():
    if current_user.is_authenticated:
        if current_user.is_seller:
            return redirect(url_for('seller_views.dashboard'))
        return redirect(url_for('customer_views.dashboard'))
    return redirect(url_for('auth_views.login'))


@seller_bp.route('/seller/dashboard')
@login_required
@seller_required
def dashboard():
    seller_id = current_user.seller_profile.id
    kpis = analytics_service.get_seller_dashboard_kpis(seller_id)
    inv_summary = inventory_service.get_inventory_summary(seller_id)
    recent_orders = order_repo.get_seller_orders(seller_id, limit=5)

    return render_template(
        'seller/dashboard.html',
        kpis=kpis,
        inventory=inv_summary,
        recent_orders=recent_orders
    )


@seller_bp.route('/seller/products')
@login_required
@seller_required
def products():
    seller_id = current_user.seller_profile.id
    seller_prods = product_repo.get_by_seller(seller_id)
    return render_template('seller/products.html', products=seller_prods)


@seller_bp.route('/seller/inventory')
@login_required
@seller_required
def inventory():
    seller_id = current_user.seller_profile.id
    summary = inventory_service.get_inventory_summary(seller_id)
    return render_template('seller/inventory.html', inventory=summary)


@seller_bp.route('/seller/analytics')
@login_required
@seller_required
def analytics():
    seller_id = current_user.seller_profile.id
    kpis = analytics_service.get_seller_dashboard_kpis(seller_id)
    rankings = analytics_service.get_product_performance_ranking(seller_id)
    return render_template('seller/analytics.html', kpis=kpis, performance_rankings=rankings)


@seller_bp.route('/seller/forecasting')
@login_required
@seller_required
def forecasting():
    seller_id = current_user.seller_profile.id
    seller_prods = product_repo.get_by_seller(seller_id)
    return render_template('seller/forecasting.html', products=seller_prods)


@seller_bp.route('/seller/pricing')
@login_required
@seller_required
def pricing():
    seller_id = current_user.seller_profile.id
    recs = pricing_service.get_pricing_recommendations(seller_id)
    return render_template('seller/pricing.html', pricing_recommendations=recs)


@seller_bp.route('/seller/customers')
@login_required
@seller_required
def customers():
    segments = segment_service.get_all_segments()
    return render_template('seller/customers.html', segments=segments)


@seller_bp.route('/seller/copilot')
@login_required
@seller_required
def seller_copilot():
    return render_template('seller/seller_copilot.html')


@seller_bp.route('/seller/settings')
@login_required
@seller_required
def seller_settings():
    return render_template('seller/seller_settings.html')
