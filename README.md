# ShopSense AI — Intelligent Shopping & Seller Intelligence Platform

> **Shop Smarter. Sell Smarter.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Framework: Flask 3.x](https://img.shields.io/badge/Framework-Flask%203.x-black.svg)](https://flask.palletsprojects.com/)
[![Database: SQLite & PostgreSQL Ready](https://img.shields.io/badge/Database-SQLAlchemy%202.0-blue.svg)](https://www.sqlalchemy.org/)
[![AI: Hybrid Offline & Cloud LLM](https://img.shields.io/badge/AI-Zero--Dependency%20Fallback-purple.svg)]()

---

## 🌟 Executive Overview

**ShopSense AI** is a complete, enterprise-grade, AI-native E-Commerce Intelligence Platform that unifies **Conversational Consumer Intelligence** with **Deep Seller Commercial Analytics**.

Built entirely with clean, standard-compliant technologies — **Python 3.x / Flask 3.x backend**, **SQLAlchemy 2.0 relational persistence**, and a **Vanilla HTML5/CSS3/ES6+ JavaScript frontend** (strictly zero React/Vue/Node build bloat) — ShopSense AI provides a blazingly fast, reliable, and explainable shopping experience.

---

## 🚀 Key Subsystems & Architectural Pillars

### 1. Customer Intelligence
* **🤖 Conversational AI Shopping Copilot**: Multi-turn natural language dialogue engine with slot filling, budget parsing (supports INR ₹, Lakhs, k), usage priority extraction, adaptive candidate ranking, and transparent *"Why am I seeing this product?"* explainability.
* **🔍 Hybrid Semantic Search**: Combines structured database filters with pure-Python TF-IDF and Cosine Vector Similarity re-ranking.
* **📊 Aspect-Level Review Intelligence**: Aspect-Based Sentiment Analysis (ABSA) across hardware dimensions (*Battery, Sound, Build, Display, Performance, Comfort, Camera, Value*) with praise/complaint summaries and verified purchase weighting.
* **⚖️ Dynamic Product Comparison Matrix**: Side-by-side technical specification alignment, price deltas, aspect sentiment radar comparisons, and automatic AI comparison verdicts.
* **🎯 Shopping Missions Optimizer**: Multi-product basket constraint solver (e.g., *"Build college study setup under ₹30,000"*) allocating budget slots across complementary items.
* **🛒 Smart Cart & Wishlist**: Real-time savings opportunities, shipping threshold indicators, accessory recommendations, and historical price-drop alerts.

### 2. Seller Intelligence
* **📈 Executive Business Dashboard**: Live metrics dynamically computed from real database transactions (Net Revenue, Gross Margin, Average Order Value, Velocity).
* **🔮 Mathematical Demand Forecasting Engine**: Multi-step time-series forecasting (Holt-Winters Triple Exponential Smoothing, Additive Seasonality, 95% Confidence Bounds, and Stockout Risk countdowns).
* **📦 Inventory Intelligence & Reordering**: Safety stock calculations, days-of-supply ledger, dead-stock detection (>60 days without sales), and interactive restock tooling.
* **🏷️ Dynamic Pricing & Elasticity Engine**: Price Elasticity of Demand (PED) tracking, competitive price matching, margin floor enforcement, and automated liquidation markdown recommendations.
* **👥 Customer RFM Cohort Segmentation**: Recency, Frequency, Monetary (RFM) clustering (*Champions, Loyal, High-Potential, At-Risk, Bargain Hunters, Hibernating*) with actionable marketing playbooks.
* **🩺 Seller AI Diagnostic Copilot**: Multi-variable root-cause analysis assistant that inspects actual stock levels, conversion funnels, and review telemetry to answer complex strategic queries.

---

## 🏗️ Clean Layered Architecture

```
                               ┌────────────────────────┐
                               │   Browser Frontend     │
                               │  HTML5 + CSS3 + ES6+   │
                               └───────────┬────────────┘
                                           │
                        REST API & Web Views (Flask Blueprints)
                                           │
                               ┌───────────▼────────────┐
                               │  Domain Services (17)  │
                               └─────┬────────────┬─────┘
                                     │            │
             ┌───────────────────────▼──┐      ┌──▼────────────────────────┐
             │ AI & Intelligence Engine │      │ Repositories / DAOs (14)  │
             │   - Gateway & Adapters   │      └───────────┬───────────────┘
             │   - NLP & Tokenizers     │                  │
             │   - Time-Series Forecaster                  │
             │   - Constraint Optimizer │                  │
             │   - ABSA Sentiment Engine│                  │
             └──────────────────────────┘      ┌───────────▼───────────────┐
                                               │ Relational Models (17)    │
                                               │ SQLite / PostgreSQL       │
                                               └───────────────────────────┘
```

---

## ⚡ Quick Start & Setup

### Prerequisites
* Python 3.10, 3.11, 3.12, or 3.13
* Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LTMani/ShopSense-AI.git
   cd ShopSense-AI
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize and seed the database:**
   ```bash
   flask seed-db
   ```

5. **Start the local development server:**
   ```bash
   python run.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

---

## 🧪 Automated Testing

Run the comprehensive pytest test suite:
```bash
pytest -v tests/
```

Run test coverage report:
```bash
pytest --cov=app tests/
```

---

## 🔐 Demo Credentials

The seeded database contains pre-configured verified accounts:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Customer** | `customer@shopsense.ai` | `CustomerPass2026!` |
| **Seller** | `seller.apex@shopsense.ai` | `SellerPass2026!` |

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
