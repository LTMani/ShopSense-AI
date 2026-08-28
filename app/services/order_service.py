import secrets
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.models.order import Order, OrderItem, OrderStatusHistory
from app.models.inventory import InventoryTransaction
from app.repositories.order_repository import OrderRepository, OrderItemRepository
from app.repositories.cart_repository import CartRepository, CartItemRepository
from app.repositories.product_repository import ProductRepository
from app.extensions import db


class OrderService:
    """Internal simulated order placement, fulfillment lifecycle, and inventory decrement."""

    def __init__(self):
        self.order_repo = OrderRepository()
        self.order_item_repo = OrderItemRepository()
        self.cart_repo = CartRepository()
        self.cart_item_repo = CartItemRepository()
        self.product_repo = ProductRepository()

    def checkout_cart(
        self,
        user_id: int,
        shipping_name: str,
        shipping_address_line1: str,
        shipping_city: str,
        shipping_state: str,
        shipping_postal_code: str,
        payment_method: str = 'simulated_upi',
        shipping_phone: str = ''
    ) -> Dict[str, Any]:
        cart = self.cart_repo.get_by_user_id(user_id)
        items = cart.items.all()
        if not items:
            raise ValueError("Your cart is empty. Add items to checkout.")

        order_number = f"ORD-{secrets.token_hex(4).upper()}"
        subtotal = cart.subtotal_amount
        shipping_fee = 0.0 if subtotal >= 1000.0 else 99.0
        tax = round(subtotal * 0.18, 2)  # 18% simulated GST
        total = subtotal + shipping_fee + tax

        order = Order(
            order_number=order_number,
            user_id=user_id,
            status='processing',
            subtotal_amount=subtotal,
            tax_amount=tax,
            shipping_fee=shipping_fee,
            total_amount=total,
            payment_method=payment_method,
            payment_status='paid',
            shipping_name=shipping_name,
            shipping_phone=shipping_phone,
            shipping_address_line1=shipping_address_line1,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_postal_code=shipping_postal_code
        )
        db.session.add(order)
        db.session.flush()

        # Add line items & deduct inventory
        for item in items:
            p = item.product
            order_item = OrderItem(
                order_id=order.id,
                product_id=p.id,
                seller_id=p.seller_id,
                product_title=p.title,
                product_sku=p.sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
                unit_cost=p.cost_price,
                total_price=item.total_price,
                item_status='processing'
            )
            db.session.add(order_item)

            # Deduct inventory & record transaction
            if p.inventory:
                p.inventory.available_quantity = max(0, p.inventory.available_quantity - item.quantity)
                tx = InventoryTransaction(
                    inventory_id=p.inventory.id,
                    transaction_type='sale',
                    quantity_change=-item.quantity,
                    quantity_after=p.inventory.available_quantity,
                    reference_id=order_number,
                    notes='Order checkout fulfillment'
                )
                db.session.add(tx)

            p.purchases_count += item.quantity

        # Add initial status history
        history = OrderStatusHistory(order_id=order.id, status='processing', comment='Order confirmed and payment verified.')
        db.session.add(history)

        # Clear active cart
        self.cart_item_repo.clear_cart(cart.id)
        db.session.commit()

        return order.to_dict(include_items=True)
