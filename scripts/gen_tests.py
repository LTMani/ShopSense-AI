# ShopSense AI Comprehensive Test Suite Generator
from pathlib import Path

BASE_T = Path(__file__).resolve().parent.parent / 'tests'
BASE_T.mkdir(parents=True, exist_ok=True)

# 1. conftest.py
(BASE_T / 'conftest.py').write_text('''import pytest
from app import create_app, db
from app.seeds.seeder import run_full_seeder
from app.models.user import User


@pytest.fixture(scope='session')
def app():
    """Create and configure a clean testing Flask application instance."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        run_full_seeder()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for making HTTP requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for CLI commands."""
    return app.test_cli_runner()


@pytest.fixture
def auth_customer_client(client, app):
    """Test client logged in as a demo customer."""
    with app.app_context():
        user = User.query.filter_by(email='customer@shopsense.ai').first()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user.id)
        sess['_fresh'] = True
    return client


@pytest.fixture
def auth_seller_client(client, app):
    """Test client logged in as a demo seller."""
    with app.app_context():
        user = User.query.filter_by(email='seller.apex@shopsense.ai').first()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user.id)
        sess['_fresh'] = True
    return client
''', encoding='utf-8')

# 2. test_auth.py
(BASE_T / 'test_auth.py').write_text('''import pytest
from app.services.auth_service import AuthService
from app.models.user import User


def test_customer_registration_and_login(app):
    with app.app_context():
        auth = AuthService()
        email = 'new_customer@test.com'
        user_dict = auth.register_customer(
            email=email,
            password='SecretPassword123!',
            first_name='Ananya',
            last_name='Iyer'
        )
        assert user_dict['email'] == email
        assert user_dict['first_name'] == 'Ananya'

        # Authenticate with valid password
        authenticated = auth.authenticate_user(email, 'SecretPassword123!')
        assert authenticated is not None
        assert authenticated.email == email

        # Authenticate with invalid password
        invalid = auth.authenticate_user(email, 'WrongPassword!')
        assert invalid is None


def test_duplicate_email_prevention(app):
    with app.app_context():
        auth = AuthService()
        with pytest.raises(ValueError):
            auth.register_customer(
                email='customer@shopsense.ai',
                password='Password123!',
                first_name='Duplicate',
                last_name='User'
            )
''', encoding='utf-8')

# 3. test_catalog_and_search.py
(BASE_T / 'test_catalog_and_search.py').write_text('''from app.services.catalog_service import CatalogService
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
''', encoding='utf-8')

# 4. test_copilot.py
(BASE_T / 'test_copilot.py').write_text('''from app.services.copilot_service import CopilotService
from app.models.user import User


def test_copilot_conversational_turn(app):
    with app.app_context():
        user = User.query.filter_by(email='customer@shopsense.ai').first()
        copilot = CopilotService()

        # Turn 1: Initial query
        res1 = copilot.process_message(
            user_id=user.id,
            conversation_id=None,
            user_message="I need a laptop under ₹60,000 for coding, occasional gaming, and long battery life."
        )

        assert res1['conversation_id'] is not None
        assert len(res1['recommended_products']) > 0
        assert res1['extracted_context'].get('budget') == 60000.0
        assert 'Best Match' in [p.get('badge') for p in res1['recommended_products']]

        # Turn 2: Follow-up refinement
        res2 = copilot.process_message(
            user_id=user.id,
            conversation_id=res1['conversation_id'],
            user_message="Battery life matters more than gaming."
        )
        assert res2['conversation_id'] == res1['conversation_id']
        assert 'battery' in res2['extracted_context'].get('priorities', [])
''', encoding='utf-8')

# 5. test_recommendations_and_comparison.py
(BASE_T / 'test_recommendations_and_comparison.py').write_text('''from app.services.recommendation_service import RecommendationService
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
''', encoding='utf-8')

