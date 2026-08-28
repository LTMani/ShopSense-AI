# ShopSense AI Customer Platform Templates Generator
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'app' / 'templates'

# 1. auth/login.html
(BASE / 'auth' / 'login.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Sign In — ShopSense AI{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card">
        <div class="auth-header">
            <div class="auth-icon"><i data-lucide="log-in"></i></div>
            <h2>Welcome to ShopSense AI</h2>
            <p>Access your intelligent shopping copilot and personalized dashboard</p>
        </div>

        <form action="{{ url_for('auth_views.login') }}" method="POST" class="auth-form">
            <div class="form-group">
                <label for="email">Email Address</label>
                <input type="email" id="email" name="email" class="form-control" placeholder="you@example.com" required autofocus>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" class="form-control" placeholder="••••••••" required>
            </div>

            <button type="submit" class="btn btn-primary btn-block btn-lg">
                <i data-lucide="log-in"></i> Sign In to Account
            </button>
        </form>

        <div class="auth-demo-credentials">
            <h4>Quick Demo Accounts</h4>
            <div class="demo-chip-row">
                <button type="button" class="btn btn-outline btn-xs" onclick="document.getElementById('email').value='customer@shopsense.ai'; document.getElementById('password').value='CustomerPass2026!';">Customer Demo</button>
                <button type="button" class="btn btn-outline btn-xs" onclick="document.getElementById('email').value='seller.apex@shopsense.ai'; document.getElementById('password').value='SellerPass2026!';">Seller Demo</button>
            </div>
        </div>

        <div class="auth-footer">
            <p>New to ShopSense AI? <a href="{{ url_for('auth_views.register') }}">Create an account</a></p>
            <p>Merchant? <a href="{{ url_for('auth_views.seller_register') }}">Register as a seller</a></p>
        </div>
    </div>
</div>
''', encoding='utf-8')

# 2. auth/register.html
(BASE / 'auth' / 'register.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Create Customer Account — ShopSense AI{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card">
        <div class="auth-header">
            <div class="auth-icon"><i data-lucide="user-plus"></i></div>
            <h2>Create Customer Account</h2>
            <p>Join ShopSense AI for conversational recommendations and smart budget tracking</p>
        </div>

        <form action="{{ url_for('auth_views.register') }}" method="POST" class="auth-form">
            <div class="form-row-2">
                <div class="form-group">
                    <label for="first_name">First Name</label>
                    <input type="text" id="first_name" name="first_name" class="form-control" placeholder="Rohan" required>
                </div>
                <div class="form-group">
                    <label for="last_name">Last Name</label>
                    <input type="text" id="last_name" name="last_name" class="form-control" placeholder="Sharma" required>
                </div>
            </div>

            <div class="form-group">
                <label for="email">Email Address</label>
                <input type="email" id="email" name="email" class="form-control" placeholder="rohan@example.com" required>
            </div>

            <div class="form-group">
                <label for="phone">Phone Number (Optional)</label>
                <input type="tel" id="phone" name="phone" class="form-control" placeholder="+91 98765 43210">
            </div>

            <div class="form-group">
                <label for="password">Password (Minimum 6 characters)</label>
                <input type="password" id="password" name="password" class="form-control" placeholder="••••••••" minlength="6" required>
            </div>

            <button type="submit" class="btn btn-primary btn-block btn-lg">
                <i data-lucide="check-circle"></i> Complete Registration
            </button>
        </form>

        <div class="auth-footer">
            <p>Already have an account? <a href="{{ url_for('auth_views.login') }}">Sign in</a></p>
        </div>
    </div>
</div>
''', encoding='utf-8')

