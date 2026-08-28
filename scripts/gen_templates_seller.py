# ShopSense AI Seller Platform & System Templates Generator
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'app' / 'templates'

# 1. seller/dashboard.html
(BASE / 'seller' / 'dashboard.html').write_text('''{% extends 'layouts/seller_base.html' %}

{% block page_title %}Executive Seller Overview{% endblock %}
{% block page_subtitle %}Live metrics dynamically computed from customer database transactions{% endblock %}

{% block content %}
<!-- Top KPI Cards -->
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon-box rev"><i data-lucide="indian-rupee"></i></div>
        <div class="kpi-details">
            <span class="kpi-label">Total Net Revenue</span>
            <h3 class="kpi-value">{{ kpis.total_revenue|currency }}</h3>
            <span class="kpi-subtext positive"><i data-lucide="trending-up"></i> Active commercial transactions</span>
        </div>
    </div>

    <div class="kpi-card">
        <div class="kpi-icon-box profit"><i data-lucide="wallet"></i></div>
        <div class="kpi-details">
            <span class="kpi-label">Gross Margin / Profit</span>
            <h3 class="kpi-value">{{ kpis.total_profit|currency }}</h3>
            <span class="kpi-subtext">Estimated acquisition margin</span>
        </div>
    </div>

    <div class="kpi-card">
        <div class="kpi-icon-box orders"><i data-lucide="shopping-bag"></i></div>
        <div class="kpi-details">
            <span class="kpi-label">Total Units Sold</span>
            <h3 class="kpi-value">{{ kpis.units_sold }}</h3>
            <span class="kpi-subtext">AOV: {{ kpis.average_order_value|currency }}</span>
        </div>
    </div>

    <div class="kpi-card">
        <div class="kpi-icon-box inv"><i data-lucide="boxes"></i></div>
        <div class="kpi-details">
            <span class="kpi-label">Total Units on Hand</span>
            <h3 class="kpi-value">{{ inventory.total_units_on_hand }}</h3>
            <span class="kpi-subtext {% if inventory.low_stock_count > 0 %}warning{% endif %}">
                {{ inventory.low_stock_count }} items near reorder threshold
            </span>
        </div>
    </div>
</div>

<!-- Active Inventory Alerts Banner if present -->
{% if inventory.active_alerts %}
    <div class="alert-banner-box">
        <div class="alert-banner-header">
            <i data-lucide="alert-triangle"></i>
            <h4>Active AI Inventory Risk Alerts ({{ inventory.active_alerts|length }})</h4>
        </div>
        <div class="alert-pills-list">
            {% for alert in inventory.active_alerts[:3] %}
                <div class="alert-pill-item severity-{{ alert.severity }}">
                    <strong>{{ alert.title }}:</strong> {{ alert.message }}
                    <span class="action-tag">&rarr; {{ alert.action_recommended }}</span>
                </div>
            {% endfor %}
        </div>
    </div>
{% endif %}

<!-- Revenue Trend & Recent Orders Grid -->
<div class="seller-split-grid">
    <div class="seller-card">
        <div class="card-header-row">
            <h3>30-Day Revenue Trend (Dynamic)</h3>
            <span class="badge badge-outline">Daily Aggregation</span>
        </div>
        <!-- Pure CSS/SVG Bar Chart Visualization -->
        <div class="trend-bars-container">
            {% for pt in kpis.revenue_trend %}
                <div class="trend-bar-wrapper" title="{{ pt.date }}: {{ pt.revenue|currency }}">
                    <div class="trend-bar-fill" style="height: {{ (pt.revenue / 200000.0 * 100)|int }}%;"></div>
                    <span class="trend-bar-label">{{ pt.date[-2:] }}</span>
                </div>
            {% endfor %}
        </div>
    </div>

    <div class="seller-card">
        <div class="card-header-row">
            <h3>Recent Store Orders</h3>
            <a href="{{ url_for('seller_views.analytics') }}" class="btn-link">View Analytics</a>
        </div>
        <div class="orders-table-wrapper">
            <table class="table table-compact">
                <thead>
                    <tr>
                        <th>Order #</th>
                        <th>Total</th>
                        <th>Status</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for ord in recent_orders %}
                        <tr>
                            <td><strong>{{ ord.order_number }}</strong></td>
                            <td>{{ ord.total_amount|currency }}</td>
                            <td><span class="badge badge-{{ ord.status }}">{{ ord.status|capitalize }}</span></td>
                            <td>{{ ord.created_at|dateformat }}</td>
                        </tr>
                    {% else %}
                        <tr><td colspan="4" class="text-muted">No recent orders.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
''', encoding='utf-8')

