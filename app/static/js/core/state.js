/**
 * ShopSense AI — Global Client State Manager
 */
const ShopSenseState = {
    cartCount: 0,
    wishlistItems: new Set(),

    updateCartBadge(count) {
        this.cartCount = count;
        const el = document.getElementById('nav-cart-count');
        if (el) {
            el.textContent = count;
            el.style.display = count > 0 ? 'inline-block' : 'none';
        }
    },

    updateWishlistBadge(count) {
        const el = document.getElementById('nav-wishlist-count');
        if (el) {
            el.textContent = count;
            el.style.display = count > 0 ? 'inline-block' : 'none';
        }
    }
};

window.ShopSenseState = ShopSenseState;
