/**
 * ShopSense AI — Cart Interactions
 */
const ShopSenseCart = {
    async add(productId, quantity = 1) {
        try {
            const res = await ShopSenseAPI.post('/api/cart/add', {
                product_id: productId,
                quantity: quantity
            });
            if (res.success) {
                ShopSenseState.updateCartBadge(res.cart.total_items_count);
                ShopSenseToast.success('Item added to cart!');
            }
        } catch (err) {
            ShopSenseToast.error(err.message || 'Failed to add item to cart');
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
