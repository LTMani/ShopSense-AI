from flask import Blueprint, render_template, request, jsonify, abort
from app.services.catalog_service import CatalogService
from app.services.search_service import SearchService
from app.services.recommendation_service import RecommendationService

product_bp = Blueprint('product_views', __name__)
product_api_bp = Blueprint('product_api', __name__, url_prefix='/api/products')
catalog_service = CatalogService()
search_service = SearchService()
rec_service = RecommendationService()


@product_bp.route('/products')
def product_list():
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    brand = request.args.get('brand')
    min_rating = request.args.get('rating', type=float)
    sort_by = request.args.get('sort', default='relevance')
    page = request.args.get('page', default=1, type=int)

    results = search_service.search(
        query='',
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        min_rating=min_rating,
        sort_by=sort_by,
        page=page,
        per_page=12
    )
    categories = catalog_service.get_categories()

    return render_template(
        'products/product_list.html',
        products=results['products'],
        total=results['total'],
        page=results['page'],
        pages=results['pages'],
        categories=categories,
        selected_category=category_id,
        sort_by=sort_by
    )


@product_bp.route('/products/<slug>')
def product_detail(slug):
    product = catalog_service.get_product_by_slug(slug, detailed=True)
    if not product:
        abort(404)

    related = catalog_service.get_related_products(product['id'], limit=4)
    alternatives = rec_service.get_smart_alternatives(product['id'], limit=3)

    return render_template(
        'products/product_detail.html',
        product=product,
        related_products=related,
        smart_alternatives=alternatives
    )


@product_api_bp.route('/', methods=['GET'])
def api_get_products():
    page = request.args.get('page', default=1, type=int)
    query = request.args.get('q', default='')
    results = search_service.search(query=query, page=page)
    return jsonify(results)


@product_api_bp.route('/<int:product_id>', methods=['GET'])
def api_get_product(product_id):
    product = catalog_service.get_product_by_id(product_id, detailed=True)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'product': product})
