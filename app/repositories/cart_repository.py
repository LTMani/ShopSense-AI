from typing import Optional
from app.models.cart import Cart, CartItem
from app.repositories.base import BaseRepository
from app.extensions import db


class CartRepository(BaseRepository[Cart]):
    def __init__(self):
        super().__init__(Cart)

    def get_by_user_id(self, user_id: int) -> Optional[Cart]:
        cart = self.find_one_by(user_id=user_id)
        if not cart:
            cart = self.create(user_id=user_id)
        return cart


class CartItemRepository(BaseRepository[CartItem]):
    def __init__(self):
        super().__init__(CartItem)

    def get_item(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        return self.find_one_by(cart_id=cart_id, product_id=product_id)

    def clear_cart(self, cart_id: int) -> None:
        CartItem.query.filter_by(cart_id=cart_id).delete()
        db.session.commit()
