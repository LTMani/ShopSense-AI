# ShopSense AI Templates Generator
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'app' / 'templates'

# 1. layouts/base.html
(BASE / 'layouts' / 'base.html').write_text('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}ShopSense AI — Intelligent Shopping & Seller Platform{% endblock %}</title>
    <meta name="description" content="ShopSense AI: AI-powered e-commerce intelligence with natural-language shopping copilot, smart recommendations, product comparison, and seller analytics.">
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Base & Component CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base/variables.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base/reset.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base/typography.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/buttons.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/cards.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/badges.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/forms.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/tables.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/modals.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/navbar.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/footer.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/pages/marketplace.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body class="shopsense-app">
    <!-- Top Announcement Bar -->
    <div class="top-bar">
        <div class="container top-bar-inner">
            <div class="top-bar-left">
                <span class="badge badge-accent">AI Powered</span>
                <span class="top-bar-text">Natural-Language Shopping Copilot & Real-Time Intelligence</span>
            </div>
            <div class="top-bar-right">
                {% if is_seller %}
                    <a href="{{ url_for('seller_views.dashboard') }}" class="top-bar-link"><i data-lucide="layout-dashboard"></i> Seller Portal</a>
                {% else %}
                    <a href="{{ url_for('auth_views.seller_register') }}" class="top-bar-link"><i data-lucide="store"></i> Become a Seller</a>
                {% endif %}
                <a href="{{ url_for('system_views.app_settings') }}" class="top-bar-link"><i data-lucide="settings"></i> Settings</a>
            </div>
        </div>
    </div>

    <!-- Main Navigation Bar -->
    <header class="main-navbar sticky">
        <div class="container navbar-inner">
            <a href="{{ url_for('system_views.landing_page') }}" class="navbar-brand">
                <div class="brand-logo"><i data-lucide="sparkles"></i></div>
                <div class="brand-text">
                    <span class="brand-name">ShopSense</span>
                    <span class="brand-ai">AI</span>
                </div>
            </a>

            <!-- Search Form with Natural Language placeholder -->
            <form action="{{ url_for('search_views.search') }}" method="GET" class="nav-search-form">
                <div class="search-input-wrapper">
                    <i data-lucide="search" class="search-icon"></i>
                    <input type="text" name="q" class="nav-search-input" placeholder="Ask AI: 'Lightweight coding laptop under ₹60,000' or search products..." value="{{ request.args.get('q', '') }}">
                    <button type="submit" class="btn btn-primary btn-search"><i data-lucide="arrow-right"></i></button>
                </div>
            </form>

            <!-- Nav Actions -->
            <nav class="nav-actions">
                <a href="{{ url_for('copilot_views.copilot_page') }}" class="btn btn-copilot-pill">
                    <i data-lucide="bot"></i>
                    <span>AI Copilot</span>
                </a>
                <a href="{{ url_for('comparison_views.compare_page') }}" class="nav-icon-btn" title="Product Comparison">
                    <i data-lucide="scale"></i>
                    <span class="nav-icon-label">Compare</span>
                </a>
                <a href="{{ url_for('mission_views.missions_list') }}" class="nav-icon-btn" title="Shopping Missions">
                    <i data-lucide="compass"></i>
                    <span class="nav-icon-label">Missions</span>
                </a>
                <a href="{{ url_for('wishlist_views.wishlist_page') }}" class="nav-icon-btn" title="Wishlist">
                    <i data-lucide="heart"></i>
                    {% if wishlist_count > 0 %}
                        <span class="badge-count" id="nav-wishlist-count">{{ wishlist_count }}</span>
                    {% endif %}
                    <span class="nav-icon-label">Wishlist</span>
                </a>
                <a href="{{ url_for('cart_views.cart_page') }}" class="nav-icon-btn" title="Shopping Cart">
                    <i data-lucide="shopping-cart"></i>
                    {% if cart_count > 0 %}
                        <span class="badge-count" id="nav-cart-count">{{ cart_count }}</span>
                    {% endif %}
                    <span class="nav-icon-label">Cart</span>
                </a>

                {% if current_user.is_authenticated %}
                    <div class="user-dropdown">
                        <a href="{{ url_for('customer_views.dashboard') }}" class="btn btn-outline btn-sm user-menu-btn">
                            <i data-lucide="user"></i>
                            <span>{{ current_user.first_name }}</span>
                        </a>
                        <div class="dropdown-menu">
                            {% if current_user.is_seller %}
                                <a href="{{ url_for('seller_views.dashboard') }}" class="dropdown-item"><i data-lucide="store"></i> Seller Dashboard</a>
                            {% else %}
                                <a href="{{ url_for('customer_views.dashboard') }}" class="dropdown-item"><i data-lucide="user-check"></i> Customer Hub</a>
                                <a href="{{ url_for('order_views.orders_list') }}" class="dropdown-item"><i data-lucide="package"></i> My Orders</a>
                                <a href="{{ url_for('customer_views.profile') }}" class="dropdown-item"><i data-lucide="settings"></i> Profile Settings</a>
                            {% endif %}
                            <hr class="dropdown-divider">
                            <a href="{{ url_for('auth_views.logout') }}" class="dropdown-item text-danger"><i data-lucide="log-out"></i> Log Out</a>
                        </div>
                    </div>
                {% else %}
                    <div class="auth-buttons">
                        <a href="{{ url_for('auth_views.login') }}" class="btn btn-ghost btn-sm">Sign In</a>
                        <a href="{{ url_for('auth_views.register') }}" class="btn btn-primary btn-sm">Get Started</a>
                    </div>
                {% endif %}
            </nav>
        </div>
    </header>

    <!-- Flash Messages Container -->
    <div class="container flash-container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible">
                        <div class="alert-content">
                            <i data-lucide="{% if category == 'success' %}check-circle{% elif category == 'danger' %}alert-circle{% else %}info{% endif %}"></i>
                            <span>{{ message }}</span>
                        </div>
                        <button type="button" class="btn-close" onclick="this.parentElement.remove()">&times;</button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <!-- Main Page Content -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    <!-- Global Footer -->
    <footer class="main-footer">
        <div class="container footer-grid">
            <div class="footer-col brand-col">
                <div class="brand-logo-footer">
                    <i data-lucide="sparkles"></i>
                    <span class="brand-title">ShopSense AI</span>
                </div>
                <p class="footer-tagline">Shop Smarter. Sell Smarter. Next-generation e-commerce intelligence powered by natural-language AI.</p>
                <div class="footer-meta">
                    <span class="badge badge-outline">Flask 3.x</span>
                    <span class="badge badge-outline">SQLite & Postgres Ready</span>
                    <span class="badge badge-outline">Vanilla JS</span>
                </div>
            </div>
            <div class="footer-col">
                <h4 class="footer-heading">Customer Intelligence</h4>
                <ul class="footer-links">
                    <li><a href="{{ url_for('copilot_views.copilot_page') }}">AI Shopping Copilot</a></li>
                    <li><a href="{{ url_for('product_views.product_list') }}">Product Catalog</a></li>
                    <li><a href="{{ url_for('comparison_views.compare_page') }}">Product Comparison</a></li>
                    <li><a href="{{ url_for('mission_views.missions_list') }}">Shopping Missions</a></li>
                    <li><a href="{{ url_for('wishlist_views.wishlist_page') }}">Smart Wishlist</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4 class="footer-heading">Seller Intelligence</h4>
                <ul class="footer-links">
                    <li><a href="{{ url_for('seller_views.dashboard') }}">Seller Dashboard</a></li>
                    <li><a href="{{ url_for('seller_views.analytics') }}">Sales Analytics</a></li>
                    <li><a href="{{ url_for('seller_views.inventory') }}">Inventory Intelligence</a></li>
                    <li><a href="{{ url_for('seller_views.forecasting') }}">Demand Forecasting</a></li>
                    <li><a href="{{ url_for('seller_views.seller_copilot') }}">Seller AI Copilot</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4 class="footer-heading">Account & Support</h4>
                <ul class="footer-links">
                    <li><a href="{{ url_for('auth_views.login') }}">Customer Sign In</a></li>
                    <li><a href="{{ url_for('auth_views.seller_register') }}">Seller Onboarding</a></li>
                    <li><a href="{{ url_for('system_views.app_settings') }}">Platform Settings</a></li>
                    <li><a href="{{ url_for('system_views.health') }}">API System Health</a></li>
                </ul>
            </div>
        </div>
        <div class="container footer-bottom">
            <p>&copy; 2026 ShopSense AI Platform. All rights reserved. Built with pure Python, Flask, and Vanilla Web Standards.</p>
        </div>
    </footer>

    <!-- Toast Notification Container -->
    <div id="toast-container" class="toast-container"></div>

    <!-- Core Scripts -->
    <script src="{{ url_for('static', filename='js/core/api_client.js') }}"></script>
    <script src="{{ url_for('static', filename='js/core/toast.js') }}"></script>
    <script src="{{ url_for('static', filename='js/core/state.js') }}"></script>
    <script>
        // Initialize Lucide icons
        lucide.createIcons();
    </script>
    {% block extra_js %}{% endblock %}
</body>
</html>
''', encoding='utf-8')

# 2. layouts/seller_base.html
(BASE / 'layouts' / 'seller_base.html').write_text('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Seller Intelligence Portal — ShopSense AI{% endblock %}</title>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base/variables.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base/reset.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base/typography.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/buttons.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/cards.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/badges.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/forms.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/tables.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components/modals.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/seller/seller_portal.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body class="seller-portal-layout">
    <!-- Seller Sidebar Navigation -->
    <aside class="seller-sidebar">
        <div class="sidebar-header">
            <a href="{{ url_for('seller_views.dashboard') }}" class="seller-brand">
                <i data-lucide="sparkles" class="brand-icon"></i>
                <div class="brand-titles">
                    <span class="seller-brand-name">ShopSense</span>
                    <span class="seller-brand-badge">SELLER AI</span>
                </div>
            </a>
        </div>

        <nav class="sidebar-nav">
            <div class="nav-section-label">Core Business</div>
            <a href="{{ url_for('seller_views.dashboard') }}" class="sidebar-link {% if request.endpoint == 'seller_views.dashboard' %}active{% endif %}">
                <i data-lucide="layout-dashboard"></i>
                <span>Executive Overview</span>
            </a>
            <a href="{{ url_for('seller_views.products') }}" class="sidebar-link {% if request.endpoint == 'seller_views.products' %}active{% endif %}">
                <i data-lucide="package"></i>
                <span>Product Catalog</span>
            </a>
            <a href="{{ url_for('seller_views.inventory') }}" class="sidebar-link {% if request.endpoint == 'seller_views.inventory' %}active{% endif %}">
                <i data-lucide="boxes"></i>
                <span>Inventory Intelligence</span>
            </a>

            <div class="nav-section-label">AI & Analytics</div>
            <a href="{{ url_for('seller_views.analytics') }}" class="sidebar-link {% if request.endpoint == 'seller_views.analytics' %}active{% endif %}">
                <i data-lucide="bar-chart-3"></i>
                <span>Sales & Funnels</span>
            </a>
            <a href="{{ url_for('seller_views.forecasting') }}" class="sidebar-link {% if request.endpoint == 'seller_views.forecasting' %}active{% endif %}">
                <i data-lucide="trending-up"></i>
                <span>Demand Forecasting</span>
            </a>
            <a href="{{ url_for('seller_views.pricing') }}" class="sidebar-link {% if request.endpoint == 'seller_views.pricing' %}active{% endif %}">
                <i data-lucide="tag"></i>
                <span>Pricing Intelligence</span>
            </a>
            <a href="{{ url_for('seller_views.customers') }}" class="sidebar-link {% if request.endpoint == 'seller_views.customers' %}active{% endif %}">
                <i data-lucide="users"></i>
                <span>Customer Segments</span>
            </a>
            <a href="{{ url_for('seller_views.seller_copilot') }}" class="sidebar-link {% if request.endpoint == 'seller_views.seller_copilot' %}active{% endif %} highlight-copilot">
                <i data-lucide="bot"></i>
                <span>Seller AI Copilot</span>
            </a>

            <div class="nav-section-label">Store Settings</div>
            <a href="{{ url_for('seller_views.seller_settings') }}" class="sidebar-link {% if request.endpoint == 'seller_views.seller_settings' %}active{% endif %}">
                <i data-lucide="settings"></i>
                <span>Store Configuration</span>
            </a>
            <a href="{{ url_for('system_views.landing_page') }}" class="sidebar-link">
                <i data-lucide="external-link"></i>
                <span>Customer Marketplace</span>
            </a>
        </nav>

        <div class="sidebar-footer">
            <div class="seller-profile-card">
                <div class="seller-avatar">{{ current_user.first_name[0] }}</div>
                <div class="seller-meta">
                    <span class="seller-name">{{ current_user.seller_profile.business_name if current_user.seller_profile else current_user.first_name }}</span>
                    <span class="seller-verified"><i data-lucide="badge-check"></i> Verified Merchant</span>
                </div>
            </div>
            <a href="{{ url_for('auth_views.logout') }}" class="btn btn-ghost btn-sm btn-logout" title="Log Out"><i data-lucide="log-out"></i></a>
        </div>
    </aside>

    <!-- Main Seller Workspace Area -->
    <div class="seller-workspace">
        <header class="seller-topbar">
            <div class="topbar-title">
                <h2>{% block page_title %}Dashboard{% endblock %}</h2>
                <p class="topbar-subtitle">{% block page_subtitle %}Real-time commercial intelligence powered by database transactions.{% endblock %}</p>
            </div>
            <div class="topbar-actions">
                <span class="status-indicator online">System Live</span>
                <a href="{{ url_for('seller_views.seller_copilot') }}" class="btn btn-primary btn-sm"><i data-lucide="bot"></i> Ask Seller Copilot</a>
            </div>
        </header>

        <div class="seller-container">
            {% block content %}{% endblock %}
        </div>
    </div>

    <!-- Scripts -->
    <script src="{{ url_for('static', filename='js/core/api_client.js') }}"></script>
    <script src="{{ url_for('static', filename='js/core/toast.js') }}"></script>
    <script>
        lucide.createIcons();
    </script>
    {% block extra_js %}{% endblock %}
</body>
</html>
''', encoding='utf-8')

