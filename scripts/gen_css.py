# ShopSense AI CSS Architecture Generator
from pathlib import Path

BASE_CSS = Path(__file__).resolve().parent.parent / 'app' / 'static' / 'css'
(BASE_CSS / 'base').mkdir(parents=True, exist_ok=True)
(BASE_CSS / 'components').mkdir(parents=True, exist_ok=True)
(BASE_CSS / 'pages').mkdir(parents=True, exist_ok=True)
(BASE_CSS / 'seller').mkdir(parents=True, exist_ok=True)

# 1. base/variables.css
(BASE_CSS / 'base' / 'variables.css').write_text('''/* ShopSense AI Modern Design System Variables */
:root {
    /* Brand & Accent Palettes */
    --primary: #4f46e5;
    --primary-hover: #4338ca;
    --primary-light: #eef2ff;
    --primary-glow: rgba(79, 70, 229, 0.25);
    
    --secondary: #0ea5e9;
    --secondary-hover: #0284c7;
    --secondary-light: #f0f9ff;
    
    --accent: #8b5cf6;
    --accent-hover: #7c3aed;
    --accent-light: #f5f3ff;

    --success: #10b981;
    --success-light: #ecfdf5;
    --warning: #f59e0b;
    --warning-light: #fffbeb;
    --danger: #ef4444;
    --danger-light: #fef2f2;

    /* Neutrals & Slate Scale */
    --bg-main: #f8fafc;
    --bg-surface: #ffffff;
    --bg-subtle: #f1f5f9;
    --bg-muted: #e2e8f0;
    
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;
    --text-inverse: #ffffff;

    --border-color: #e2e8f0;
    --border-focus: #818cf8;

    /* Elevation Shadows */
    --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);

    /* Transitions & Radii */
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --radius-full: 9999px;
    
    --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
''', encoding='utf-8')

# 2. base/reset.css
(BASE_CSS / 'base' / 'reset.css').write_text('''*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    font-size: 16px;
    scroll-behavior: smooth;
    -webkit-font-smoothing: antialiased;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg-main);
    color: var(--text-primary);
    line-height: 1.5;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

a {
    color: var(--primary);
    text-decoration: none;
    transition: var(--transition);
}

a:hover {
    color: var(--primary-hover);
}

ul, ol {
    list-style: none;
}

img, svg {
    display: block;
    max-width: 100%;
}

button, input, select, textarea {
    font: inherit;
    color: inherit;
}
''', encoding='utf-8')

# 3. base/typography.css
(BASE_CSS / 'base' / 'typography.css').write_text('''h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary);
    font-weight: 700;
    line-height: 1.25;
    letter-spacing: -0.02em;
}

h1 { font-size: 2.25rem; }
h2 { font-size: 1.75rem; margin-bottom: 0.5rem; }
h3 { font-size: 1.25rem; }
h4 { font-size: 1.05rem; }

p {
    color: var(--text-secondary);
    margin-bottom: 0.75rem;
}

.text-muted { color: var(--text-muted); }
.text-success { color: var(--success); }
.text-danger { color: var(--danger); }
.text-warning { color: var(--warning); }

.gradient-text {
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 50%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
''', encoding='utf-8')

# 4. components/buttons.css
(BASE_CSS / 'components' / 'buttons.css').write_text('''.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    font-size: 0.9375rem;
    font-weight: 600;
    border-radius: var(--radius-md);
    border: 1px solid transparent;
    cursor: pointer;
    transition: var(--transition);
    text-decoration: none;
}

.btn-primary {
    background-color: var(--primary);
    color: var(--text-inverse);
    box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
    background-color: var(--primary-hover);
    color: var(--text-inverse);
    box-shadow: 0 4px 12px var(--primary-glow);
    transform: translateY(-1px);
}

.btn-outline {
    background-color: transparent;
    border-color: var(--border-color);
    color: var(--text-primary);
}

.btn-outline:hover {
    background-color: var(--bg-subtle);
    border-color: var(--text-muted);
}

.btn-ghost {
    background-color: transparent;
    color: var(--text-secondary);
}

.btn-ghost:hover {
    background-color: var(--bg-subtle);
    color: var(--text-primary);
}

.btn-copilot-pill {
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
    color: #fff;
    padding: 0.5rem 1.1rem;
    border-radius: var(--radius-full);
    box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.btn-copilot-pill:hover {
    color: #fff;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.45);
    transform: translateY(-1px);
}

.btn-sm { padding: 0.4rem 0.8rem; font-size: 0.8125rem; }
.btn-lg { padding: 0.85rem 1.75rem; font-size: 1.05rem; }
.btn-xs { padding: 0.25rem 0.5rem; font-size: 0.75rem; }
.btn-block { width: 100%; }
''', encoding='utf-8')

