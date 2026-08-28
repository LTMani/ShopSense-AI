import pytest
from app.models.user import User, Role
from app.models.profile import CustomerProfile, SellerProfile
from app.models.category import Category
from app.models.product import Product, ProductAttribute, ProductImage
from app.models.inventory import ProductInventory, InventoryTransaction, InventoryAlert
from app.models.price import ProductPriceHistory, PricePromotionRule
from app.models.review import Review, ReviewAspectRating
from app.models.cart import Cart, CartItem
from app.models.wishlist import Wishlist, WishlistItem
from app.models.order import Order, OrderItem
from app.models.tracking import BrowsingEvent, SearchHistory
from app.models.mission import ShoppingMission, ShoppingMissionItem
from app.models.conversation import Conversation, ConversationMessage
from app.models.forecast import DemandForecast
from app.models.analytics import SellerMetricDaily, ProductPerformanceScore
from app.models.audit import AuditLog, SystemSetting


def test_user_and_profile_models(app):
    with app.app_context():
        role = Role.query.filter_by(name='customer').first()
        u = User(email='unit_model_test@test.com', first_name='Riya', last_name='Patel', role_id=role.id)
        u.role = role
        u.set_password('ModelPass123!')
        assert u.check_password('ModelPass123!')
        assert not u.check_password('WrongPass!')
        assert u.full_name == 'Riya Patel'
        assert u.is_customer is True
        assert u.is_seller is False
        d = u.to_dict()
        assert d['email'] == 'unit_model_test@test.com'


def test_category_and_product_models(app):
    with app.app_context():
        cat = Category(name='Test Sound Tech', slug='test-sound-tech', icon_name='headphones')
        assert cat.name == 'Test Sound Tech'
        d_cat = cat.to_dict()
        assert d_cat['name'] == 'Test Sound Tech'

        prod = Product(
            seller_id=1,
            category_id=1,
            title='Test Audio Device',
            slug='test-audio-device',
            sku='TEST-AUD-001',
            base_price=5000.0,
            sale_price=4000.0,
            cost_price=2800.0
        )
        assert prod.current_price == 4000.0
        d_prod = prod.to_dict()
        assert d_prod['sku'] == 'TEST-AUD-001'


def test_cart_and_wishlist_models(app):
    with app.app_context():
        cart = Cart(user_id=1)
        item = CartItem(cart_id=1, product_id=1, quantity=3, unit_price=1000.0)
        assert item.total_price == 3000.0

        wishlist = Wishlist(user_id=1)
        w_item = WishlistItem(wishlist_id=1, product_id=1, price_when_added=5000.0)
        assert w_item.price_when_added == 5000.0


def test_order_model_properties(app):
    with app.app_context():
        order = Order(
            order_number='ORD-TEST-999',
            user_id=1,
            subtotal_amount=10000.0,
            tax_amount=1800.0,
            shipping_fee=0.0,
            total_amount=11800.0,
            payment_method='simulated_upi',
            status='processing'
        )
        assert order.total_amount == 11800.0
        assert order.status == 'processing'
        d_ord = order.to_dict()
        assert d_ord['order_number'] == 'ORD-TEST-999'


def test_conversation_and_messages(app):
    with app.app_context():
        conv = Conversation(user_id=None, copilot_type='customer_shopping', session_title='Test Session')
        conv.set_context_dict({'budget': 50000.0, 'category': 'Laptops & Computers'})
        ctx = conv.get_context_dict()
        assert ctx.get('budget') == 50000.0

        msg = ConversationMessage(conversation_id=1, sender='user', content='Hello AI')
        d_msg = msg.to_dict()
        assert d_msg['content'] == 'Hello AI'
