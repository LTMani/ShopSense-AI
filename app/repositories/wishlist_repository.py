from typing import Optional, List
from app.models.wishlist import Wishlist, WishlistItem
from app.repositories.base import BaseRepository
from app.extensions import db


class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self):
        super().__init__(Wishlist)

    def get_by_user_id(self, user_id: int) -> Optional[Wishlist]:
        wishlist = self.find_one_by(user_id=user_id)
        if not wishlist:
            wishlist = self.create(user_id=user_id, name='My Wishlist')
        return wishlist


class WishlistItemRepository(BaseRepository[WishlistItem]):
    def __init__(self):
        super().__init__(WishlistItem)

    def get_item(self, wishlist_id: int, product_id: int) -> Optional[WishlistItem]:
        return self.find_one_by(wishlist_id=wishlist_id, product_id=product_id)

    def get_price_dropped_items(self, user_id: int) -> List[WishlistItem]:
        wishlist = Wishlist.query.filter_by(user_id=user_id).first()
        if not wishlist:
            return []
        items = WishlistItem.query.filter_by(wishlist_id=wishlist.id).all()
        return [i for i in items if i.price_drop_amount > 0]
