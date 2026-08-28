# ShopSense AI Middleware & Schemas Generator
from pathlib import Path

BASE_MW = Path(__file__).resolve().parent.parent / 'app' / 'middleware'
BASE_SC = Path(__file__).resolve().parent.parent / 'app' / 'schemas'
BASE_MW.mkdir(parents=True, exist_ok=True)
BASE_SC.mkdir(parents=True, exist_ok=True)

# 1. auth_middleware.py
(BASE_MW / 'auth_middleware.py').write_text('''from functools import wraps
from flask import request, jsonify, redirect, url_for, flash
from flask_login import current_user


def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required', 'code': 'UNAUTHORIZED'}), 401
            flash('Please log in to continue.', 'info')
            return redirect(url_for('auth_views.login', next=request.url))
        if not current_user.is_customer and not current_user.is_admin:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Customer account required', 'code': 'FORBIDDEN'}), 403
            flash('This page is only accessible to customers.', 'warning')
            return redirect(url_for('customer_views.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Seller authentication required', 'code': 'UNAUTHORIZED'}), 401
            flash('Please log in as a seller.', 'info')
            return redirect(url_for('seller_views.seller_login', next=request.url))
        if not current_user.is_seller and not current_user.is_admin:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Seller account required', 'code': 'FORBIDDEN'}), 403
            flash('This section is restricted to seller accounts.', 'warning')
            return redirect(url_for('seller_views.dashboard'))
        return f(*args, **kwargs)
    return decorated_function
''', encoding='utf-8')

# 2. error_handlers.py
(BASE_MW / 'error_handlers.py').write_text('''import logging
from flask import render_template, request, jsonify

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Bad Request', 'message': str(error.description if hasattr(error, 'description') else error)}), 400
        return render_template('errors/400.html', error=error), 400

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Unauthorized', 'message': 'Authentication is required.'}), 401
        return render_template('errors/401.html', error=error), 401

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to perform this action.'}), 403
        return render_template('errors/403.html', error=error), 403

    @app.errorhandler(404)
    def not_found(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found.'}), 404
        return render_template('errors/404.html', error=error), 404

    @app.errorhandler(429)
    def ratelimit_exceeded(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Rate Limit Exceeded', 'message': 'Too many requests. Please slow down.'}), 429
        return render_template('errors/429.html', error=error), 429

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}", exc_info=True)
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected server error occurred.'}), 500
        return render_template('errors/500.html', error=error), 500
''', encoding='utf-8')

# 3. security_headers.py
(BASE_MW / 'security_headers.py').write_text('''def add_security_headers(app):
    @app.after_request
    def set_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response
''', encoding='utf-8')

# 4. __init__.py for middleware
(BASE_MW / '__init__.py').write_text('''from app.middleware.auth_middleware import customer_required, seller_required
from app.middleware.error_handlers import register_error_handlers
from app.middleware.security_headers import add_security_headers

__all__ = [
    'customer_required',
    'seller_required',
    'register_error_handlers',
    'add_security_headers'
]
''', encoding='utf-8')

# 5. Schemas
(BASE_SC / 'user_schemas.py').write_text('''from marshmallow import Schema, fields, validate


class RegisterCustomerSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    phone = fields.String(required=False, allow_none=True)


class RegisterSellerSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    business_name = fields.String(required=True, validate=validate.Length(min=2, max=150))
    phone = fields.String(required=False, allow_none=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
''', encoding='utf-8')

(BASE_SC / 'copilot_schemas.py').write_text('''from marshmallow import Schema, fields, validate


class CopilotMessageSchema(Schema):
    conversation_id = fields.Integer(required=False, allow_none=True)
    message = fields.String(required=True, validate=validate.Length(min=1, max=2000))
''', encoding='utf-8')

(BASE_SC / 'order_schemas.py').write_text('''from marshmallow import Schema, fields, validate


class CheckoutSchema(Schema):
    shipping_name = fields.String(required=True, validate=validate.Length(min=2, max=150))
    shipping_phone = fields.String(required=False, allow_none=True)
    shipping_address_line1 = fields.String(required=True, validate=validate.Length(min=3, max=255))
    shipping_city = fields.String(required=True, validate=validate.Length(min=2, max=100))
    shipping_state = fields.String(required=True, validate=validate.Length(min=2, max=100))
    shipping_postal_code = fields.String(required=True, validate=validate.Length(min=3, max=20))
    payment_method = fields.String(required=False, load_default='simulated_upi')
''', encoding='utf-8')

(BASE_SC / '__init__.py').write_text('''from app.schemas.user_schemas import RegisterCustomerSchema, RegisterSellerSchema, LoginSchema
from app.schemas.copilot_schemas import CopilotMessageSchema
from app.schemas.order_schemas import CheckoutSchema

__all__ = [
    'RegisterCustomerSchema',
    'RegisterSellerSchema',
    'LoginSchema',
    'CopilotMessageSchema',
    'CheckoutSchema'
]
''', encoding='utf-8')

print('Middleware & Schemas generated successfully!')