# 2. seller/products.html
(BASE / 'seller' / 'products.html').write_text('''{% extends 'layouts/seller_base.html' %}

{% block page_title %}Seller Product Catalog{% endblock %}
{% block page_subtitle %}Manage pricing, status, and view velocity metrics for your active SKUs{% endblock %}

{% block content %}
<div class="seller-card">
    <div class="card-header-row">
        <h3>Your Listed Products ({{ products|length }} SKUs)</h3>
    </div>

    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>SKU</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Cost</th>
                    <th>Stock</th>
                    <th>Rating</th>
                    <th>Velocity</th>
                </tr>
            </thead>
            <tbody>
                {% for p in products %}
                    <tr>
                        <td>
                            <div class="table-prod-info">
                                <img src="{{ p.primary_image_url }}" alt="{{ p.title }}" class="table-thumb">
                                <div>
                                    <strong><a href="{{ url_for('product_views.product_detail', slug=p.slug) }}" target="_blank">{{ p.title }}</a></strong>
                                    <span class="table-sub">{{ p.brand }}</span>
                                </div>
                            </div>
                        </td>
                        <td><code>{{ p.sku }}</code></td>
                        <td>{{ p.category.name if p.category else '—' }}</td>
                        <td><strong>{{ p.current_price|currency }}</strong></td>
                        <td>{{ p.cost_price|currency }}</td>
                        <td>
                            {% if p.inventory %}
                                <span class="badge {% if p.inventory.available_quantity <= 5 %}badge-danger{% elif p.inventory.available_quantity <= 20 %}badge-warning{% else %}badge-success{% endif %}">
                                    {{ p.inventory.available_quantity }} in stock
                                </span>
                            {% else %}
                                0
                            {% endif %}
                        </td>
                        <td>{{ p.average_rating }}★ ({{ p.total_reviews_count }})</td>
                        <td>{{ p.purchases_count }} sold</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
''', encoding='utf-8')

# 3. seller/inventory.html
(BASE / 'seller' / 'inventory.html').write_text('''{% extends 'layouts/seller_base.html' %}

{% block page_title %}Inventory Intelligence & Reordering{% endblock %}
{% block page_subtitle %}Safety stock thresholds, days of supply, and stockout risk mitigation{% endblock %}

{% block content %}
<div class="inventory-kpi-row">
    <div class="kpi-pill">Total SKUs: <strong>{{ inventory.total_sku_count }}</strong></div>
    <div class="kpi-pill">Units on Hand: <strong>{{ inventory.total_units_on_hand }}</strong></div>
    <div class="kpi-pill warning">Low Stock: <strong>{{ inventory.low_stock_count }}</strong></div>
    <div class="kpi-pill danger">Out of Stock: <strong>{{ inventory.out_of_stock_count }}</strong></div>
    <div class="kpi-pill dead">Dead Stock SKUs: <strong>{{ inventory.dead_stock_count }}</strong></div>
</div>

<div class="seller-card">
    <h3>Inventory Level Ledger</h3>
    <table class="table">
        <thead>
            <tr>
                <th>Product</th>
                <th>Available</th>
                <th>Safety Stock</th>
                <th>Reorder Point</th>
                <th>Days of Supply</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for item in inventory.inventory_items %}
                <tr>
                    <td><strong>{{ item.product_title }}</strong> <br><small class="text-muted">{{ item.product_sku }}</small></td>
                    <td><strong>{{ item.available_quantity }}</strong> units</td>
                    <td>{{ item.safety_stock }}</td>
                    <td>{{ item.reorder_point }}</td>
                    <td>{{ item.days_of_supply }} days</td>
                    <td>
                        <span class="badge badge-{{ item.stock_status }}">{{ item.stock_status|capitalize }}</span>
                    </td>
                    <td>
                        <button class="btn btn-outline btn-xs" onclick="ShopSenseSeller.restock({{ item.id }}, '{{ item.product_title }}')">Restock +50</button>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
''', encoding='utf-8')

# 4. seller/analytics.html
(BASE / 'seller' / 'analytics.html').write_text('''{% extends 'layouts/seller_base.html' %}

{% block page_title %}Sales & Performance Analytics{% endblock %}
{% block page_subtitle %}Detailed conversion scoring, margins, and product performance grades{% endblock %}

{% block content %}
<div class="seller-card">
    <h3>Product Performance Score Matrix</h3>
    <p class="text-muted">Calculated using traffic velocity, conversion rate, return rate, and review sentiment.</p>
    
    <table class="table">
        <thead>
            <tr>
                <th>Product</th>
                <th>Grade</th>
                <th>Overall Index</th>
                <th>Velocity</th>
                <th>Conversion</th>
                <th>Sentiment</th>
                <th>Dead Stock?</th>
                <th>AI Strategic Advice</th>
            </tr>
        </thead>
        <tbody>
            {% for p in performance_rankings %}
                <tr>
                    <td><strong>{{ p.product_title }}</strong></td>
                    <td><span class="badge badge-grade-{{ p.performance_grade }}">{{ p.performance_grade }}</span></td>
                    <td><strong>{{ p.overall_score }} / 100</strong></td>
                    <td>{{ p.sales_velocity_score }}</td>
                    <td>{{ p.conversion_score }}</td>
                    <td>{{ p.rating_sentiment_score }}</td>
                    <td>{% if p.is_dead_stock %}<span class="badge badge-danger">YES ({{ p.days_since_last_sale }}d)</span>{% else %}<span class="badge badge-success">Active</span>{% endif %}</td>
                    <td><em>{{ p.action_recommendation }}</em></td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
''', encoding='utf-8')