# 3. auth/seller_register.html
(BASE / 'auth' / 'seller_register.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Merchant Store Registration — ShopSense AI{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card auth-card-wide">
        <div class="auth-header">
            <div class="auth-icon"><i data-lucide="store"></i></div>
            <h2>Register Seller Store</h2>
            <p>Launch your storefront with demand forecasting, inventory alerts, and Seller AI Copilot</p>
        </div>

        <form action="{{ url_for('auth_views.seller_register') }}" method="POST" class="auth-form">
            <div class="form-group">
                <label for="business_name">Store / Business Name</label>
                <input type="text" id="business_name" name="business_name" class="form-control" placeholder="Apex Tech Innovations" required>
            </div>

            <div class="form-row-2">
                <div class="form-group">
                    <label for="first_name">Owner First Name</label>
                    <input type="text" id="first_name" name="first_name" class="form-control" placeholder="Vikram" required>
                </div>
                <div class="form-group">
                    <label for="last_name">Owner Last Name</label>
                    <input type="text" id="last_name" name="last_name" class="form-control" placeholder="Menon" required>
                </div>
            </div>

            <div class="form-row-2">
                <div class="form-group">
                    <label for="email">Business Email</label>
                    <input type="email" id="email" name="email" class="form-control" placeholder="partner@apextech.in" required>
                </div>
                <div class="form-group">
                    <label for="phone">Business Contact Phone</label>
                    <input type="tel" id="phone" name="phone" class="form-control" placeholder="+91 98450 12345">
                </div>
            </div>

            <div class="form-group">
                <label for="password">Account Password</label>
                <input type="password" id="password" name="password" class="form-control" placeholder="••••••••" minlength="6" required>
            </div>

            <button type="submit" class="btn btn-primary btn-block btn-lg">
                <i data-lucide="store"></i> Register & Launch Seller Portal
            </button>
        </form>

        <div class="auth-footer">
            <p>Already a registered merchant? <a href="{{ url_for('auth_views.login') }}">Seller Login</a></p>
        </div>
    </div>
</div>
''', encoding='utf-8')

# 4. products/product_list.html
(BASE / 'products' / 'product_list.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Product Catalog — ShopSense AI{% endblock %}

{% block content %}
<div class="container catalog-page">
    <div class="catalog-header">
        <div>
            <h1>Product Marketplace</h1>
            <p>Showing {{ total }} verified catalog products with real-time stock levels</p>
        </div>
        <div class="catalog-sort">
            <label for="sort-select">Sort by:</label>
            <select id="sort-select" class="form-control select-inline" onchange="location = this.value;">
                <option value="{{ url_for('product_views.product_list', sort='relevance') }}" {% if sort_by == 'relevance' %}selected{% endif %}>AI Relevance</option>
                <option value="{{ url_for('product_views.product_list', sort='price_asc') }}" {% if sort_by == 'price_asc' %}selected{% endif %}>Price: Low to High</option>
                <option value="{{ url_for('product_views.product_list', sort='price_desc') }}" {% if sort_by == 'price_desc' %}selected{% endif %}>Price: High to Low</option>
                <option value="{{ url_for('product_views.product_list', sort='rating') }}" {% if sort_by == 'rating' %}selected{% endif %}>Highest Rated</option>
                <option value="{{ url_for('product_views.product_list', sort='popularity') }}" {% if sort_by == 'popularity' %}selected{% endif %}>Popularity</option>
            </select>
        </div>
    </div>

    <div class="catalog-layout">
        <!-- Filter Sidebar -->
        <aside class="catalog-sidebar">
            <div class="filter-card">
                <h3>Categories</h3>
                <ul class="filter-list">
                    <li><a href="{{ url_for('product_views.product_list') }}" class="{% if not selected_category %}active{% endif %}">All Categories</a></li>
                    {% for cat in categories %}
                        <li>
                            <a href="{{ url_for('product_views.product_list', category=cat.id) }}" class="{% if selected_category == cat.id %}active{% endif %}">
                                <i data-lucide="{{ cat.icon_name }}"></i> {{ cat.name }}
                            </a>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        </aside>

        <!-- Product Grid -->
        <div class="catalog-main">
            <div class="products-grid">
                {% for product in products %}
                    {% include 'components/product_card.html' %}
                {% endfor %}
            </div>

            <!-- Pagination -->
            {% if pages > 1 %}
                <div class="pagination">
                    {% if page > 1 %}
                        <a href="{{ url_for('product_views.product_list', page=page-1, category=selected_category, sort=sort_by) }}" class="btn btn-outline btn-sm">&larr; Previous</a>
                    {% endif %}
                    <span class="pagination-info">Page {{ page }} of {{ pages }}</span>
                    {% if page < pages %}
                        <a href="{{ url_for('product_views.product_list', page=page+1, category=selected_category, sort=sort_by) }}" class="btn btn-outline btn-sm">Next &rarr;</a>
                    {% endif %}
                </div>
            {% endif %}
        </div>
    </div>
</div>
''', encoding='utf-8')

