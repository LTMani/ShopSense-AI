# ShopSense AI Routes Generator
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'app' / 'routes'
BASE.mkdir(parents=True, exist_ok=True)

# 1. auth_routes.py
(BASE / 'auth_routes.py').write_text('''from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import AuthService
from app.schemas.user_schemas import RegisterCustomerSchema, RegisterSellerSchema, LoginSchema

auth_bp = Blueprint('auth_views', __name__)
auth_api_bp = Blueprint('auth_api', __name__, url_prefix='/api/auth')
auth_service = AuthService()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_seller:
            return redirect(url_for('seller_views.dashboard'))
        return redirect(url_for('customer_views.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        user = auth_service.authenticate_user(email, password)
        if user:
            login_user(user, remember=True)
            flash(f"Welcome back, {user.first_name}!", 'success')
            next_page = request.args.get('next')
            if user.is_seller:
                return redirect(next_page or url_for('seller_views.dashboard'))
            return redirect(next_page or url_for('customer_views.dashboard'))
        flash('Invalid email or password. Please try again.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer_views.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        phone = request.form.get('phone', '')

        try:
            auth_service.register_customer(email, password, first_name, last_name, phone)
            user = auth_service.authenticate_user(email, password)
            if user:
                login_user(user, remember=True)
                flash("Account created successfully! Welcome to ShopSense AI.", 'success')
                return redirect(url_for('customer_views.dashboard'))
        except ValueError as err:
            flash(str(err), 'danger')

    return render_template('auth/register.html')


@auth_bp.route('/seller/register', methods=['GET', 'POST'])
def seller_register():
    if current_user.is_authenticated and current_user.is_seller:
        return redirect(url_for('seller_views.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        business_name = request.form.get('business_name', '')
        phone = request.form.get('phone', '')

        try:
            auth_service.register_seller(email, password, first_name, last_name, business_name, phone=phone)
            user = auth_service.authenticate_user(email, password)
            if user:
                login_user(user, remember=True)
                flash(f"Seller store registered! Welcome, {business_name}.", 'success')
                return redirect(url_for('seller_views.dashboard'))
        except ValueError as err:
            flash(str(err), 'danger')

    return render_template('auth/seller_register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('auth_views.login'))


# JSON API Endpoints
@auth_api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    schema = LoginSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    user = auth_service.authenticate_user(data['email'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    login_user(user, remember=True)
    return jsonify({'success': True, 'user': user.to_dict(include_profile=True)})


@auth_api_bp.route('/me', methods=['GET'])
@login_required
def api_me():
    return jsonify({'user': current_user.to_dict(include_profile=True)})
''', encoding='utf-8')

# 2. product_routes.py
(BASE / 'product_routes.py').write_text('''from flask import Blueprint, render_template, request, jsonify, abort
from app.services.catalog_service import CatalogService
from app.services.search_service import SearchService
from app.services.recommendation_service import RecommendationService

product_bp = Blueprint('product_views', __name__)
product_api_bp = Blueprint('product_api', __name__, url_prefix='/api/products')
catalog_service = CatalogService()
search_service = SearchService()
rec_service = RecommendationService()


@product_bp.route('/products')
def product_list():
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    brand = request.args.get('brand')
    min_rating = request.args.get('rating', type=float)
    sort_by = request.args.get('sort', default='relevance')
    page = request.args.get('page', default=1, type=int)

    results = search_service.search(
        query='',
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        min_rating=min_rating,
        sort_by=sort_by,
        page=page,
        per_page=12
    )
    categories = catalog_service.get_categories()

    return render_template(
        'products/product_list.html',
        products=results['products'],
        total=results['total'],
        page=results['page'],
        pages=results['pages'],
        categories=categories,
        selected_category=category_id,
        sort_by=sort_by
    )


@product_bp.route('/products/<slug>')
def product_detail(slug):
    product = catalog_service.get_product_by_slug(slug, detailed=True)
    if not product:
        abort(404)

    related = catalog_service.get_related_products(product['id'], limit=4)
    alternatives = rec_service.get_smart_alternatives(product['id'], limit=3)

    return render_template(
        'products/product_detail.html',
        product=product,
        related_products=related,
        smart_alternatives=alternatives
    )


@product_api_bp.route('/', methods=['GET'])
def api_get_products():
    page = request.args.get('page', default=1, type=int)
    query = request.args.get('q', default='')
    results = search_service.search(query=query, page=page)
    return jsonify(results)


@product_api_bp.route('/<int:product_id>', methods=['GET'])
def api_get_product(product_id):
    product = catalog_service.get_product_by_id(product_id, detailed=True)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'product': product})
''', encoding='utf-8')