# 3. components/product_card.html
(BASE / 'components' / 'product_card.html').write_text('''<div class="product-card" data-product-id="{{ product.id }}">
    <div class="product-card-header">
        {% if product.discount_percentage and product.discount_percentage > 0 %}
            <span class="badge badge-sale">-{{ product.discount_percentage|int }}%</span>
        {% elif product.is_featured %}
            <span class="badge badge-featured">Featured</span>
        {% endif %}

        <button class="btn-wishlist-toggle {% if product.is_wishlisted %}active{% endif %}" onclick="ShopSenseWishlist.toggle({{ product.id }}, this)" title="Add to Wishlist">
            <i data-lucide="heart"></i>
        </button>
    </div>

    <a href="{{ url_for('product_views.product_detail', slug=product.slug) }}" class="product-img-container">
        <img src="{{ product.primary_image_url }}" alt="{{ product.title }}" class="product-image" loading="lazy">
    </a>

    <div class="product-card-body">
        <div class="product-brand-category">
            <span class="product-brand">{{ product.brand }}</span>
            <span class="product-category-tag">{{ product.category_name }}</span>
        </div>

        <h3 class="product-title">
            <a href="{{ url_for('product_views.product_detail', slug=product.slug) }}" title="{{ product.title }}">{{ product.title }}</a>
        </h3>

        <div class="product-rating">
            <div class="stars-outer">
                <i data-lucide="star" class="star-icon filled"></i>
                <span class="rating-val">{{ product.average_rating }}</span>
                <span class="reviews-count">({{ product.total_reviews_count }})</span>
            </div>
        </div>

        <p class="product-short-desc">{{ product.short_description[:90] }}...</p>

        <div class="product-price-row">
            <div class="price-box">
                <span class="current-price">{{ product.current_price|currency }}</span>
                {% if product.sale_price and product.sale_price < product.base_price %}
                    <span class="original-price">{{ product.base_price|currency }}</span>
                {% endif %}
            </div>
            <button class="btn btn-primary btn-sm btn-add-cart" onclick="ShopSenseCart.add({{ product.id }}, 1)" title="Add to Cart">
                <i data-lucide="plus"></i> Add
            </button>
        </div>
    </div>
</div>
''', encoding='utf-8')

