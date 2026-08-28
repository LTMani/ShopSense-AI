from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.wishlist_intelligence_service import WishlistIntelligenceService

wishlist_bp = Blueprint('wishlist_views', __name__)
wishlist_api_bp = Blueprint('wishlist_api', __name__, url_prefix='/api/wishlist')
wishlist_service = WishlistIntelligenceService()


@wishlist_bp.route('/wishlist')
@login_required
def wishlist_page():
    wishlist_data = wishlist_service.get_wishlist_with_insights(current_user.id)
    return render_template('wishlist/wishlist.html', wishlist=wishlist_data)


@wishlist_api_bp.route('/toggle', methods=['POST'])
@login_required
def api_toggle_wishlist():
    data = request.get_json() or {}
    product_id = int(data.get('product_id', 0))
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    res = wishlist_service.toggle_wishlist(current_user.id, product_id)
    return jsonify(res)
