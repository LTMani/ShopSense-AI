import pytest
from app.services.auth_service import AuthService
from app.models.user import User


def test_customer_registration_and_login(app):
    with app.app_context():
        auth = AuthService()
        email = 'new_customer@test.com'
        user_dict = auth.register_customer(
            email=email,
            password='SecretPassword123!',
            first_name='Ananya',
            last_name='Iyer'
        )
        assert user_dict['email'] == email
        assert user_dict['first_name'] == 'Ananya'

        # Authenticate with valid password
        authenticated = auth.authenticate_user(email, 'SecretPassword123!')
        assert authenticated is not None
        assert authenticated.email == email

        # Authenticate with invalid password
        invalid = auth.authenticate_user(email, 'WrongPassword!')
        assert invalid is None


def test_duplicate_email_prevention(app):
    with app.app_context():
        auth = AuthService()
        with pytest.raises(ValueError):
            auth.register_customer(
                email='customer@shopsense.ai',
                password='Password123!',
                first_name='Duplicate',
                last_name='User'
            )
