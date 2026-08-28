from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.order_service import OrderService
from app.services.cart_intelligence_service import CartIntelligenceService
from app.repositories.order_repository import OrderRepository

order_bp = Blueprint('order_views', __name__)
order_api_bp = Blueprint('order_api', __name__, url_prefix='/api/orders')
order_service = OrderService()
cart_service = CartIntelligenceService()
order_repo = OrderRepository()


@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout_page():
    cart_data = cart_service.get_cart_with_intelligence(current_user.id)
    if cart_data['total_items_count'] == 0:
        flash("Your cart is empty.", 'warning')
        return redirect(url_for('cart_views.cart_page'))

    if request.method == 'POST':
        name = request.form.get('shipping_name', '')
        address = request.form.get('shipping_address_line1', '')
        city = request.form.get('shipping_city', '')
        state = request.form.get('shipping_state', '')
        postal_code = request.form.get('shipping_postal_code', '')
        phone = request.form.get('shipping_phone', '')
        payment_method = request.form.get('payment_method', 'simulated_upi')

        try:
            order = order_service.checkout_cart(
                user_id=current_user.id,
                shipping_name=name,
                shipping_address_line1=address,
                shipping_city=city,
                shipping_state=state,
                shipping_postal_code=postal_code,
                payment_method=payment_method,
                shipping_phone=phone
            )
            flash(f"Order #{order['order_number']} placed successfully!", 'success')
            return redirect(url_for('order_views.order_detail', order_number=order['order_number']))
        except Exception as err:
            flash(str(err), 'danger')

    return render_template('orders/checkout.html', cart=cart_data)


@order_bp.route('/orders')
@login_required
def orders_list():
    orders = order_repo.get_by_user(current_user.id)
    return render_template('orders/orders_list.html', orders=orders)


@order_bp.route('/orders/<order_number>')
@login_required
def order_detail(order_number):
    order = order_repo.get_by_order_number(order_number)
    if not order or (order.user_id != current_user.id and not current_user.is_seller and not current_user.is_admin):
        flash("Order not found.", 'danger')
        return redirect(url_for('order_views.orders_list'))

    return render_template('orders/order_detail.html', order=order.to_dict(include_items=True))