# 5. components/cards.css
(BASE_CSS / 'components' / 'cards.css').write_text('''.card, .product-card, .seller-card, .auth-card {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    padding: 1.5rem;
    transition: var(--transition);
}

.product-card {
    display: flex;
    flex-direction: column;
    padding: 1rem;
    position: relative;
}

.product-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-3px);
    border-color: #cbd5e1;
}

.product-img-container {
    height: 190px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8fafc;
    border-radius: var(--radius-md);
    margin-bottom: 0.85rem;
    overflow: hidden;
}

.product-image {
    max-height: 160px;
    object-fit: contain;
    transition: var(--transition-slow);
}

.product-card:hover .product-image {
    transform: scale(1.05);
}

.product-card-body {
    display: flex;
    flex-direction: column;
    flex: 1;
}

.product-title a {
    color: var(--text-primary);
    font-size: 0.975rem;
    font-weight: 600;
    line-height: 1.35;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.product-short-desc {
    font-size: 0.8125rem;
    color: var(--text-muted);
    margin: 0.35rem 0 0.75rem;
}

.product-price-row {
    margin-top: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.current-price {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
}

.original-price {
    font-size: 0.8125rem;
    text-decoration: line-through;
    color: var(--text-muted);
    margin-left: 0.35rem;
}
''', encoding='utf-8')

# 6. components/badges.css
(BASE_CSS / 'components' / 'badges.css').write_text('''.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: var(--radius-full);
}

.badge-accent { background-color: var(--accent-light); color: var(--accent); }
.badge-sale { background-color: var(--danger-light); color: var(--danger); font-weight: 700; }
.badge-featured { background-color: var(--primary-light); color: var(--primary); }
.badge-success { background-color: var(--success-light); color: var(--success); }
.badge-warning { background-color: var(--warning-light); color: var(--warning); }
.badge-danger { background-color: var(--danger-light); color: var(--danger); }
.badge-outline { background-color: transparent; border: 1px solid var(--border-color); color: var(--text-secondary); }

.badge-count {
    background-color: var(--primary);
    color: #fff;
    font-size: 0.6875rem;
    padding: 0.15rem 0.4rem;
    border-radius: var(--radius-full);
    margin-left: 0.2rem;
}
''', encoding='utf-8')

# 7. components/forms.css
(BASE_CSS / 'components' / 'forms.css').write_text('''.form-group {
    margin-bottom: 1.1rem;
}

.form-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.35rem;
}

.form-control {
    width: 100%;
    padding: 0.65rem 0.9rem;
    font-size: 0.9375rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background-color: var(--bg-surface);
    transition: var(--transition);
}

.form-control:focus {
    outline: none;
    border-color: var(--border-focus);
    box-shadow: 0 0 0 3px var(--primary-glow);
}

.form-row-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.form-row-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
}
''', encoding='utf-8')

