from functools import wraps
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
            return redirect(url_for('auth_views.login', next=request.url))
        if not current_user.is_seller and not current_user.is_admin:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Seller account required', 'code': 'FORBIDDEN'}), 403
            flash('This section is restricted to seller accounts.', 'warning')
            return redirect(url_for('customer_views.dashboard'))
        return f(*args, **kwargs)
    return decorated_function
