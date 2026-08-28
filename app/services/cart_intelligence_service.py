from typing import Dict, Any, List
from app.models.cart import Cart, CartItem
from app.repositories.cart_repository import CartRepository, CartItemRepository
from app.repositories.product_repository import ProductRepository
from app.services.recommendation_service import RecommendationService
from app.extensions import db


class CartIntelligenceService:
    """Analyzes cart items for budget optimization, accessories, duplicates, and compatibility."""

    def __init__(self):
        self.cart_repo = CartRepository()
        self.cart_item_repo = CartItemRepository()
        self.product_repo = ProductRepository()
        self.rec_service = RecommendationService()

    def get_cart_with_intelligence(self, user_id: int) -> Dict[str, Any]:
        cart = self.cart_repo.get_by_user_id(user_id)
        items = cart.items.all()
        cart_data = cart.to_dict(include_items=True)

        insights = []
        potential_savings = 0.0
        complementary_products = []

        # 1. Analyze each item for cheaper alternatives
        for item in items:
            p = item.product
            if p:
                alts = self.rec_service.get_smart_alternatives(p.id, limit=1)
                if alts['budget_alternatives']:
                    cheaper = alts['budget_alternatives'][0]
                    save_amt = cheaper['savings_amount'] * item.quantity
                    potential_savings += save_amt
                    insights.append({
                        'type': 'savings_opportunity',
                        'item_title': p.title,
                        'message': f"You can save ₹{save_amt:,.0f} by choosing {cheaper['product']['title']}.",
                        'alternative_product': cheaper['product']
                    })

        # 2. Complementary Accessories Suggestions
        categories_in_cart = {item.product.category.name for item in items if item.product and item.product.category}
        if 'Laptops' in categories_in_cart and 'Computer Peripherals' not in categories_in_cart:
            insights.append({
                'type': 'accessory_suggestion',
                'message': 'Customers buying laptops frequently add a wireless mouse or USB-C multi-port hub.'
            })

        cart_data['intelligence'] = {
            'insights': insights,
            'potential_savings': round(potential_savings, 2),
            'free_shipping_eligible': cart.subtotal_amount >= 1000.0,
            'free_shipping_threshold': 1000.0
        }
        return cart_data

    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> Dict[str, Any]:
        cart = self.cart_repo.get_by_user_id(user_id)
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        item = self.cart_item_repo.get_item(cart.id, product_id)
        if item:
            item.quantity += quantity
        else:
            self.cart_item_repo.create(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.current_price
            )
        db.session.commit()
        return self.get_cart_with_intelligence(user_id)

    def update_quantity(self, user_id: int, cart_item_id: int, quantity: int) -> Dict[str, Any]:
        cart = self.cart_repo.get_by_user_id(user_id)
        item = self.cart_item_repo.get_by_id(cart_item_id)
        if item and item.cart_id == cart.id:
            if quantity <= 0:
                self.cart_item_repo.delete(item)
            else:
                item.quantity = quantity
                db.session.commit()
        return self.get_cart_with_intelligence(user_id)

    def remove_item(self, user_id: int, cart_item_id: int) -> Dict[str, Any]:
        return self.update_quantity(user_id, cart_item_id, 0)