# 6. test_reviews_and_aspects.py
(BASE_T / 'test_reviews_and_aspects.py').write_text('''from app.services.review_intelligence_service import ReviewIntelligenceService
from app.models.product import Product
from app.models.user import User


def test_review_aspect_sentiment_extraction(app):
    with app.app_context():
        rev_svc = ReviewIntelligenceService()
        product = Product.query.filter_by(is_active=True).first()
        user = User.query.filter_by(email='customer@shopsense.ai').first()

        review = rev_svc.add_review(
            product_id=product.id,
            user_id=user.id,
            rating=5,
            title="Superb battery backup and crystal sound!",
            content="The battery lasts over 12 hours easily. Audio is crisp with great deep bass. Very comfortable."
        )

        assert review['sentiment_label'] == 'positive'
        assert review['sentiment_polarity'] > 0.0

        intel = rev_svc.get_review_intelligence(product.id)
        assert 'aspect_breakdown' in intel
        assert intel['total_reviews'] > 0
''', encoding='utf-8')

# 7. test_cart_and_missions.py
(BASE_T / 'test_cart_and_missions.py').write_text('''from app.services.cart_intelligence_service import CartIntelligenceService
from app.services.shopping_mission_service import ShoppingMissionService
from app.models.product import Product
from app.models.user import User


def test_smart_cart_operations(app):
    with app.app_context():
        cart_svc = CartIntelligenceService()
        user = User.query.filter_by(email='customer@shopsense.ai').first()
        product = Product.query.filter_by(is_active=True).first()

        # Add item
        cart = cart_svc.add_to_cart(user.id, product.id, quantity=2)
        assert cart['total_items_count'] >= 2
        assert 'intelligence' in cart

        # Remove item
        item_id = cart['items'][0]['id']
        updated_cart = cart_svc.remove_item(user.id, item_id)
        assert updated_cart is not None


def test_shopping_mission_basket_solver(app):
    with app.app_context():
        mission_svc = ShoppingMissionService()
        user = User.query.filter_by(email='customer@shopsense.ai').first()

        mission = mission_svc.build_mission(
            user_id=user.id,
            prompt="Build college study setup with laptop and chair",
            target_budget=30000.0,
            optimization_mode='balanced'
        )

        assert mission['target_budget'] == 30000.0
        assert len(mission['items']) > 0
        assert mission['allocated_total'] > 0
''', encoding='utf-8')

# 8. test_seller_intelligence.py
(BASE_T / 'test_seller_intelligence.py').write_text('''from app.services.seller_analytics_service import SellerAnalyticsService
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
''', encoding='utf-8')

# 9. test_e2e_flow.py
(BASE_T / 'test_e2e_flow.py').write_text('''from app.models.user import User
from app.models.product import Product
from app.services.cart_intelligence_service import CartIntelligenceService
from app.services.order_service import OrderService


def test_complete_end_to_end_journey(app):
    with app.app_context():
        # 1. Customer user
        user = User.query.filter_by(email='customer@shopsense.ai').first()
        product = Product.query.filter_by(is_active=True).first()

        # 2. Add to Cart
        cart_svc = CartIntelligenceService()
        cart = cart_svc.add_to_cart(user.id, product.id, quantity=1)
        assert cart['total_items_count'] >= 1

        # 3. Complete Checkout & Inventory Deduction
        initial_stock = product.inventory.available_quantity if product.inventory else 0
        order_svc = OrderService()
        order = order_svc.checkout_cart(
            user_id=user.id,
            shipping_name='Rohan Sharma',
            shipping_address_line1='Flat 402, Bellandur',
            shipping_city='Bengaluru',
            shipping_state='Karnataka',
            shipping_postal_code='560103',
            payment_method='simulated_upi'
        )

        assert order['order_number'].startswith('ORD-')
        assert order['total_amount'] > 0
        assert order['status'] == 'processing'
        if product.inventory:
            assert product.inventory.available_quantity == max(0, initial_stock - 1)
''', encoding='utf-8')

print('All 9 test suite modules generated successfully!')
