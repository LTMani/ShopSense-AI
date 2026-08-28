import os
import secrets
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

INSTANCE_DIR = BASE_DIR / 'instance'
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_DB_PATH = (INSTANCE_DIR / 'shopsense.db').as_posix()


class BaseConfig:
    """Base application configuration shared across all environments."""

    PROJECT_NAME = 'ShopSense AI'
    PROJECT_VERSION = '1.0.0'
    TAGLINE = 'Shop Smarter. Sell Smarter.'
    
    # Secret Key for session signing and cryptographic tokens
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    
    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Session & Cookie Security
    SESSION_COOKIE_NAME = 'shopsense_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # AI Engine Configuration
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'local')
    AI_API_KEY = os.getenv('AI_API_KEY', '')
    AI_MODEL = os.getenv('AI_MODEL', 'local-hybrid-v1')
    AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', '0.7'))
    AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', '1024'))
    AI_TIMEOUT_SECONDS = int(os.getenv('AI_TIMEOUT_SECONDS', '15'))
    
    # Catalog and Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('PAGINATION_PER_PAGE', '12'))
    MAX_PAGE_SIZE = 50
    CURRENCY_SYMBOL = os.getenv('CURRENCY_SYMBOL', '₹')
    CURRENCY_CODE = 'INR'
    
    # Business Logic Defaults
    LOW_STOCK_THRESHOLD = 15
    OUT_OF_STOCK_THRESHOLD = 0
    CRITICAL_STOCK_THRESHOLD = 5
    DEAD_STOCK_DAYS_THRESHOLD = 60
    DEAD_STOCK_VIEW_THRESHOLD = 10
    RETURN_WINDOW_DAYS = 14
    MAX_COMPARISON_PRODUCTS = 4
    MAX_MISSION_BUDGET = 500000.0
    MIN_MISSION_BUDGET = 1000.0
    
    # Rate Limiting & Security
    RATE_LIMIT_STORAGE_URL = 'memory://'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DEFAULT_DB_PATH}'
    SESSION_COOKIE_SECURE = False
    EXPLAIN_TEMPLATE_LOADING = False


class TestingConfig(BaseConfig):
    """Testing environment configuration using in-memory or ephemeral database."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    AI_PROVIDER = 'local'


class ProductionConfig(BaseConfig):
    """Production environment configuration with hardened security settings."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{DEFAULT_DB_PATH}')
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'


CONFIG_MAP = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Resolve and return configuration instance according to environment name."""
    if not config_name:
        config_name = os.getenv('FLASK_ENV', os.getenv('ENV', 'development')).lower()
    return CONFIG_MAP.get(config_name, DevelopmentConfig)
