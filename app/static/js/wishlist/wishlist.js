/**
 * ShopSense AI — Wishlist Interactions
 */
const ShopSenseWishlist = {
    async toggle(productId, buttonElement) {
        try {
            const res = await ShopSenseAPI.post('/api/wishlist/toggle', { product_id: productId });
            if (buttonElement) {
                buttonElement.classList.toggle('active', res.is_wishlisted);
            }
            ShopSenseState.updateWishlistBadge(res.wishlist.total_items_count);
            if (res.is_wishlisted) {
                ShopSenseToast.success('Saved to wishlist');
            } else {
                ShopSenseToast.info('Removed from wishlist');
                const itemEl = document.getElementById(`wishlist-item-${productId}`);
                if (itemEl) itemEl.remove();
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Please log in to manage your wishlist');
        }
    }
};

window.ShopSenseWishlist = ShopSenseWishlist;