# 3. search_routes.py
(BASE / 'search_routes.py').write_text('''from flask import Blueprint, render_template, request, jsonify
from app.services.search_service import SearchService
from app.services.catalog_service import CatalogService

search_bp = Blueprint('search_views', __name__)
search_api_bp = Blueprint('search_api', __name__, url_prefix='/api/search')
search_service = SearchService()
catalog_service = CatalogService()


@search_bp.route('/search')
def search():
    query = request.args.get('q', default='')
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', default='relevance')
    page = request.args.get('page', default=1, type=int)

    results = search_service.search(
        query=query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        page=page,
        per_page=12
    )
    categories = catalog_service.get_categories()

    return render_template(
        'products/search_results.html',
        query=query,
        products=results['products'],
        total=results['total'],
        page=results['page'],
        pages=results['pages'],
        categories=categories,
        extracted=results.get('extracted_filters', {})
    )


@search_api_bp.route('/', methods=['GET'])
def api_search():
    query = request.args.get('q', default='')
    page = request.args.get('page', default=1, type=int)
    results = search_service.search(query=query, page=page)
    return jsonify(results)
''', encoding='utf-8')

# 4. copilot_routes.py
(BASE / 'copilot_routes.py').write_text('''from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.copilot_service import CopilotService
from app.repositories.conversation_repository import ConversationRepository

copilot_bp = Blueprint('copilot_views', __name__)
copilot_api_bp = Blueprint('copilot_api', __name__, url_prefix='/api/copilot')
copilot_service = CopilotService()
conv_repo = ConversationRepository()


@copilot_bp.route('/copilot')
@login_required
def copilot_page():
    conversations = conv_repo.get_user_conversations(current_user.id, copilot_type='customer_shopping')
    return render_template('copilot/copilot.html', conversations=conversations)


@copilot_api_bp.route('/chat', methods=['POST'])
@login_required
def api_copilot_chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    conversation_id = data.get('conversation_id')

    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    result = copilot_service.process_message(
        user_id=current_user.id,
        conversation_id=conversation_id,
        user_message=message
    )
    return jsonify(result)


@copilot_api_bp.route('/conversations/<int:conv_id>', methods=['GET'])
@login_required
def api_get_conversation(conv_id):
    conv = conv_repo.get_by_id(conv_id)
    if not conv or conv.user_id != current_user.id:
        return jsonify({'error': 'Conversation not found'}), 404
    return jsonify({'conversation': conv.to_dict(include_messages=True)})
''', encoding='utf-8')

# 5. comparison_routes.py
(BASE / 'comparison_routes.py').write_text('''from flask import Blueprint, render_template, request, jsonify
from app.services.comparison_service import ComparisonService

compare_bp = Blueprint('compare_views', __name__)
compare_api_bp = Blueprint('compare_api', __name__, url_prefix='/api/compare')
comparison_service = ComparisonService()


@compare_bp.route('/compare')
def compare_page():
    raw_pids = request.args.get('ids', '')
    product_ids = []
    if raw_pids:
        try:
            product_ids = [int(pid.strip()) for pid in raw_pids.split(',') if pid.strip().isdigit()]
        except Exception:
            product_ids = []

    comparison_data = comparison_service.compare_products(product_ids)
    return render_template('comparison/compare.html', comparison=comparison_data, product_ids=product_ids)


@compare_api_bp.route('/', methods=['POST'])
def api_compare():
    data = request.get_json() or {}
    product_ids = data.get('product_ids', [])
    result = comparison_service.compare_products(product_ids)
    return jsonify(result)
''', encoding='utf-8')

