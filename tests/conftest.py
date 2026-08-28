import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import create_app, db
from app.seeds.seeder import run_full_seeder
from app.models.user import User


@pytest.fixture(scope='session')
def app():
    """Create and configure a clean testing Flask application instance."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        run_full_seeder()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for making HTTP requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for CLI commands."""
    return app.test_cli_runner()


@pytest.fixture
def auth_customer_client(client, app):
    """Test client logged in as a demo customer."""
    client.post('/api/auth/login', json={
        'email': 'customer@shopsense.ai',
        'password': 'CustomerPass2026!'
    })
    return client


@pytest.fixture
def auth_seller_client(client, app):
    """Test client logged in as a demo seller."""
    client.post('/api/auth/login', json={
        'email': 'seller.apex@shopsense.ai',
        'password': 'SellerPass2026!'
    })
    return client
