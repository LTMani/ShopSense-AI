from app.models.user import User
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
