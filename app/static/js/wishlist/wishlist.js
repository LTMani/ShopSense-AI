/**
 * ShopSense AI — Wishlist Interactions
 */
const ShopSenseWishlist = {
    async toggle(productId, buttonElement) {
        try {
            const res = await ShopSenseAPI.post('/api/wishlist/toggle', { product_id: parseInt(productId, 10) });
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
            const msg = err.message || '';
            if (msg.toLowerCase().includes('log in') || msg.toLowerCase().includes('auth')) {
                ShopSenseToast.info('Please sign in to save items to your wishlist');
                setTimeout(() => {
                    window.location.href = '/login?next=' + encodeURIComponent(window.location.pathname);
                }, 1000);
            } else {
                ShopSenseToast.error(msg || 'Please log in to manage your wishlist');
            }
        }
    }
};

window.ShopSenseWishlist = ShopSenseWishlist;
