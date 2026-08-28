from flask import Blueprint, render_template, request, jsonify
from app.services.comparison_service import ComparisonService

compare_bp = Blueprint('comparison_views', __name__)
compare_api_bp = Blueprint('compare_api', __name__, url_prefix='/api/compare')
comparison_service = ComparisonService()


@compare_bp.route('/compare')
def compare_page():
    raw_pids = request.args.get('ids', '')
    product_ids = []
    if raw_pids:
        try:
            product_ids = [int(pid.strip()) for pid in raw_pids.split(',') if pid.strip().isdigit()]
        except Exception:
            product_ids = []

    comparison_data = comparison_service.compare_products(product_ids)
    return render_template('comparison/compare.html', comparison=comparison_data, product_ids=product_ids)


@compare_api_bp.route('/', methods=['GET', 'POST'])
def api_compare():
    if request.method == 'GET':
        raw_pids = request.args.get('ids', '')
        product_ids = [int(pid.strip()) for pid in raw_pids.split(',') if pid.strip().isdigit()] if raw_pids else []
    else:
        data = request.get_json() or {}
        product_ids = data.get('product_ids', [])

    result = comparison_service.compare_products(product_ids)
    return jsonify(result)
