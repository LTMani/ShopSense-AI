from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.services.cart_intelligence_service import CartIntelligenceService

cart_bp = Blueprint('cart_views', __name__)
cart_api_bp = Blueprint('cart_api', __name__, url_prefix='/api/cart')
cart_service = CartIntelligenceService()


@cart_bp.route('/cart')
@login_required
def cart_page():
    cart_data = cart_service.get_cart_with_intelligence(current_user.id)
    return render_template('cart/cart.html', cart=cart_data)


@cart_api_bp.route('/', methods=['GET'])
@login_required
def api_get_cart():
    cart_data = cart_service.get_cart_with_intelligence(current_user.id)
    return jsonify(cart_data)


@cart_api_bp.route('/add', methods=['POST'])
@login_required
def api_add_to_cart():
    data = request.get_json() or {}
    product_id = int(data.get('product_id', 0))
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    updated_cart = cart_service.add_to_cart(current_user.id, product_id, quantity)
    return jsonify({'success': True, 'cart': updated_cart})


@cart_api_bp.route('/update', methods=['POST'])
@login_required
def api_update_cart():
    data = request.get_json() or {}
    cart_item_id = int(data.get('cart_item_id', 0))
    quantity = int(data.get('quantity', 1))

    updated_cart = cart_service.update_quantity(current_user.id, cart_item_id, quantity)
    return jsonify({'success': True, 'cart': updated_cart})


@cart_api_bp.route('/remove/<int:cart_item_id>', methods=['DELETE', 'POST'])
@login_required
def api_remove_from_cart(cart_item_id):
    updated_cart = cart_service.remove_item(current_user.id, cart_item_id)
    return jsonify({'success': True, 'cart': updated_cart})
