from app.services.cart_intelligence_service import CartIntelligenceService
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
