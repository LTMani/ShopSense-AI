from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import AuthService
from app.schemas.user_schemas import RegisterCustomerSchema, RegisterSellerSchema, LoginSchema

auth_bp = Blueprint('auth_views', __name__)
auth_api_bp = Blueprint('auth_api', __name__, url_prefix='/api/auth')
auth_service = AuthService()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_seller:
            return redirect(url_for('seller_views.dashboard'))
        return redirect(url_for('customer_views.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        user = auth_service.authenticate_user(email, password)
        if user:
            login_user(user, remember=True)
            flash(f"Welcome back, {user.first_name}!", 'success')
            next_page = request.args.get('next')
            if user.is_seller:
                return redirect(next_page or url_for('seller_views.dashboard'))
            return redirect(next_page or url_for('customer_views.dashboard'))
        flash('Invalid email or password. Please try again.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer_views.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        phone = request.form.get('phone', '')

        try:
            auth_service.register_customer(email, password, first_name, last_name, phone)
            user = auth_service.authenticate_user(email, password)
            if user:
                login_user(user, remember=True)
                flash("Account created successfully! Welcome to ShopSense AI.", 'success')
                return redirect(url_for('customer_views.dashboard'))
        except ValueError as err:
            flash(str(err), 'danger')

    return render_template('auth/register.html')


@auth_bp.route('/seller/register', methods=['GET', 'POST'])
def seller_register():
    if current_user.is_authenticated and current_user.is_seller:
        return redirect(url_for('seller_views.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        business_name = request.form.get('business_name', '')
        phone = request.form.get('phone', '')

        try:
            auth_service.register_seller(email, password, first_name, last_name, business_name, phone=phone)
            user = auth_service.authenticate_user(email, password)
            if user:
                login_user(user, remember=True)
                flash(f"Seller store registered! Welcome, {business_name}.", 'success')
                return redirect(url_for('seller_views.dashboard'))
        except ValueError as err:
            flash(str(err), 'danger')

    return render_template('auth/seller_register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('auth_views.login'))


# JSON API Endpoints
@auth_api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    schema = LoginSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    user = auth_service.authenticate_user(data['email'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    login_user(user, remember=True)
    return jsonify({'success': True, 'user': user.to_dict(include_profile=True)})


@auth_api_bp.route('/me', methods=['GET'])
@login_required
def api_me():
    return jsonify({'user': current_user.to_dict(include_profile=True)})