# 5. products/search_results.html
(BASE / 'products' / 'search_results.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Search: {{ query }} — ShopSense AI{% endblock %}

{% block content %}
<div class="container search-results-page">
    <div class="search-hero-box">
        <h1>Search Results for <span class="highlight">"{{ query }}"</span></h1>
        <p>Found {{ total }} matching items using hybrid semantic NLP ranking.</p>

        {% if extracted %}
            <div class="extracted-chips-row">
                <span class="chips-label">AI Detected Constraints:</span>
                {% if extracted.budget %}<span class="badge badge-accent">Budget: ₹{{ "{:,.0f}".format(extracted.budget) }}</span>{% endif %}
                {% if extracted.category %}<span class="badge badge-outline">Category: {{ extracted.category }}</span>{% endif %}
                {% if extracted.brand %}<span class="badge badge-outline">Brand: {{ extracted.brand }}</span>{% endif %}
                {% for u in extracted.usage %}<span class="badge badge-outline">Focus: {{ u }}</span>{% endfor %}
            </div>
        {% endif %}
    </div>

    <div class="products-grid">
        {% for product in products %}
            {% include 'components/product_card.html' %}
        {% else %}
            <div class="empty-state">
                <i data-lucide="search-x" class="empty-icon"></i>
                <h3>No exact matches found</h3>
                <p>Try refining your query or asking the AI Shopping Copilot.</p>
                <a href="{{ url_for('copilot_views.copilot_page') }}" class="btn btn-primary">Open AI Shopping Copilot</a>
            </div>
        {% endfor %}
    </div>
</div>
''', encoding='utf-8')

# 6. products/product_detail.html
(BASE / 'products' / 'product_detail.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}{{ product.title }} — ShopSense AI{% endblock %}

{% block content %}
<div class="container product-detail-container">
    <div class="product-detail-grid">
        <!-- Gallery -->
        <div class="product-gallery">
            <div class="main-image-box">
                <img src="{{ product.primary_image_url }}" alt="{{ product.title }}" class="main-prod-img" id="main-image">
            </div>
        </div>

        <!-- Info & Actions -->
        <div class="product-info-col">
            <div class="product-brand-badge">{{ product.brand }}</div>
            <h1 class="product-detail-title">{{ product.title }}</h1>
            
            <div class="product-detail-rating">
                <span class="stars-score"><i data-lucide="star" class="star-icon filled"></i> {{ product.average_rating }}</span>
                <a href="{{ url_for('review_views.reviews_page', slug=product.slug) }}" class="review-link">({{ product.total_reviews_count }} verified buyer reviews & sentiment report)</a>
            </div>

            <div class="product-detail-price-box">
                <span class="detail-current-price">{{ product.current_price|currency }}</span>
                {% if product.sale_price and product.sale_price < product.base_price %}
                    <span class="detail-base-price">{{ product.base_price|currency }}</span>
                    <span class="badge badge-sale">Save {{ product.discount_percentage|int }}%</span>
                {% endif %}
            </div>

            <p class="product-detail-desc">{{ product.description }}</p>

            <div class="product-specs-highlights">
                <h4>Key Technical Specifications:</h4>
                <ul class="specs-bullet-list">
                    {% for feat in product.key_features %}
                        <li><i data-lucide="check" class="check-icon"></i> {{ feat }}</li>
                    {% endfor %}
                </ul>
            </div>

            <!-- Aspect Sentiment Meter -->
            <div class="aspect-sentiment-box">
                <h4>Aspect Sentiment Breakdown:</h4>
                <div class="aspect-bars">
                    {% for aspect, score in product.aspect_sentiments.items() %}
                        <div class="aspect-bar-row">
                            <span class="aspect-name">{{ aspect|capitalize }}</span>
                            <div class="progress-bar-track">
                                <div class="progress-bar-fill {% if score >= 85 %}good{% elif score >= 70 %}moderate{% else %}low{% endif %}" style="width: {{ score }}%;"></div>
                            </div>
                            <span class="aspect-score">{{ score }}% Positive</span>
                        </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="product-actions-row">
                <button class="btn btn-primary btn-lg" onclick="ShopSenseCart.add({{ product.id }}, 1)">
                    <i data-lucide="shopping-cart"></i> Add to Cart
                </button>
                <a href="{{ url_for('comparison_views.compare_page', ids=product.id) }}" class="btn btn-outline btn-lg">
                    <i data-lucide="scale"></i> Add to Compare
                </a>
                <button class="btn btn-ghost btn-lg" onclick="ShopSenseWishlist.toggle({{ product.id }}, this)">
                    <i data-lucide="heart"></i> Save
                </button>
            </div>
        </div>
    </div>

    <!-- Smart Alternatives Section -->
    {% if smart_alternatives.budget_alternatives or smart_alternatives.premium_upgrades %}
        <section class="section smart-alternatives-section">
            <h2>Smart Alternatives & Recommendations</h2>
            <div class="alternatives-grid">
                {% for alt in smart_alternatives.budget_alternatives %}
                    <div class="alternative-card budget-alt">
                        <span class="alt-tag badge-sale">Budget Saver Option</span>
                        <h4>{{ alt.product.title }}</h4>
                        <p class="alt-reason">{{ alt.explanation }}</p>
                        <div class="alt-price-row">
                            <span class="alt-price">{{ alt.product.current_price|currency }}</span>
                            <a href="{{ url_for('product_views.product_detail', slug=alt.product.slug) }}" class="btn btn-outline btn-sm">View Item</a>
                        </div>
                    </div>
                {% endfor %}

                {% for alt in smart_alternatives.premium_upgrades %}
                    <div class="alternative-card premium-alt">
                        <span class="alt-tag badge-accent">Performance Upgrade</span>
                        <h4>{{ alt.product.title }}</h4>
                        <p class="alt-reason">{{ alt.explanation }}</p>
                        <div class="alt-price-row">
                            <span class="alt-price">{{ alt.product.current_price|currency }}</span>
                            <a href="{{ url_for('product_views.product_detail', slug=alt.product.slug) }}" class="btn btn-outline btn-sm">View Item</a>
                        </div>
                    </div>
                {% endfor %}
            </div>
        </section>
    {% endif %}
</div>
''', encoding='utf-8')

