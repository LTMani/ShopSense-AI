# ShopSense AI — REST API Reference Guide

This document specifies the REST API contracts, request payloads, response schemas, and error formats across all 15 Blueprint modules.

---

## 1. Authentication & Session APIs (`/api/auth/`)

### `POST /api/auth/register`
Creates a new customer account.
```json
// Request Body
{
  "email": "customer@example.com",
  "password": "SecurePassword123!",
  "first_name": "Riya",
  "last_name": "Patel",
  "phone": "+919876543210"
}

// Response (201 Created)
{
  "success": true,
  "message": "Registration successful.",
  "user": {
    "id": 12,
    "email": "customer@example.com",
    "full_name": "Riya Patel",
    "role": "customer"
  }
}
```

### `POST /api/auth/login`
Authenticates a customer or seller and initiates a secure session.
```json
// Request Body
{
  "email": "customer@example.com",
  "password": "SecurePassword123!"
}

// Response (200 OK)
{
  "success": true,
  "message": "Login successful.",
  "redirect_url": "/customer/dashboard",
  "user": {
    "id": 12,
    "email": "customer@example.com",
    "full_name": "Riya Patel",
    "role": "customer"
  }
}
```

---

## 2. Catalog & Product Search APIs (`/api/products/`, `/api/search/`)

### `GET /api/products`
Retrieves paginated product catalog with dynamic facet filters.
- **Query Parameters**:
  - `category_id` (int): Filter by category
  - `brand` (string): Filter by brand name
  - `min_price` (float): Minimum price
  - `max_price` (float): Maximum price
  - `min_rating` (float): Minimum average rating (e.g. 4.0)
  - `page` (int, default=1)
  - `per_page` (int, default=20)
  - `sort_by` (string: `price_asc`, `price_desc`, `rating_desc`, `newest`)

---

## 3. Conversational AI Copilot APIs (`/api/copilot/`)

### `POST /api/copilot/chat`
Sends a message to the conversational shopping copilot.
```json
// Request Body
{
  "message": "I need a coding laptop under 75000 with at least 16GB RAM",
  "conversation_id": 5
}

// Response (200 OK)
{
  "success": true,
  "conversation_id": 5,
  "reply": "I found 3 great laptops matching your requirement for coding with 16GB RAM under ₹75,000.",
  "recommendations": [
    {
      "id": 14,
      "title": "Lenovo ThinkPad E14 Gen 5",
      "brand": "Lenovo",
      "price": 64990.0,
      "match_score": 96.5,
      "why_recommended": "Features 16GB RAM, 512GB SSD, exceptional keyboard ergonomics for software engineering, and is ₹10,010 under your ₹75,000 budget."
    }
  ],
  "extracted_context": {
    "category": "Laptops & Computers",
    "budget": 75000.0,
    "usage": "coding",
    "specs": {"ram_gb": 16}
  }
}
```

---

## 4. Product Comparison APIs (`/api/compare/`)

### `POST /api/compare`
Compares 2 to 4 products side-by-side.
```json
// Request Body
{
  "product_ids": [1, 2]
}

// Response (200 OK)
{
  "success": true,
  "products": [...],
  "specification_matrix": [...],
  "aspect_comparisons": {
    "performance": {"1": 95, "2": 88},
    "battery": {"1": 85, "2": 92}
  },
  "ai_verdict": {
    "best_overall_id": 2,
    "best_value_id": 1,
    "key_tradeoffs": "Product 2 provides 18-hour marathon battery life at a 15% price premium, whereas Product 1 delivers higher raw CPU compute per rupee."
  }
}
```

---

## 5. Shopping Missions Basket Solver APIs (`/api/missions/`)

### `POST /api/missions/solve`
Solves a multi-item shopping constraint mission.
```json
// Request Body
{
  "title": "College Developer Setup",
  "budget": 100000.0,
  "slots": [
    {"category": "Laptops & Computers", "weight": 0.65},
    {"category": "Computer Peripherals", "weight": 0.15},
    {"category": "Audio & Headphones", "weight": 0.20}
  ]
}

// Response (200 OK)
{
  "success": true,
  "total_spend": 98480.0,
  "budget_utilization_pct": 98.48,
  "items": [...]
}
```

---

## 6. Seller Analytics & Forecasting APIs (`/api/seller/`)

### `GET /api/seller/analytics/overview`
Returns live seller KPIs, revenue curves, and category margins.

### `GET /api/seller/forecasting/predict`
Calculates 14-day demand forecast for active SKUs with Holt-Winters smoothing.
