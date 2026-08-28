from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from app.services.review_intelligence_service import ReviewIntelligenceService
from app.services.catalog_service import CatalogService

review_bp = Blueprint('review_views', __name__)
review_api_bp = Blueprint('review_api', __name__, url_prefix='/api/reviews')
review_service = ReviewIntelligenceService()
catalog_service = CatalogService()


@review_bp.route('/products/<slug>/reviews')
def reviews_page(slug):
    product = catalog_service.get_product_by_slug(slug, detailed=True)
    if not product:
        abort(404)

    intel = review_service.get_review_intelligence(product['id'])
    return render_template('reviews/review_intelligence.html', product=product, intelligence=intel)


@review_api_bp.route('/<int:product_id>', methods=['GET'])
def api_get_reviews(product_id):
    intel = review_service.get_review_intelligence(product_id)
    return jsonify(intel)


@review_api_bp.route('/<int:product_id>/add', methods=['POST'])
@login_required
def api_add_review(product_id):
    data = request.get_json() or {}
    rating = int(data.get('rating', 5))
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': 'Title and review content are required'}), 400

    try:
        new_rev = review_service.add_review(product_id, current_user.id, rating, title, content)
        return jsonify({'success': True, 'review': new_rev})
    except Exception as err:
        return jsonify({'error': str(err)}), 400
