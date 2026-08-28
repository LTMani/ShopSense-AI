from typing import Dict, Any, List
from app.models.wishlist import Wishlist, WishlistItem
from app.repositories.wishlist_repository import WishlistRepository, WishlistItemRepository
from app.repositories.product_repository import ProductRepository
from app.extensions import db


class WishlistIntelligenceService:
    """Manages saved items with price drops, back-in-stock alerts, and budget alternatives."""

    def __init__(self):
        self.wishlist_repo = WishlistRepository()
        self.wishlist_item_repo = WishlistItemRepository()
        self.product_repo = ProductRepository()

    def get_wishlist_with_insights(self, user_id: int) -> Dict[str, Any]:
        wishlist = self.wishlist_repo.get_by_user_id(user_id)
        items = wishlist.items.all()
        data = wishlist.to_dict(include_items=True)

        price_drop_total = sum(i.price_drop_amount for i in items)
        data['insights'] = {
            'total_price_drops_count': sum(1 for i in items if i.has_price_dropped),
            'total_savings_available': round(price_drop_total, 2)
        }
        return data

    def toggle_wishlist(self, user_id: int, product_id: int) -> Dict[str, Any]:
        wishlist = self.wishlist_repo.get_by_user_id(user_id)
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        item = self.wishlist_item_repo.get_item(wishlist.id, product_id)
        if item:
            self.wishlist_item_repo.delete(item)
            is_added = False
        else:
            self.wishlist_item_repo.create(
                wishlist_id=wishlist.id,
                product_id=product_id,
                price_when_added=product.current_price
            )
            is_added = True

        return {'is_wishlisted': is_added, 'wishlist': self.get_wishlist_with_insights(user_id)}
