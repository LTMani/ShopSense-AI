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


from app.models.category import Category
from app.models.product import Product, ProductImage
from app.models.inventory import ProductInventory
from app.extensions import db
import secrets
import json


@seller_bp.route('/seller/products', methods=['GET', 'POST'])
@seller_bp.route('/seller/products/new', methods=['GET', 'POST'])
@login_required
@seller_required
def products():
    seller_id = current_user.seller_profile.id
    categories = Category.query.order_by(Category.display_order).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        brand = request.form.get('brand', '').strip()
        try:
            category_id = int(request.form.get('category_id', 1))
        except (ValueError, TypeError):
            category_id = 1

        try:
            base_price = float(request.form.get('base_price', 0))
        except (ValueError, TypeError):
            base_price = 0.0

        try:
            sale_price = float(request.form.get('sale_price') or base_price)
        except (ValueError, TypeError):
            sale_price = base_price

        try:
            cost_price = float(request.form.get('cost_price') or (sale_price * 0.70))
        except (ValueError, TypeError):
            cost_price = sale_price * 0.70

        try:
            stock_qty = int(request.form.get('stock_quantity', 50))
        except (ValueError, TypeError):
            stock_qty = 50

        target_usage = request.form.get('target_usage', 'office, productivity')
        description = request.form.get('description', f"High quality {brand} product engineered for {target_usage}.")
        features_raw = request.form.get('key_features', '')
        features = [f.strip() for f in features_raw.split(',') if f.strip()] or [f"{brand} premium build", "1-year warranty"]

        if not title or base_price <= 0:
            flash("Product title and a valid positive price are required.", "danger")
            return redirect(url_for('seller_views.products'))

        # Generate unique SKU and slug
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

        # Add Inventory
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

        # Add ProductImage
        img = ProductImage(
            product_id=product.id,
            image_url=product.primary_image_url,
            alt_text=f"{product.title} view",
            is_primary=True,
            display_order=0
        )
        db.session.add(img)
        db.session.commit()

        flash(f"Product '{title}' added to your catalog successfully!", "success")
        return redirect(url_for('seller_views.products'))

    seller_prods = product_repo.get_by_seller(seller_id)
    return render_template('seller/products.html', products=seller_prods, categories=categories)


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
