from app.routes.auth_routes import auth_bp, auth_api_bp
from app.routes.product_routes import product_bp, product_api_bp
from app.routes.search_routes import search_bp, search_api_bp
from app.routes.copilot_routes import copilot_bp, copilot_api_bp
from app.routes.comparison_routes import compare_bp, compare_api_bp
from app.routes.review_routes import review_bp, review_api_bp
from app.routes.cart_routes import cart_bp, cart_api_bp
from app.routes.wishlist_routes import wishlist_bp, wishlist_api_bp
from app.routes.mission_routes import mission_bp, mission_api_bp
from app.routes.order_routes import order_bp, order_api_bp
from app.routes.customer_routes import customer_bp
from app.routes.seller_routes import seller_bp
from app.routes.seller_api_routes import seller_api_bp
from app.routes.system_routes import system_bp


def register_routes(app):
    """Registers all web view and RESTful API blueprints with the Flask application instance."""
    app.register_blueprint(system_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(auth_api_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(seller_api_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(product_api_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(search_api_bp)
    app.register_blueprint(copilot_bp)
    app.register_blueprint(copilot_api_bp)
    app.register_blueprint(compare_bp)
    app.register_blueprint(compare_api_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(review_api_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(cart_api_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(wishlist_api_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(mission_api_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(order_api_bp)
