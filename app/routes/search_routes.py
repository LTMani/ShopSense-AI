from flask import Blueprint, render_template, request, jsonify
from app.services.search_service import SearchService
from app.services.catalog_service import CatalogService

search_bp = Blueprint('search_views', __name__)
search_api_bp = Blueprint('search_api', __name__, url_prefix='/api/search')
search_service = SearchService()
catalog_service = CatalogService()


@search_bp.route('/search')
def search():
    query = request.args.get('q', default='')
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', default='relevance')
    page = request.args.get('page', default=1, type=int)

    results = search_service.search(
        query=query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        page=page,
        per_page=12
    )
    categories = catalog_service.get_categories()

    return render_template(
        'products/search_results.html',
        query=query,
        products=results['products'],
        total=results['total'],
        page=results['page'],
        pages=results['pages'],
        categories=categories,
        extracted=results.get('extracted_filters', {})
    )


@search_api_bp.route('/', methods=['GET'])
def api_search():
    query = request.args.get('q', default='')
    page = request.args.get('page', default=1, type=int)
    results = search_service.search(query=query, page=page)
    return jsonify(results)