# 4. index.html (Landing page)
(BASE / 'index.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}ShopSense AI — Intelligent Shopping & Seller Intelligence Platform{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero-section">
    <div class="container hero-grid">
        <div class="hero-text-col">
            <div class="badge badge-hero"><i data-lucide="sparkles"></i> Next-Gen E-Commerce Platform</div>
            <h1 class="hero-title">Shop Smarter. <br><span class="gradient-text">Sell Smarter.</span></h1>
            <p class="hero-description">
                Experience natural-language conversational shopping, explainable product recommendations, 
                aspect-based review intelligence, and enterprise-grade seller demand forecasting.
            </p>
            
            <div class="hero-actions">
                <a href="{{ url_for('copilot_views.copilot_page') }}" class="btn btn-primary btn-lg">
                    <i data-lucide="bot"></i> Open AI Shopping Copilot
                </a>
                <a href="{{ url_for('product_views.product_list') }}" class="btn btn-outline btn-lg">
                    <i data-lucide="grid"></i> Explore Catalog
                </a>
            </div>

            <!-- Natural Language Query Samples -->
            <div class="copilot-query-chips">
                <span class="chips-label">Try asking:</span>
                <a href="{{ url_for('search_views.search', q='laptop for coding under 60000 lightweight') }}" class="query-chip">"Coding laptop under ₹60,000 lightweight"</a>
                <a href="{{ url_for('search_views.search', q='wireless headphones with anc and great battery') }}" class="query-chip">"ANC headphones with 30hr battery"</a>
                <a href="{{ url_for('mission_views.missions_list') }}" class="query-chip">"Build college study setup for ₹30,000"</a>
            </div>
        </div>

        <div class="hero-visual-col">
            <div class="copilot-preview-card">
                <div class="preview-header">
                    <div class="copilot-avatar"><i data-lucide="bot"></i></div>
                    <div class="copilot-info">
                        <strong>ShopSense AI Copilot</strong>
                        <span class="status-online">Online & Ready</span>
                    </div>
                </div>
                <div class="preview-dialogue">
                    <div class="dialogue-msg user-msg">
                        <p>I need a laptop under ₹60,000 for coding, occasional gaming, and long battery life.</p>
                    </div>
                    <div class="dialogue-msg bot-msg">
                        <div class="extracted-pill-row">
                            <span class="pill">Category: Laptops</span>
                            <span class="pill">Budget: ₹60,000</span>
                            <span class="pill">Priority: Battery & RAM</span>
                        </div>
                        <p>I found the <strong>ThinkPad E14 Gen 5 AMD</strong> (94% Match Score). Fits your ₹56,999 budget, features 8-Core Ryzen 7, 16GB RAM, and 10+ hours battery life.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Category Showcase -->
<section class="section categories-section">
    <div class="container">
        <div class="section-header">
            <div>
                <h2 class="section-title">Explore by Category</h2>
                <p class="section-subtitle">Discover high-performance electronics and workspace essentials</p>
            </div>
            <a href="{{ url_for('product_views.product_list') }}" class="btn-link">View All Catalog &rarr;</a>
        </div>

        <div class="category-grid">
            {% for cat in categories %}
                <a href="{{ url_for('product_views.product_list', category=cat.id) }}" class="category-card">
                    <div class="cat-icon-box"><i data-lucide="{{ cat.icon_name }}"></i></div>
                    <h3 class="cat-name">{{ cat.name }}</h3>
                    <p class="cat-desc">{{ cat.description }}</p>
                </a>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Featured Products Grid -->
<section class="section featured-products-section">
    <div class="container">
        <div class="section-header">
            <div>
                <h2 class="section-title">Trending & Featured Products</h2>
                <p class="section-subtitle">Top verified ratings and recommended value champions</p>
            </div>
            <a href="{{ url_for('product_views.product_list') }}" class="btn btn-outline btn-sm">Browse All</a>
        </div>

        <div class="products-grid">
            {% for product in featured_products %}
                {% include 'components/product_card.html' %}
            {% endfor %}
        </div>
    </div>
</section>

<!-- Platform Pillars Section -->
<section class="section pillars-section">
    <div class="container">
        <div class="pillars-grid">
            <div class="pillar-card">
                <div class="pillar-icon"><i data-lucide="brain"></i></div>
                <h3>AI Shopping Copilot</h3>
                <p>Stateful multi-turn conversational assistant that extracts budgets, usage priorities, and hardware specifications to rank candidate items.</p>
            </div>
            <div class="pillar-card">
                <div class="pillar-icon"><i data-lucide="scale"></i></div>
                <h3>Intelligent Product Comparison</h3>
                <p>Side-by-side technical specification alignment with aspect-based sentiment comparisons and AI comparison verdicts.</p>
            </div>
            <div class="pillar-card">
                <div class="pillar-icon"><i data-lucide="message-square-check"></i></div>
                <h3>Aspect-Level Review Intelligence</h3>
                <p>Deep NLP sentiment extraction across battery, sound, build quality, and comfort rather than misleading single average ratings.</p>
            </div>
            <div class="pillar-card">
                <div class="pillar-icon"><i data-lucide="trending-up"></i></div>
                <h3>Seller Demand Forecasting</h3>
                <p>Mathematical time-series predictive modeling (Moving Averages, Holt-Winters) to prevent stockouts and detect dead stock.</p>
            </div>
        </div>
    </div>
</section>
{% endblock %}
''', encoding='utf-8')

print('Part 1 of templates generated successfully!')