# 6. review_routes.py
(BASE / 'review_routes.py').write_text('''from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from app.services.review_intelligence_service import ReviewIntelligenceService
from app.services.catalog_service import CatalogService

review_bp = Blueprint('review_views', __name__)
review_api_bp = Blueprint('review_api', __name__, url_prefix='/api/reviews')
review_service = ReviewIntelligenceService()
catalog_service = CatalogService()


@review_bp.route('/products/<slug>/reviews')
def reviews_page(slug):
    product = catalog_service.get_product_by_slug(slug, detailed=True)
    if not product:
        abort(404)

    intel = review_service.get_review_intelligence(product['id'])
    return render_template('reviews/review_intelligence.html', product=product, intelligence=intel)


@review_api_bp.route('/<int:product_id>', methods=['GET'])
def api_get_reviews(product_id):
    intel = review_service.get_review_intelligence(product_id)
    return jsonify(intel)


@review_api_bp.route('/<int:product_id>/add', methods=['POST'])
@login_required
def api_add_review(product_id):
    data = request.get_json() or {}
    rating = int(data.get('rating', 5))
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': 'Title and review content are required'}), 400

    try:
        new_rev = review_service.add_review(product_id, current_user.id, rating, title, content)
        return jsonify({'success': True, 'review': new_rev})
    except Exception as err:
        return jsonify({'error': str(err)}), 400
''', encoding='utf-8')

# 7. cart_routes.py
(BASE / 'cart_routes.py').write_text('''from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.services.cart_intelligence_service import CartIntelligenceService

cart_bp = Blueprint('cart_views', __name__)
cart_api_bp = Blueprint('cart_api', __name__, url_prefix='/api/cart')
cart_service = CartIntelligenceService()


@cart_bp.route('/cart')
@login_required
def cart_page():
    cart_data = cart_service.get_cart_with_intelligence(current_user.id)
    return render_template('cart/cart.html', cart=cart_data)


@cart_api_bp.route('/', methods=['GET'])
@login_required
def api_get_cart():
    cart_data = cart_service.get_cart_with_intelligence(current_user.id)
    return jsonify(cart_data)


@cart_api_bp.route('/add', methods=['POST'])
@login_required
def api_add_to_cart():
    data = request.get_json() or {}
    product_id = int(data.get('product_id', 0))
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    updated_cart = cart_service.add_to_cart(current_user.id, product_id, quantity)
    return jsonify({'success': True, 'cart': updated_cart})


@cart_api_bp.route('/update', methods=['POST'])
@login_required
def api_update_cart():
    data = request.get_json() or {}
    cart_item_id = int(data.get('cart_item_id', 0))
    quantity = int(data.get('quantity', 1))

    updated_cart = cart_service.update_quantity(current_user.id, cart_item_id, quantity)
    return jsonify({'success': True, 'cart': updated_cart})


@cart_api_bp.route('/remove/<int:cart_item_id>', methods=['DELETE', 'POST'])
@login_required
def api_remove_from_cart(cart_item_id):
    updated_cart = cart_service.remove_item(current_user.id, cart_item_id)
    return jsonify({'success': True, 'cart': updated_cart})
''', encoding='utf-8')