# 7. copilot/copilot.html
(BASE / 'copilot' / 'copilot.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}AI Shopping Copilot — ShopSense AI{% endblock %}

{% block content %}
<div class="container copilot-page-layout">
    <!-- Conversation Sidebar -->
    <aside class="copilot-sidebar">
        <div class="sidebar-top">
            <button class="btn btn-primary btn-block" onclick="ShopSenseCopilot.newSession()">
                <i data-lucide="plus"></i> New Shopping Session
            </button>
        </div>
        <div class="sessions-list">
            <h4>Recent Sessions</h4>
            {% for conv in conversations %}
                <div class="session-item" onclick="ShopSenseCopilot.loadSession({{ conv.id }})">
                    <i data-lucide="message-square"></i>
                    <span>{{ conv.session_title }}</span>
                </div>
            {% endfor %}
        </div>
    </aside>

    <!-- Main Chat Workspace -->
    <div class="copilot-chat-workspace">
        <div class="chat-header">
            <div class="copilot-brand-badge">
                <i data-lucide="bot"></i>
                <div>
                    <h3>ShopSense AI Shopping Copilot</h3>
                    <p>Natural-language requirements, adaptive ranking, and grounded explanations</p>
                </div>
            </div>
        </div>

        <!-- Chat Stream Area -->
        <div class="chat-stream" id="chat-stream">
            <div class="chat-bubble bot">
                <div class="bot-avatar"><i data-lucide="bot"></i></div>
                <div class="bubble-content">
                    <p>Hello! I am your AI Shopping Copilot. Tell me what you're looking for, your budget ceiling, and key usage priorities (e.g. <em>"I need a laptop under ₹60,000 for coding, occasional gaming, and long battery life"</em>).</p>
                </div>
            </div>
        </div>

        <!-- Input Bar -->
        <div class="chat-input-bar">
            <form id="copilot-form" onsubmit="ShopSenseCopilot.sendMessage(event)">
                <input type="text" id="copilot-input" class="form-control" placeholder="Describe your shopping requirements or refine: 'Battery matters more than gaming'..." autofocus>
                <button type="submit" class="btn btn-primary" id="btn-send-copilot"><i data-lucide="send"></i></button>
            </form>
        </div>
    </div>
</div>
''', encoding='utf-8')

# 8. comparison/compare.html
(BASE / 'comparison' / 'compare.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Product Comparison Matrix — ShopSense AI{% endblock %}

{% block content %}
<div class="container comparison-page">
    <div class="comparison-header">
        <h1>Intelligent Product Comparison</h1>
        <p>Side-by-side technical specification alignment and AI diagnostic verdict</p>
    </div>

    {% if comparison.products %}
        <!-- AI Comparison Verdict Box -->
        {% if comparison.verdict %}
            <div class="comparison-verdict-box">
                <div class="verdict-icon"><i data-lucide="sparkles"></i></div>
                <div class="verdict-content">
                    <h4>AI Comparison Verdict</h4>
                    <p>{{ comparison.verdict|safe }}</p>
                </div>
            </div>
        {% endif %}

        <!-- Comparison Table -->
        <div class="comparison-table-wrapper">
            <table class="table comparison-table">
                <thead>
                    <tr>
                        <th class="feature-col">Product / Feature</th>
                        {% for p in comparison.products %}
                            <th class="product-col">
                                <img src="{{ p.primary_image_url }}" alt="{{ p.title }}" class="compare-thumb">
                                <h3>{{ p.title }}</h3>
                                <span class="compare-price">{{ p.current_price|currency }}</span>
                                <button class="btn btn-primary btn-xs" onclick="ShopSenseCart.add({{ p.id }}, 1)">Add to Cart</button>
                            </th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    <tr class="section-divider-row"><td colspan="{{ comparison.products|length + 1 }}">Rating & Sentiment</td></tr>
                    <tr>
                        <td class="spec-label">Customer Rating</td>
                        {% for p in comparison.products %}
                            <td><strong>{{ p.average_rating }}★</strong> ({{ p.total_reviews_count }} reviews)</td>
                        {% endfor %}
                    </tr>
                    {% for aspect, scores in comparison.aspects_matrix.items() %}
                        <tr>
                            <td class="spec-label">{{ aspect|capitalize }} Satisfaction</td>
                            {% for p in comparison.products %}
                                <td>{{ scores.get(p.id, '—') }}% Positive</td>
                            {% endfor %}
                        </tr>
                    {% endfor %}

                    <tr class="section-divider-row"><td colspan="{{ comparison.products|length + 1 }}">Technical Specifications</td></tr>
                    {% for spec_name, vals in comparison.attributes_matrix.items() %}
                        <tr>
                            <td class="spec-label">{{ spec_name }}</td>
                            {% for p in comparison.products %}
                                <td>{{ vals.get(p.id, '—') }}</td>
                            {% endfor %}
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% else %}
        <div class="empty-state">
            <i data-lucide="scale" class="empty-icon"></i>
            <h3>No products selected for comparison</h3>
            <p>Browse products and click "Add to Compare" on any 2 to 4 items.</p>
            <a href="{{ url_for('product_views.product_list') }}" class="btn btn-primary">Browse Marketplace</a>
        </div>
    {% endif %}
</div>
''', encoding='utf-8')

