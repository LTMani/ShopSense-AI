import os
import logging
from flask import Flask, current_app
from flask_login import current_user
from app.config import get_config
from app.extensions import db, bcrypt, login_manager, csrf
from app.models.user import User
from app.models.cart import Cart
from app.models.wishlist import Wishlist
from app.routes import register_routes
from app.middleware import register_error_handlers, add_security_headers

# Configure standard structured logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Application factory creating, configuring, and wiring the Flask instance."""
    app = Flask(__name__, instance_relative_config=True)
    
    # 1. Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Ensure instance folder exists for SQLite persistence
    os.makedirs(app.instance_path, exist_ok=True)

    # 2. Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # 3. User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 4. Context Processors (Global template variables)
    @app.context_processor
    def inject_globals():
        cart_count = 0
        wishlist_count = 0
        if current_user.is_authenticated and current_user.is_customer:
            c = Cart.query.filter_by(user_id=current_user.id).first()
            w = Wishlist.query.filter_by(user_id=current_user.id).first()
            cart_count = c.total_items_count if c else 0
            wishlist_count = w.total_items_count if w else 0

        return {
            'app_name': app.config.get('PROJECT_NAME', 'ShopSense AI'),
            'tagline': app.config.get('TAGLINE', 'Shop Smarter. Sell Smarter.'),
            'currency_symbol': app.config.get('CURRENCY_SYMBOL', '₹'),
            'cart_count': cart_count,
            'wishlist_count': wishlist_count,
            'is_seller': current_user.is_authenticated and current_user.is_seller,
            'is_customer': current_user.is_authenticated and current_user.is_customer
        }

    # 5. Template Filters
    @app.template_filter('currency')
    def format_currency(value):
        try:
            val = float(value or 0.0)
            return f"₹{val:,.2f}"
        except (ValueError, TypeError):
            return f"₹{value}"

    @app.template_filter('dateformat')
    def format_date(value, format='%b %d, %Y'):
        if not value:
            return ""
        if isinstance(value, str):
            try:
                from datetime import datetime
                value = datetime.fromisoformat(value)
            except Exception:
                return value
        return value.strftime(format)

    # 6. Register Error Handlers & Security Headers
    register_error_handlers(app)
    add_security_headers(app)

    # 7. Register Blueprints
    register_routes(app)

    # 8. Exempt REST API Blueprints from CSRF for seamless JSON AJAX requests
    api_blueprint_names = [
        'auth_api', 'seller_api', 'product_api', 'search_api',
        'copilot_api', 'compare_api', 'review_api', 'cart_api',
        'wishlist_api', 'mission_api', 'order_api', 'system_api'
    ]
    for bp_name in api_blueprint_names:
        bp = app.blueprints.get(bp_name)
        if bp:
            csrf.exempt(bp)

    # 9. Register CLI Commands
    _register_cli_commands(app)

    logger.info(f"ShopSense AI initialized in {app.config.get('ENV', 'development')} mode.")
    return app


def _register_cli_commands(app):
    import click

    @app.cli.command('init-db')
    def init_db_command():
        """Creates database schema tables from SQLAlchemy models."""
        with app.app_context():
            db.create_all()
            click.echo("Database schema initialized successfully.")

    @app.cli.command('seed-db')
    def seed_db_command():
        """Seeds development database with realistic products, categories, reviews, and historical orders."""
        from app.seeds.seeder import run_full_seeder
        with app.app_context():
            run_full_seeder()
            click.echo("Comprehensive seed data populated successfully.")

    @app.cli.command('loc-report')
    def loc_report_command():
        """Calculates and prints authentic line of code (LOC) breakdown across all directories."""
        from scripts.loc_reporter import calculate_loc_breakdown
        report = calculate_loc_breakdown()
        click.echo(report)