# 8. wishlist_routes.py
(BASE / 'wishlist_routes.py').write_text('''from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.wishlist_intelligence_service import WishlistIntelligenceService

wishlist_bp = Blueprint('wishlist_views', __name__)
wishlist_api_bp = Blueprint('wishlist_api', __name__, url_prefix='/api/wishlist')
wishlist_service = WishlistIntelligenceService()


@wishlist_bp.route('/wishlist')
@login_required
def wishlist_page():
    wishlist_data = wishlist_service.get_wishlist_with_insights(current_user.id)
    return render_template('wishlist/wishlist.html', wishlist=wishlist_data)


@wishlist_api_bp.route('/toggle', methods=['POST'])
@login_required
def api_toggle_wishlist():
    data = request.get_json() or {}
    product_id = int(data.get('product_id', 0))
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    res = wishlist_service.toggle_wishlist(current_user.id, product_id)
    return jsonify(res)
''', encoding='utf-8')

# 9. mission_routes.py
(BASE / 'mission_routes.py').write_text('''from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.shopping_mission_service import ShoppingMissionService
from app.repositories.mission_repository import MissionRepository

mission_bp = Blueprint('mission_views', __name__)
mission_api_bp = Blueprint('mission_api', __name__, url_prefix='/api/missions')
mission_service = ShoppingMissionService()
mission_repo = MissionRepository()


@mission_bp.route('/missions')
@login_required
def missions_list():
    missions = mission_repo.get_by_user(current_user.id)
    return render_template('missions/missions_list.html', missions=missions)


@mission_api_bp.route('/build', methods=['POST'])
@login_required
def api_build_mission():
    data = request.get_json() or {}
    prompt = data.get('prompt', '').strip()
    target_budget = float(data.get('target_budget', 30000.0))
    mode = data.get('optimization_mode', 'balanced')

    if not prompt or target_budget <= 0:
        return jsonify({'error': 'Valid prompt and budget are required'}), 400

    mission_data = mission_service.build_mission(current_user.id, prompt, target_budget, mode)
    return jsonify({'success': True, 'mission': mission_data})
''', encoding='utf-8')

# 10. order_routes.py
(BASE / 'order_routes.py').write_text('''from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.order_service import OrderService
from app.services.cart_intelligence_service import CartIntelligenceService
from app.repositories.order_repository import OrderRepository

order_bp = Blueprint('order_views', __name__)
order_api_bp = Blueprint('order_api', __name__, url_prefix='/api/orders')
order_service = OrderService()
cart_service = CartIntelligenceService()
order_repo = OrderRepository()


@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout_page():
    cart_data = cart_service.get_cart_with_intelligence(current_user.id)
    if cart_data['total_items_count'] == 0:
        flash("Your cart is empty.", 'warning')
        return redirect(url_for('cart_views.cart_page'))

    if request.method == 'POST':
        name = request.form.get('shipping_name', '')
        address = request.form.get('shipping_address_line1', '')
        city = request.form.get('shipping_city', '')
        state = request.form.get('shipping_state', '')
        postal_code = request.form.get('shipping_postal_code', '')
        phone = request.form.get('shipping_phone', '')
        payment_method = request.form.get('payment_method', 'simulated_upi')

        try:
            order = order_service.checkout_cart(
                user_id=current_user.id,
                shipping_name=name,
                shipping_address_line1=address,
                shipping_city=city,
                shipping_state=state,
                shipping_postal_code=postal_code,
                payment_method=payment_method,
                shipping_phone=phone
            )
            flash(f"Order #{order['order_number']} placed successfully!", 'success')
            return redirect(url_for('order_views.order_detail', order_number=order['order_number']))
        except Exception as err:
            flash(str(err), 'danger')

    return render_template('orders/checkout.html', cart=cart_data)


@order_bp.route('/orders')
@login_required
def orders_list():
    orders = order_repo.get_by_user(current_user.id)
    return render_template('orders/orders_list.html', orders=orders)


@order_bp.route('/orders/<order_number>')
@login_required
def order_detail(order_number):
    order = order_repo.get_by_order_number(order_number)
    if not order or (order.user_id != current_user.id and not current_user.is_seller and not current_user.is_admin):
        flash("Order not found.", 'danger')
        return redirect(url_for('order_views.orders_list'))

    return render_template('orders/order_detail.html', order=order.to_dict(include_items=True))
''', encoding='utf-8')