# 9. cart/cart.html
(BASE / 'cart' / 'cart.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Shopping Cart — ShopSense AI{% endblock %}

{% block content %}
<div class="container cart-page">
    <h1>Your Shopping Cart</h1>

    {% if cart.items %}
        <div class="cart-grid">
            <div class="cart-items-col">
                <!-- Smart Insights Box -->
                {% if cart.intelligence.insights %}
                    <div class="cart-insights-box">
                        <div class="insight-header"><i data-lucide="sparkles"></i> <strong>Smart Cart Intelligence</strong></div>
                        {% for ins in cart.intelligence.insights %}
                            <div class="insight-item">
                                <i data-lucide="info"></i>
                                <span>{{ ins.message }}</span>
                            </div>
                        {% endfor %}
                    </div>
                {% endif %}

                <!-- Items List -->
                <div class="cart-items-list">
                    {% for item in cart.items %}
                        <div class="cart-item-row" id="cart-item-{{ item.id }}">
                            <img src="{{ item.product.primary_image_url }}" alt="{{ item.product.title }}" class="cart-item-img">
                            <div class="cart-item-details">
                                <h3><a href="{{ url_for('product_views.product_detail', slug=item.product.slug) }}">{{ item.product.title }}</a></h3>
                                <span class="cart-item-unit-price">{{ item.unit_price|currency }}</span>
                            </div>
                            <div class="cart-item-qty">
                                <input type="number" class="form-control qty-input" value="{{ item.quantity }}" min="1" max="10" onchange="ShopSenseCart.update({{ item.id }}, this.value)">
                            </div>
                            <div class="cart-item-total">
                                <span>{{ item.total_price|currency }}</span>
                            </div>
                            <button class="btn-remove-item" onclick="ShopSenseCart.remove({{ item.id }})" title="Remove item">&times;</button>
                        </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Order Summary -->
            <div class="cart-summary-col">
                <div class="summary-card">
                    <h3>Order Summary</h3>
                    <div class="summary-row">
                        <span>Subtotal ({{ cart.total_items_count }} items)</span>
                        <span>{{ cart.subtotal_amount|currency }}</span>
                    </div>
                    <div class="summary-row">
                        <span>Shipping</span>
                        <span>{% if cart.intelligence.free_shipping_eligible %}FREE{% else %}₹99.00{% endif %}</span>
                    </div>
                    <div class="summary-row">
                        <span>Estimated Tax (18% GST)</span>
                        <span>{{ (cart.subtotal_amount * 0.18)|currency }}</span>
                    </div>
                    <hr>
                    <div class="summary-row total-row">
                        <strong>Total Amount</strong>
                        <strong>{{ (cart.subtotal_amount * 1.18)|currency }}</strong>
                    </div>

                    <a href="{{ url_for('order_views.checkout_page') }}" class="btn btn-primary btn-block btn-lg btn-checkout">
                        <i data-lucide="shield-check"></i> Proceed to Simulated Checkout
                    </a>
                </div>
            </div>
        </div>
    {% else %}
        <div class="empty-state">
            <i data-lucide="shopping-cart" class="empty-icon"></i>
            <h3>Your cart is empty</h3>
            <p>Explore our AI recommendations and catalog to add products.</p>
            <a href="{{ url_for('product_views.product_list') }}" class="btn btn-primary">Start Shopping</a>
        </div>
    {% endif %}
</div>
''', encoding='utf-8')

# 10. wishlist/wishlist.html
(BASE / 'wishlist' / 'wishlist.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Smart Wishlist — ShopSense AI{% endblock %}

{% block content %}
<div class="container wishlist-page">
    <div class="wishlist-header">
        <div>
            <h1>Intelligent Wishlist</h1>
            <p>Track price drops, availability, and alternative recommendations</p>
        </div>
    </div>

    {% if wishlist.items %}
        {% if wishlist.insights.total_price_drops_count > 0 %}
            <div class="alert alert-success">
                <i data-lucide="trending-down"></i>
                <span>Great news! <strong>{{ wishlist.insights.total_price_drops_count }}</strong> items in your wishlist have dropped in price. Total savings: <strong>{{ wishlist.insights.total_savings_available|currency }}</strong>.</span>
            </div>
        {% endif %}

        <div class="products-grid">
            {% for item in wishlist.items %}
                <div class="product-card" id="wishlist-item-{{ item.id }}">
                    {% if item.has_price_dropped %}
                        <span class="badge badge-sale">Price Drop: Save {{ item.price_drop_amount|currency }}</span>
                    {% endif %}
                    <a href="{{ url_for('product_views.product_detail', slug=item.product.slug) }}">
                        <img src="{{ item.product.primary_image_url }}" alt="{{ item.product.title }}" class="product-image">
                    </a>
                    <div class="product-card-body">
                        <h3>{{ item.product.title }}</h3>
                        <div class="price-box">
                            <span class="current-price">{{ item.current_price|currency }}</span>
                        </div>
                        <div class="product-actions-row">
                            <button class="btn btn-primary btn-sm" onclick="ShopSenseCart.add({{ item.product_id }}, 1)">Add to Cart</button>
                            <button class="btn btn-outline btn-sm" onclick="ShopSenseWishlist.toggle({{ item.product_id }}, this)">Remove</button>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="empty-state">
            <i data-lucide="heart" class="empty-icon"></i>
            <h3>Your wishlist is empty</h3>
            <p>Save items as you browse to track prices and stock changes.</p>
            <a href="{{ url_for('product_views.product_list') }}" class="btn btn-primary">Discover Products</a>
        </div>
    {% endif %}
</div>
''', encoding='utf-8')

