from flask import Blueprint, render_template, jsonify
from app.services.catalog_service import CatalogService
from app.services.recommendation_service import RecommendationService

system_bp = Blueprint('system_views', __name__)
catalog_service = CatalogService()
rec_service = RecommendationService()


@system_bp.route('/')
def landing_page():
    categories = catalog_service.get_categories()
    featured = catalog_service.get_featured_products(limit=8)
    trending = rec_service.get_personalized_recommendations(limit=4)
    return render_template('index.html', categories=categories, featured_products=featured, trending=trending)


@system_bp.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'platform': 'ShopSense AI',
        'version': '1.0.0',
        'mode': 'production-ready'
    })


@system_bp.route('/settings')
def app_settings():
    return render_template('settings/app_settings.html')