# 11. customer_routes.py
(BASE / 'customer_routes.py').write_text('''from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.repositories.order_repository import OrderRepository
from app.repositories.wishlist_repository import WishlistRepository
from app.services.recommendation_service import RecommendationService

customer_bp = Blueprint('customer_views', __name__)
order_repo = OrderRepository()
wishlist_repo = WishlistRepository()
rec_service = RecommendationService()


@customer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_seller:
        return redirect(url_for('seller_views.dashboard'))

    recent_orders = order_repo.get_by_user(current_user.id, limit=3)
    wishlist = wishlist_repo.get_by_user_id(current_user.id)
    recommendations = rec_service.get_personalized_recommendations(current_user.id, limit=4)

    return render_template(
        'customer/dashboard.html',
        orders=recent_orders,
        wishlist=wishlist,
        recommendations=recommendations
    )


@customer_bp.route('/profile')
@login_required
def profile():
    return render_template('customer/profile.html', user=current_user)
''', encoding='utf-8')

# 12. seller_routes.py
(BASE / 'seller_routes.py').write_text('''from flask import Blueprint, render_template, redirect, url_for, flash, request
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
''', encoding='utf-8')

# 13. seller_api_routes.py
(BASE / 'seller_api_routes.py').write_text('''from flask import Blueprint, request, jsonify
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
''', encoding='utf-8')

# 14. system_routes.py
(BASE / 'system_routes.py').write_text('''from flask import Blueprint, render_template, jsonify
from app.services.catalog_service import CatalogService
from app.services.recommendation_service import RecommendationService

system_bp = Blueprint('system_views', __name__)
catalog_service = CatalogService()
rec_service = RecommendationService()


@system_bp.route('/')
def landing_page():
    categories = catalog_service.get_categories()
    featured = catalog_service.get_featured_products(limit=8)
    trending = rec_service.get_personalized_recommendations(limit=4)
    return render_template('index.html', categories=categories, featured_products=featured, trending=trending)


@system_bp.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'platform': 'ShopSense AI',
        'version': '1.0.0',
        'mode': 'production-ready'
    })


@system_bp.route('/settings')
def app_settings():
    return render_template('settings/app_settings.html')
''', encoding='utf-8')

# 15. __init__.py for routes
(BASE / '__init__.py').write_text('''from app.routes.auth_routes import auth_bp, auth_api_bp
from app.routes.product_routes import product_bp, product_api_bp
from app.routes.search_routes import search_bp, search_api_bp
from app.routes.copilot_routes import copilot_bp, copilot_api_bp
from app.routes.comparison_routes import compare_bp, compare_api_bp
from app.routes.review_routes import review_bp, review_api_bp
from app.routes.cart_routes import cart_bp, cart_api_bp
from app.routes.wishlist_routes import wishlist_bp, wishlist_api_bp
from app.routes.mission_routes import mission_bp, mission_api_bp
from app.routes.order_routes import order_bp, order_api_bp
from app.routes.customer_routes import customer_bp
from app.routes.seller_routes import seller_bp
from app.routes.seller_api_routes import seller_api_bp
from app.routes.system_routes import system_bp


def register_routes(app):
    """Registers all web view and RESTful API blueprints with the Flask application instance."""
    app.register_blueprint(system_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(auth_api_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(seller_api_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(product_api_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(search_api_bp)
    app.register_blueprint(copilot_bp)
    app.register_blueprint(copilot_api_bp)
    app.register_blueprint(compare_bp)
    app.register_blueprint(compare_api_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(review_api_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(cart_api_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(wishlist_api_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(mission_api_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(order_api_bp)
''', encoding='utf-8')

print('All routes modules generated successfully!')