# 11. missions/missions_list.html
(BASE / 'missions' / 'missions_list.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Shopping Missions — ShopSense AI{% endblock %}

{% block content %}
<div class="container missions-page">
    <div class="missions-hero">
        <div class="badge badge-accent"><i data-lucide="compass"></i> Multi-Product Basket Goal Solver</div>
        <h1>Shopping Missions</h1>
        <p>Set a goal and total budget ceiling (e.g. <em>"Build college study setup under ₹30,000"</em>). Our constraint optimizer allocates budget slots and selects compatible, highly rated items.</p>
    </div>

    <!-- Mission Builder Form Card -->
    <div class="mission-builder-card">
        <h3>Launch a New Shopping Mission</h3>
        <form onsubmit="ShopSenseMissions.build(event)">
            <div class="form-group">
                <label for="mission-prompt">What are you trying to assemble?</label>
                <input type="text" id="mission-prompt" class="form-control" placeholder="e.g., Complete college study setup with laptop, monitor, and desk chair" required>
            </div>
            <div class="form-row-2">
                <div class="form-group">
                    <label for="mission-budget">Total Maximum Budget (₹)</label>
                    <input type="number" id="mission-budget" class="form-control" value="30000" min="1000" max="500000" step="500" required>
                </div>
                <div class="form-group">
                    <label for="mission-mode">Optimization Strategy</label>
                    <select id="mission-mode" class="form-control">
                        <option value="balanced">Balanced Value & Quality</option>
                        <option value="performance_first">Prioritize Maximum Performance</option>
                        <option value="budget_saver">Maximize Budget Savings</option>
                    </select>
                </div>
            </div>
            <button type="submit" class="btn btn-primary btn-lg" id="btn-build-mission">
                <i data-lucide="sparkles"></i> Generate Optimized Basket
            </button>
        </form>
    </div>

    <!-- Result Basket Display Area -->
    <div id="mission-result-area"></div>
</div>
''', encoding='utf-8')

# 12. orders/checkout.html
(BASE / 'orders' / 'checkout.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Simulated Checkout — ShopSense AI{% endblock %}

{% block content %}
<div class="container checkout-page">
    <h1>Simulated Order Checkout</h1>
    <p class="text-muted">ShopSense AI internal simulation checkout (No real payment processing required).</p>

    <form action="{{ url_for('order_views.checkout_page') }}" method="POST" class="checkout-grid">
        <div class="checkout-form-col">
            <div class="checkout-card">
                <h3>1. Delivery Address</h3>
                <div class="form-group">
                    <label for="shipping_name">Full Recipient Name</label>
                    <input type="text" id="shipping_name" name="shipping_name" class="form-control" value="{{ current_user.full_name }}" required>
                </div>
                <div class="form-group">
                    <label for="shipping_phone">Contact Phone</label>
                    <input type="tel" id="shipping_phone" name="shipping_phone" class="form-control" value="{{ current_user.phone or '+91 9876543210' }}">
                </div>
                <div class="form-group">
                    <label for="shipping_address_line1">Street Address</label>
                    <input type="text" id="shipping_address_line1" name="shipping_address_line1" class="form-control" value="Flat 402, Green Glen Heights, Bellandur" required>
                </div>
                <div class="form-row-3">
                    <div class="form-group">
                        <label for="shipping_city">City</label>
                        <input type="text" id="shipping_city" name="shipping_city" class="form-control" value="Bengaluru" required>
                    </div>
                    <div class="form-group">
                        <label for="shipping_state">State</label>
                        <input type="text" id="shipping_state" name="shipping_state" class="form-control" value="Karnataka" required>
                    </div>
                    <div class="form-group">
                        <label for="shipping_postal_code">PIN Code</label>
                        <input type="text" id="shipping_postal_code" name="shipping_postal_code" class="form-control" value="560103" required>
                    </div>
                </div>
            </div>

            <div class="checkout-card">
                <h3>2. Payment Method (Simulated)</h3>
                <div class="payment-options">
                    <label class="payment-radio-card">
                        <input type="radio" name="payment_method" value="simulated_upi" checked>
                        <div class="radio-content">
                            <strong>Simulated UPI / Instant Pay</strong>
                            <p>Instant virtual transaction confirmation</p>
                        </div>
                    </label>
                    <label class="payment-radio-card">
                        <input type="radio" name="payment_method" value="simulated_card">
                        <div class="radio-content">
                            <strong>Simulated Credit / Debit Card</strong>
                            <p>Test token checkout</p>
                        </div>
                    </label>
                </div>
            </div>
        </div>

        <div class="checkout-summary-col">
            <div class="summary-card">
                <h3>Order Review ({{ cart.total_items_count }} items)</h3>
                <div class="checkout-items-preview">
                    {% for item in cart.items %}
                        <div class="checkout-item-line">
                            <span>{{ item.product.title[:30] }}... &times; {{ item.quantity }}</span>
                            <span>{{ item.total_price|currency }}</span>
                        </div>
                    {% endfor %}
                </div>
                <hr>
                <div class="summary-row">
                    <span>Subtotal</span>
                    <span>{{ cart.subtotal_amount|currency }}</span>
                </div>
                <div class="summary-row">
                    <span>18% GST</span>
                    <span>{{ (cart.subtotal_amount * 0.18)|currency }}</span>
                </div>
                <div class="summary-row total-row">
                    <strong>Total to Pay</strong>
                    <strong>{{ (cart.subtotal_amount * 1.18)|currency }}</strong>
                </div>

                <button type="submit" class="btn btn-primary btn-block btn-lg">
                    <i data-lucide="check"></i> Confirm & Complete Order
                </button>
            </div>
        </div>
    </form>
</div>
''', encoding='utf-8')