# 8. components/navbar.css
(BASE_CSS / 'components' / 'navbar.css').write_text('''.top-bar {
    background-color: #0f172a;
    color: #94a3b8;
    font-size: 0.8125rem;
    padding: 0.35rem 0;
}

.top-bar-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.top-bar-right {
    display: flex;
    gap: 1.25rem;
}

.top-bar-link {
    color: #cbd5e1;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
}

.top-bar-link:hover { color: #fff; }

.main-navbar {
    background-color: var(--bg-surface);
    border-bottom: 1px solid var(--border-color);
    padding: 0.75rem 0;
    z-index: 100;
}

.sticky { position: sticky; top: 0; }

.navbar-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
}

.navbar-brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text-primary);
}

.brand-logo {
    width: 36px;
    height: 36px;
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
}

.brand-ai { color: var(--primary); margin-left: 0.15rem; }

.nav-search-form {
    flex: 1;
    max-width: 540px;
}

.search-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.search-icon {
    position: absolute;
    left: 0.85rem;
    color: var(--text-muted);
    width: 18px;
    height: 18px;
}

.nav-search-input {
    width: 100%;
    padding: 0.6rem 3rem 0.6rem 2.4rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-full);
    font-size: 0.875rem;
    background-color: var(--bg-subtle);
    transition: var(--transition);
}

.nav-search-input:focus {
    background-color: #fff;
    outline: none;
    border-color: var(--border-focus);
    box-shadow: 0 0 0 3px var(--primary-glow);
}

.btn-search {
    position: absolute;
    right: 3px;
    border-radius: var(--radius-full);
    padding: 0.35rem 0.75rem;
}

.nav-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.nav-icon-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: var(--text-secondary);
    font-size: 0.75rem;
    font-weight: 500;
    position: relative;
}

.nav-icon-btn:hover { color: var(--primary); }
''', encoding='utf-8')

# 9. components/footer.css
(BASE_CSS / 'components' / 'footer.css').write_text('''.main-footer {
    background-color: #0f172a;
    color: #94a3b8;
    margin-top: auto;
    padding: 3.5rem 0 1.5rem;
    border-top: 1px solid #1e293b;
}

.footer-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 2.5rem;
    margin-bottom: 2.5rem;
}

.brand-logo-footer {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.25rem;
    font-weight: 800;
    color: #fff;
    margin-bottom: 0.85rem;
}

.footer-tagline {
    font-size: 0.875rem;
    color: #94a3b8;
    line-height: 1.6;
    margin-bottom: 1rem;
}

.footer-heading {
    color: #fff;
    font-size: 0.95rem;
    margin-bottom: 1rem;
}

.footer-links li {
    margin-bottom: 0.5rem;
}

.footer-links a {
    color: #94a3b8;
    font-size: 0.875rem;
}

.footer-links a:hover { color: #fff; }

.footer-bottom {
    border-top: 1px solid #1e293b;
    padding-top: 1.5rem;
    text-align: center;
    font-size: 0.8125rem;
}
''', encoding='utf-8')

# 10. components/tables.css
(BASE_CSS / 'components' / 'tables.css').write_text('''.table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    text-align: left;
}

.table th {
    background-color: var(--bg-subtle);
    color: var(--text-secondary);
    font-weight: 600;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border-color);
}

.table td {
    padding: 0.85rem 1rem;
    border-bottom: 1px solid var(--border-color);
    vertical-align: middle;
}

.table tbody tr:hover {
    background-color: #f8fafc;
}
''', encoding='utf-8')

# 11. components/modals.css
(BASE_CSS / 'components' / 'modals.css').write_text('''.toast-container {
    position: fixed;
    bottom: 1.5rem;
    right: 1.5rem;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}

.toast {
    background-color: #0f172a;
    color: #fff;
    padding: 0.85rem 1.25rem;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-xl);
    font-size: 0.875rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    animation: toast-in 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes toast-in {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
''', encoding='utf-8')