# 5. seller/forecasting.html
(BASE / 'seller' / 'forecasting.html').write_text('''{% extends 'layouts/seller_base.html' %}

{% block page_title %}AI Demand Forecasting Engine{% endblock %}
{% block page_subtitle %}Mathematical time-series projections with stockout risk indicators{% endblock %}

{% block content %}
<div class="seller-card">
    <h3>Select Product for 14-Day Demand Forecast Projection</h3>
    <div class="forecast-select-box">
        <select id="forecast-prod-select" class="form-control" onchange="ShopSenseSeller.fetchForecast(this.value)">
            {% for p in products %}
                <option value="{{ p.id }}">{{ p.title }} (Current Stock: {{ p.inventory.available_quantity if p.inventory else 0 }})</option>
            {% endfor %}
        </select>
    </div>

    <!-- Forecast Output Display Area -->
    <div id="forecast-output-area" class="forecast-results-box">
        <div class="empty-state">
            <p>Select a product above or click below to generate projection.</p>
            <button class="btn btn-primary" onclick="ShopSenseSeller.fetchForecast(document.getElementById('forecast-prod-select').value)">Generate Forecast</button>
        </div>
    </div>
</div>
{% endblock %}
''', encoding='utf-8')

# 6. seller/pricing.html
(BASE / 'seller' / 'pricing.html').write_text('''{% extends 'layouts/seller_base.html' %}

{% block page_title %}Pricing Intelligence & Elasticity{% endblock %}
{% block page_subtitle %}Data-driven pricing suggestions for velocity optimization and clearance{% endblock %}

{% block content %}
<div class="seller-card">
    <h3>AI Pricing Recommendations</h3>
    <table class="table">
        <thead>
            <tr>
                <th>Product</th>
                <th>Current Price</th>
                <th>Recommended</th>
                <th>Delta</th>
                <th>Strategy Action</th>
                <th>Rationale</th>
            </tr>
        </thead>
        <tbody>
            {% for rec in pricing_recommendations %}
                <tr>
                    <td><strong>{{ rec.product_title }}</strong></td>
                    <td>{{ rec.current_price|currency }}</td>
                    <td><strong>{{ rec.recommended_price|currency }}</strong></td>
                    <td>
                        {% if rec.price_change_amount < 0 %}
                            <span class="text-danger">{{ rec.price_change_amount|currency }}</span>
                        {% elif rec.price_change_amount > 0 %}
                            <span class="text-success">+{{ rec.price_change_amount|currency }}</span>
                        {% else %}
                            <span class="text-muted">0.00</span>
                        {% endif %}
                    </td>
                    <td><span class="badge badge-outline">{{ rec.action|capitalize }}</span></td>
                    <td>{{ rec.reason }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
''', encoding='utf-8')

# 7. seller/customers.html
(BASE / 'seller' / 'customers.html').write_text('''{% extends 'layouts/seller_base.html' %}

{% block page_title %}Customer Cohort & RFM Segmentation{% endblock %}
{% block page_subtitle %}Customer clusters based on Recency, Frequency, and Monetary parameters{% endblock %}

{% block content %}
<div class="segments-grid">
    {% for seg in segments %}
        <div class="segment-card">
            <div class="segment-card-header">
                <h3>{{ seg.name }}</h3>
                <span class="badge badge-accent">{{ seg.member_count }} Shoppers</span>
            </div>
            <p class="seg-desc">{{ seg.description }}</p>
            <div class="seg-metric">Average Lifetime Spend: <strong>{{ seg.average_spend|currency }}</strong></div>
            <div class="seg-strategy">
                <strong>Recommended Marketing Strategy:</strong>
                <p>{{ seg.recommended_strategy }}</p>
            </div>
        </div>
    {% endfor %}
</div>
{% endblock %}
''', encoding='utf-8')