# 13. orders/orders_list.html
(BASE / 'orders' / 'orders_list.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Order History — ShopSense AI{% endblock %}

{% block content %}
<div class="container orders-page">
    <h1>Your Order History</h1>
    <p>Track past orders and delivery progress</p>

    <div class="orders-list">
        {% for order in orders %}
            <div class="order-card">
                <div class="order-card-header">
                    <div>
                        <span class="order-number">Order #{{ order.order_number }}</span>
                        <span class="order-date">Placed on {{ order.created_at|dateformat }}</span>
                    </div>
                    <div class="order-status-badge badge-{{ order.status }}">{{ order.status|capitalize }}</div>
                </div>
                <div class="order-card-body">
                    <div class="order-summary-metrics">
                        <span>Total: <strong>{{ order.total_amount|currency }}</strong></span>
                        <span>Items: <strong>{{ order.items.count() }}</strong></span>
                    </div>
                    <a href="{{ url_for('order_views.order_detail', order_number=order.order_number) }}" class="btn btn-outline btn-sm">View Details & Invoice</a>
                </div>
            </div>
        {% else %}
            <div class="empty-state">
                <i data-lucide="package" class="empty-icon"></i>
                <h3>No past orders found</h3>
                <a href="{{ url_for('product_views.product_list') }}" class="btn btn-primary">Start Shopping</a>
            </div>
        {% endfor %}
    </div>
</div>
''', encoding='utf-8')

# 14. orders/order_detail.html
(BASE / 'orders' / 'order_detail.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Order #{{ order.order_number }} — ShopSense AI{% endblock %}

{% block content %}
<div class="container order-detail-page">
    <div class="order-header-box">
        <div class="badge badge-success"><i data-lucide="check-circle"></i> Confirmed Order</div>
        <h1>Order #{{ order.order_number }}</h1>
        <p>Placed on {{ order.created_at|dateformat }} &bull; Status: <strong class="badge-{{ order.status }}">{{ order.status|capitalize }}</strong></p>
    </div>

    <div class="order-detail-grid">
        <div class="order-items-col">
            <div class="card">
                <h3>Items in Order</h3>
                <div class="order-lines-list">
                    {% for item in order.items %}
                        <div class="order-line-row">
                            <div>
                                <h4>{{ item.product_title }}</h4>
                                <span class="sku-label">SKU: {{ item.product_sku }}</span>
                            </div>
                            <div class="order-line-qty">Qty: {{ item.quantity }}</div>
                            <div class="order-line-price">{{ item.total_price|currency }}</div>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <div class="order-info-col">
            <div class="card">
                <h3>Delivery Address</h3>
                <p><strong>{{ order.shipping_address.name }}</strong></p>
                <p>{{ order.shipping_address.line1 }}</p>
                <p>{{ order.shipping_address.city }}, {{ order.shipping_address.state }} - {{ order.shipping_address.postal_code }}</p>
            </div>

            <div class="card">
                <h3>Payment Summary</h3>
                <div class="summary-row"><span>Subtotal:</span><span>{{ order.subtotal_amount|currency }}</span></div>
                <div class="summary-row"><span>GST (18%):</span><span>{{ order.tax_amount|currency }}</span></div>
                <div class="summary-row"><span>Shipping:</span><span>{{ order.shipping_fee|currency }}</span></div>
                <hr>
                <div class="summary-row total-row"><strong>Total Paid:</strong><strong>{{ order.total_amount|currency }}</strong></div>
            </div>
        </div>
    </div>
</div>
''', encoding='utf-8')