# 12. pages/marketplace.css
(BASE_CSS / 'pages' / 'marketplace.css').write_text('''.container {
    max-width: 1240px;
    margin: 0 auto;
    padding: 0 1.25rem;
}

.section { padding: 3.5rem 0; }

.hero-section {
    padding: 3.5rem 0 2.5rem;
    background: radial-gradient(circle at top right, rgba(124, 58, 237, 0.08) 0%, transparent 60%);
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 3rem;
    align-items: center;
}

.hero-title {
    font-size: 3.25rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0.75rem 0 1rem;
}

.hero-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}

.copilot-query-chips {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1.5rem;
}

.query-chip {
    font-size: 0.8125rem;
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    padding: 0.3rem 0.75rem;
    border-radius: var(--radius-full);
    color: var(--text-secondary);
}

.query-chip:hover {
    border-color: var(--primary);
    color: var(--primary);
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1.5rem;
}

.catalog-layout {
    display: grid;
    grid-template-columns: 240px 1fr;
    gap: 2rem;
    margin-top: 1.5rem;
}

.category-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.25rem;
}

.category-card {
    background: #fff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    text-align: center;
    transition: var(--transition);
}

.category-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.cat-icon-box {
    width: 48px;
    height: 48px;
    background-color: var(--primary-light);
    color: var(--primary);
    border-radius: var(--radius-md);
    margin: 0 auto 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Chat Copilot Layout */
.copilot-page-layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 1.5rem;
    height: calc(100vh - 160px);
    margin: 1.5rem auto;
}

.copilot-chat-workspace {
    background: #fff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.chat-stream {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.chat-bubble {
    display: flex;
    gap: 0.75rem;
    max-width: 80%;
}

.chat-bubble.bot { align-self: flex-start; }
.chat-bubble.user { align-self: flex-end; flex-direction: row-reverse; }

.bot-avatar {
    width: 34px;
    height: 34px;
    border-radius: var(--radius-full);
    background: var(--primary);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.bubble-content {
    background-color: #f1f5f9;
    padding: 0.85rem 1.15rem;
    border-radius: var(--radius-md);
    font-size: 0.9375rem;
}

.chat-bubble.user .bubble-content {
    background-color: var(--primary);
    color: #fff;
}

.chat-bubble.user .bubble-content p { color: #fff; }

.chat-input-bar {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border-color);
    background: #fff;
}

.chat-input-bar form {
    display: flex;
    gap: 0.75rem;
}
''', encoding='utf-8')

# 13. seller/seller_portal.css
(BASE_CSS / 'seller' / 'seller_portal.css').write_text('''.seller-portal-layout {
    display: flex;
    min-height: 100vh;
    background-color: #f8fafc;
}

.seller-sidebar {
    width: 260px;
    background-color: #0f172a;
    color: #94a3b8;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
}

.sidebar-header {
    padding: 1.5rem;
    border-bottom: 1px solid #1e293b;
}

.seller-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #fff;
}

.seller-brand-name {
    font-size: 1.15rem;
    font-weight: 800;
}

.seller-brand-badge {
    font-size: 0.65rem;
    background-color: var(--accent);
    color: #fff;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-weight: 700;
    margin-left: 0.35rem;
}

.sidebar-nav {
    flex: 1;
    padding: 1rem 0.75rem;
    overflow-y: auto;
}

.nav-section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
    padding: 0.75rem 0.75rem 0.35rem;
    font-weight: 700;
}

.sidebar-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.75rem;
    border-radius: var(--radius-md);
    color: #94a3b8;
    font-size: 0.875rem;
    font-weight: 500;
    transition: var(--transition);
}

.sidebar-link:hover, .sidebar-link.active {
    background-color: #1e293b;
    color: #fff;
}

.sidebar-link.active {
    background-color: var(--primary);
}

.seller-workspace {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}

.seller-topbar {
    background: #fff;
    border-bottom: 1px solid var(--border-color);
    padding: 1.25rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.seller-container {
    padding: 2rem;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.kpi-card {
    background: #fff;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: var(--shadow-sm);
}

.kpi-icon-box {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.kpi-icon-box.rev { background-color: var(--primary-light); color: var(--primary); }
.kpi-icon-box.profit { background-color: var(--success-light); color: var(--success); }
.kpi-icon-box.orders { background-color: var(--secondary-light); color: var(--secondary); }
.kpi-icon-box.inv { background-color: var(--warning-light); color: var(--warning); }

.kpi-value { font-size: 1.45rem; font-weight: 800; margin: 0.15rem 0; }
.kpi-label { font-size: 0.75rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }
.kpi-subtext { font-size: 0.75rem; color: var(--text-secondary); }

.trend-bars-container {
    display: flex;
    align-items: flex-end;
    gap: 0.5rem;
    height: 180px;
    padding-top: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.trend-bar-wrapper {
    flex: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
}

.trend-bar-fill {
    width: 100%;
    background: linear-gradient(180deg, var(--primary) 0%, #818cf8 100%);
    border-radius: 4px 4px 0 0;
    min-height: 6px;
    transition: var(--transition);
}

.trend-bar-fill:hover {
    background: var(--accent);
}

.trend-bar-label {
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-top: 0.35rem;
}
''', encoding='utf-8')

print('Complete CSS3 design system generated successfully!')
