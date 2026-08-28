# ShopSense AI — Architecture Specification

## 1. Architectural Principles

ShopSense AI adheres strictly to **Clean Architecture** and **Layered Separation of Concerns**:

1. **Explicit Data Contracts**: All data transfer between persistence, domain logic, and web representation passes through strongly-typed models, data structures, and typed dictionaries.
2. **Zero Framework Bloat**: Frontend UI is implemented purely with semantic HTML5 templates, modular CSS3 custom properties, and modern ES6+ JavaScript modules.
3. **Deterministic Fallback AI**: The AI Engine does not rely on third-party cloud APIs to function. If no external API key (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`) is present, ShopSense AI automatically engages its internal mathematical heuristic algorithms without breaking or degrading functionality.
4. **Relational Data Integrity**: Strict foreign key constraints, cascading policies, composite indexes, and transaction boundaries ensure ACID safety across SQLite and PostgreSQL.

---

## 2. Layered Structure

### 1. Presentation Layer (`app/templates/`, `app/static/`)
- **Templates**: Jinja2 semantic HTML5 components structured into layouts (`base.html`, `seller_base.html`), customer views, and seller portal views.
- **Design System**: 13 modular CSS stylesheets defining a coherent token system (`variables.css`), buttons, cards, forms, badges, modals, and responsive layout grids.
- **JavaScript Core**: Modular ES6 modules for async API communication (`api_client.js`), global event-driven reactive state (`state.js`), user notifications (`toast.js`), conversational streaming UI (`copilot.js`), and interactive seller charts (`seller.js`).

### 2. HTTP Route Layer (`app/routes/`)
- 15 Flask Blueprints registering 40+ REST API endpoints and server-rendered web pages.
- Standardized authentication guards, CSRF protection, rate limiting, and security headers.

### 3. Business Service Layer (`app/services/`)
- 17 specialized domain services encapsulating all core business logic (Checkout, Invoicing, Tax calculation, Promo validation, Wishlist tracking, Telemetry logging, Catalog management, Customer profiling).

### 4. AI & Intelligence Layer (`app/ai/`)
- **Gateway & Adapters**: `AIGateway` dynamically delegates to `LocalAIAdapter`, `OpenAIAdapter`, `GeminiAdapter`, or `AnthropicAdapter`.
- **NLP Engine**: Entity extraction, Intent classification, Tokenization, and TF-IDF Cosine Vector document ranking.
- **Mathematical Forecaster**: Holt-Winters exponential smoothing, additive trend, weekly seasonality, confidence intervals, and stockout projection.
- **Constraint Optimizer**: Combinatorial knapsack mission solver maximizing utility under budget constraints.
- **Aspect Sentiment Engine**: Lexicon-based sentiment parser extracting dimension polarities from customer reviews.

### 5. Repository Layer (`app/repositories/`)
- 14 Repository classes isolating database queries from domain logic, providing clean CRUD, pagination, filtering, and transaction boundaries.

### 6. Relational Persistence Layer (`app/models/`)
- 17 SQLAlchemy models with relationship mappings, JSON serialization methods, and calculated properties.
