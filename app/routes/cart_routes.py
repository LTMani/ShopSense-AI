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
def api_get_cart():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please log in to view cart', 'requires_login': True}), 401
    cart_data = cart_service.get_cart_with_intelligence(current_user.id)
    return jsonify(cart_data)


@cart_api_bp.route('/add', methods=['POST'])
def api_add_to_cart():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please log in to add items to your cart', 'requires_login': True}), 401

    data = request.get_json(silent=True) or request.form or {}
    try:
        product_id = int(data.get('product_id', 0))
    except (ValueError, TypeError):
        product_id = 0

    try:
        quantity = int(data.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if not product_id:
        return jsonify({'error': 'A valid Product ID is required'}), 400

    try:
        updated_cart = cart_service.add_to_cart(current_user.id, product_id, quantity)
        return jsonify({'success': True, 'cart': updated_cart})
    except Exception as err:
        return jsonify({'error': str(err)}), 400


@cart_api_bp.route('/update', methods=['POST'])
def api_update_cart():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please log in to update your cart', 'requires_login': True}), 401

    data = request.get_json(silent=True) or request.form or {}
    try:
        cart_item_id = int(data.get('cart_item_id', 0))
    except (ValueError, TypeError):
        cart_item_id = 0

    try:
        quantity = int(data.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    try:
        updated_cart = cart_service.update_quantity(current_user.id, cart_item_id, quantity)
        return jsonify({'success': True, 'cart': updated_cart})
    except Exception as err:
        return jsonify({'error': str(err)}), 400


@cart_api_bp.route('/remove/<int:cart_item_id>', methods=['DELETE', 'POST'])
def api_remove_from_cart(cart_item_id):
    if not current_user.is_authenticated:
        return jsonify({'error': 'Please log in to remove items', 'requires_login': True}), 401

    try:
        updated_cart = cart_service.remove_item(current_user.id, cart_item_id)
        return jsonify({'success': True, 'cart': updated_cart})
    except Exception as err:
        return jsonify({'error': str(err)}), 400
