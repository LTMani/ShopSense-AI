from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.repositories.order_repository import OrderRepository
from app.repositories.wishlist_repository import WishlistRepository
from app.services.recommendation_service import RecommendationService

customer_bp = Blueprint('customer_views', __name__)
order_repo = OrderRepository()
wishlist_repo = WishlistRepository()
rec_service = RecommendationService()


@customer_bp.route('/dashboard')
@customer_bp.route('/customer/dashboard')
@login_required
def dashboard():
    if current_user.is_seller:
        return redirect(url_for('seller_views.dashboard'))

    recent_orders = order_repo.get_by_user(current_user.id, limit=3)
    wishlist = wishlist_repo.get_by_user_id(current_user.id)
    recommendations = rec_service.get_personalized_recommendations(current_user.id, limit=4)

    return render_template(
        'customer/dashboard.html',
        orders=recent_orders,
        wishlist=wishlist,
        recommendations=recommendations
    )


@customer_bp.route('/profile')
@customer_bp.route('/customer/profile')
@login_required
def profile():
    return render_template('customer/profile.html', user=current_user)
