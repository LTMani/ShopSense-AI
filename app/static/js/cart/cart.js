/**
 * ShopSense AI — Cart Interactions
 */
const ShopSenseCart = {
    async add(productId, quantity = 1) {
        try {
            const res = await ShopSenseAPI.post('/api/cart/add', {
                product_id: parseInt(productId, 10),
                quantity: parseInt(quantity, 10) || 1
            });
            if (res.success) {
                ShopSenseState.updateCartBadge(res.cart.total_items_count);
                ShopSenseToast.success('Item added to cart!');
            }
        } catch (err) {
            const msg = err.message || '';
            if (msg.toLowerCase().includes('log in') || msg.toLowerCase().includes('auth')) {
                ShopSenseToast.info('Please sign in to add items to your cart');
                setTimeout(() => {
                    window.location.href = '/login?next=' + encodeURIComponent(window.location.pathname);
                }, 1000);
            } else {
                ShopSenseToast.error(msg || 'Failed to add item to cart');
            }
        }
    },

    async update(cartItemId, quantity) {
        try {
            const res = await ShopSenseAPI.post('/api/cart/update', {
                cart_item_id: cartItemId,
                quantity: parseInt(quantity, 10)
            });
            if (res.success) {
                ShopSenseState.updateCartBadge(res.cart.total_items_count);
                location.reload();
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Failed to update quantity');
        }
    },

    async remove(cartItemId) {
        try {
            const res = await ShopSenseAPI.post(`/api/cart/remove/${cartItemId}`);
            if (res.success) {
                ShopSenseState.updateCartBadge(res.cart.total_items_count);
                const row = document.getElementById(`cart-item-${cartItemId}`);
                if (row) row.remove();
                ShopSenseToast.info('Item removed from cart');
                setTimeout(() => location.reload(), 500);
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Failed to remove item');
        }
    }
};

window.ShopSenseCart = ShopSenseCart;
