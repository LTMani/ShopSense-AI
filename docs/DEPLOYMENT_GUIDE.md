# ShopSense AI — Production Deployment Guide

This guide details deployment procedures for ShopSense AI using standard WSGI containers (Gunicorn / Waitress), reverse proxies (Nginx), and PostgreSQL persistence.

---

## 1. Environment Configurations

Create a secure `.env` file in the project root:

```env
# Application Core
FLASK_ENV=production
SECRET_KEY=generate_a_cryptographically_secure_64_byte_hex_key_here
DEBUG=False

# Relational Database (PostgreSQL Production / SQLite Local)
DATABASE_URL=postgresql+psycopg2://shopsense_user:SecureDBPassword2026@localhost:5432/shopsense_db

# AI Provider Gateway (Optional — falls back to local heuristic engine if omitted)
AI_DEFAULT_PROVIDER=local
OPENAI_API_KEY=
GEMINI_API_KEY=
ANTHROPIC_API_KEY=

# Security & Sessions
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=86400
```

---

## 2. Database Initialization & Seeding

```bash
# Activate virtual environment
source venv/bin/activate

# Execute migrations and seed database
flask db upgrade
flask seed-db
```

---

## 3. WSGI Server Execution

### Linux (Gunicorn with Gevent / Sync workers):
```bash
gunicorn --workers 4 --threads 2 --bind 0.0.0.0:8000 "app:create_app('production')"
```

### Windows (Waitress):
```bash
waitress-serve --port=8000 --call "app:create_app"
```

---

## 4. Nginx Reverse Proxy Configuration

```nginx
server {
    listen 80;
    server_name shopsense.yourdomain.com;

    location /static/ {
        alias /var/www/shopsense-ai/app/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