# 15. customer/dashboard.html
(BASE / 'customer' / 'dashboard.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Customer Dashboard — ShopSense AI{% endblock %}

{% block content %}
<div class="container customer-dashboard">
    <div class="dashboard-hero">
        <div class="welcome-col">
            <h1>Welcome, {{ current_user.first_name }}!</h1>
            <p>Your personalized shopping hub powered by ShopSense AI</p>
        </div>
        <div class="quick-copilot-cta">
            <a href="{{ url_for('copilot_views.copilot_page') }}" class="btn btn-primary">
                <i data-lucide="bot"></i> Open AI Shopping Copilot
            </a>
        </div>
    </div>

    <!-- Recent Orders & Wishlist -->
    <div class="dashboard-grid">
        <div class="dash-card">
            <div class="dash-card-header">
                <h3><i data-lucide="package"></i> Recent Orders</h3>
                <a href="{{ url_for('order_views.orders_list') }}" class="btn-link">View All</a>
            </div>
            {% if orders %}
                <ul class="dash-list">
                    {% for order in orders %}
                        <li class="dash-list-item">
                            <div>
                                <strong>Order #{{ order.order_number }}</strong>
                                <span class="text-muted">{{ order.created_at|dateformat }}</span>
                            </div>
                            <span class="badge badge-{{ order.status }}">{{ order.status|capitalize }}</span>
                        </li>
                    {% endfor %}
                </ul>
            {% else %}
                <p class="text-muted">No orders placed yet.</p>
            {% endif %}
        </div>

        <div class="dash-card">
            <div class="dash-card-header">
                <h3><i data-lucide="heart"></i> Saved in Wishlist ({{ wishlist.items.count() }})</h3>
                <a href="{{ url_for('wishlist_views.wishlist_page') }}" class="btn-link">View Wishlist</a>
            </div>
            {% if wishlist.items.count() > 0 %}
                <ul class="dash-list">
                    {% for item in wishlist.items.limit(3) %}
                        <li class="dash-list-item">
                            <span>{{ item.product.title[:35] }}...</span>
                            <strong>{{ item.current_price|currency }}</strong>
                        </li>
                    {% endfor %}
                </ul>
            {% else %}
                <p class="text-muted">Your wishlist is currently empty.</p>
            {% endif %}
        </div>
    </div>

    <!-- Recommended for You -->
    <section class="section">
        <h2>Recommended For You</h2>
        <div class="products-grid">
            {% for item in recommendations %}
                {% with product = item.product %}
                    {% include 'components/product_card.html' %}
                {% endwith %}
            {% endfor %}
        </div>
    </section>
</div>
''', encoding='utf-8')

# 16. customer/profile.html
(BASE / 'customer' / 'profile.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}My Profile — ShopSense AI{% endblock %}

{% block content %}
<div class="container profile-page">
    <h1>Account Profile</h1>
    <div class="card profile-card">
        <h3>Personal Details</h3>
        <p><strong>Name:</strong> {{ user.full_name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Account Type:</strong> {{ user.role.display_name }}</p>
        <p><strong>Member Since:</strong> {{ user.created_at|dateformat }}</p>
    </div>
</div>
''', encoding='utf-8')

print('Customer platform templates generated successfully!')