# 8. seller/seller_copilot.html
(BASE / 'seller' / 'seller_copilot.html').write_text('''{% extends 'layouts/seller_base.html' %}

{% block page_title %}Seller AI Diagnostic Copilot{% endblock %}
{% block page_subtitle %}Ask root-cause business questions grounded in actual store metrics{% endblock %}

{% block content %}
<div class="seller-copilot-workspace">
    <div class="seller-copilot-suggestions">
        <span>Suggested questions:</span>
        <button class="btn btn-outline btn-xs" onclick="ShopSenseSellerCopilot.ask('Why did my sales decrease this month?')">Why did my sales decrease this month?</button>
        <button class="btn btn-outline btn-xs" onclick="ShopSenseSellerCopilot.ask('Which items are at risk of stockout within 10 days?')">Which items are at risk of stockout?</button>
        <button class="btn btn-outline btn-xs" onclick="ShopSenseSellerCopilot.ask('How can I optimize pricing for slow moving inventory?')">How to optimize slow inventory?</button>
    </div>

    <div class="seller-chat-stream" id="seller-chat-stream">
        <div class="chat-bubble bot">
            <div class="bot-avatar"><i data-lucide="bot"></i></div>
            <div class="bubble-content">
                <p>Welcome to <strong>Seller AI Copilot</strong>. I analyze your real inventory levels, conversion funnels, review sentiments, and transaction history to diagnose business performance.</p>
            </div>
        </div>
    </div>

    <div class="chat-input-bar">
        <form onsubmit="ShopSenseSellerCopilot.send(event)">
            <input type="text" id="seller-copilot-input" class="form-control" placeholder="Ask a diagnostic question (e.g., 'Why are headphones revenue dropping?')..." required>
            <button type="submit" class="btn btn-primary"><i data-lucide="send"></i></button>
        </form>
    </div>
</div>
{% endblock %}
''', encoding='utf-8')

# 9. seller/seller_settings.html
(BASE / 'seller' / 'seller_settings.html').write_text('''{% extends 'layouts/seller_base.html' %}

{% block page_title %}Store Configuration & Settings{% endblock %}
{% block page_subtitle %}Manage merchant credentials, notifications, and commission rates{% endblock %}

{% block content %}
<div class="seller-card">
    <h3>Merchant Store Profile</h3>
    <p><strong>Business Name:</strong> {{ current_user.seller_profile.business_name if current_user.seller_profile else 'Apex Tech' }}</p>
    <p><strong>Store Slug:</strong> <code>{{ current_user.seller_profile.store_slug if current_user.seller_profile else 'apex-tech' }}</code></p>
    <p><strong>Platform Commission Rate:</strong> 8.0%</p>
    <p><strong>Merchant Status:</strong> <span class="badge badge-success">Verified Merchant</span></p>
</div>
{% endblock %}
''', encoding='utf-8')

# 10. settings/app_settings.html
(BASE / 'settings' / 'app_settings.html').write_text('''{% extends 'layouts/base.html' %}

{% block title %}Application Settings — ShopSense AI{% endblock %}

{% block content %}
<div class="container settings-page">
    <h1>Platform Configuration & AI Settings</h1>
    <div class="card settings-card">
        <h3>AI Provider & Engine Status</h3>
        <p><strong>Current Active Provider:</strong> <code>{{ config.AI_PROVIDER }}</code></p>
        <p><strong>Model:</strong> <code>{{ config.AI_MODEL }}</code></p>
        <p><strong>Local Heuristic Engine:</strong> <span class="badge badge-success">Operational</span></p>
        <p><strong>Relational Database:</strong> <span class="badge badge-success">SQLite / PostgreSQL-Ready</span></p>
        <p><strong>Payment Processing:</strong> <span class="badge badge-outline">Simulated (Zero Real Financial APIs)</span></p>
    </div>
</div>
{% endblock %}
''', encoding='utf-8')

# 11. Error Pages
for code, title, msg in [
    (400, 'Bad Request', 'The request could not be processed.'),
    (401, 'Unauthorized', 'Please log in to access this resource.'),
    (403, 'Forbidden', 'You do not have permission to view this page.'),
    (404, 'Page Not Found', 'The requested page does not exist.'),
    (429, 'Rate Limit Exceeded', 'Too many requests. Please slow down.'),
    (500, 'Internal Server Error', 'An unexpected server error occurred.')
]:
    content = "{% extends 'layouts/base.html' %}\n\n"
    content += f"{{% block title %}}{code} — {title}{{% endblock %}}\n\n"
    content += "{% block content %}\n"
    content += '<div class="container error-page">\n'
    content += '    <div class="error-card">\n'
    content += f'        <h1 class="error-code">{code}</h1>\n'
    content += f'        <h2>{title}</h2>\n'
    content += f'        <p>{msg}</p>\n'
    content += '        <a href="{{ url_for(\'system_views.landing_page\') }}" class="btn btn-primary">Return to Homepage</a>\n'
    content += '    </div>\n'
    content += '</div>\n'
    content += '{% endblock %}\n'
    (BASE / 'errors' / f'{code}.html').write_text(content, encoding='utf-8')

print('Seller and System templates generated successfully!')
