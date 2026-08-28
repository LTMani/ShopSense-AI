# ShopSense AI — Entity Relationship & Data Model Specification

This document details the 17 relational database models and schema relationships supporting the ShopSense AI platform.

---

## 1. Schema ER Diagram

```
 users (Users & Auth)
   ├── customer_profiles (1:1 Customer details & RFM stats)
   ├── seller_profiles (1:1 Store details, ratings, settings)
   │     ├── products (1:N Catalog items)
   │     │     ├── product_attributes (1:N Tech specs key-values)
   │     │     ├── product_images (1:N Gallery images)
   │     │     ├── product_inventories (1:1 Stock quantities & safety buffers)
   │     │     ├── product_price_histories (1:N Price evolution)
   │     │     ├── reviews (1:N Verified customer reviews)
   │     │     │     └── review_aspect_ratings (1:N ABSA scores)
   │     │     └── demand_forecasts (1:N Holt-Winters projections)
   │     └── seller_metrics_daily (1:N Historical business ledger)
   ├── carts (1:1 Active shopper cart)
   │     └── cart_items (1:N Cart item line items)
   ├── wishlists (1:1 Saved products)
   │     └── wishlist_items (1:N Price tracked items)
   ├── orders (1:N Placed orders)
   │     ├── order_items (1:N Purchased line items)
   │     └── order_status_histories (1:N Timeline audit)
   ├── shopping_missions (1:N Multi-item basket optimization)
   │     └── shopping_mission_items (1:N Allocated items)
   ├── conversations (1:N Copilot chat sessions)
   │     └── conversation_messages (1:N Messages & recommendation cards)
   ├── browsing_events (1:N Behavioral tracking events)
   └── search_histories (1:N Search logs with intent entities)
```

---

## 2. Table Specifications

### `users`
Core user authentication table with role-based access control.
- `id` (PK, Integer)
- `email` (Unique, String(255), Indexed)
- `password_hash` (String(255))
- `first_name` (String(100))
- `last_name` (String(100))
- `role_id` (FK -> `roles.id`)
- `is_active` (Boolean, Default True)
- `last_login_at` (DateTime, Nullable)

### `products`
E-Commerce product catalog model with calculated commercial properties.
- `id` (PK, Integer)
- `sku` (Unique, String(64), Indexed)
- `title` (String(255), Indexed)
- `slug` (Unique, String(255), Indexed)
- `seller_id` (FK -> `seller_profiles.id`)
- `category_id` (FK -> `categories.id`)
- `base_price` (Float)
- `sale_price` (Float)
- `cost_price` (Float)
- `average_rating` (Float, Default 0.0)
- `total_reviews_count` (Integer, Default 0)
- `aspect_sentiments` (JSON/Text)
- `is_featured` (Boolean, Default False)
- `is_active` (Boolean, Default True)

### `product_inventories`
Real-time inventory levels, safety thresholds, and restock policies.
- `id` (PK, Integer)
- `product_id` (FK -> `products.id`, Unique)
- `quantity` (Integer, Default 0)
- `reserved_quantity` (Integer, Default 0)
- `safety_stock_threshold` (Integer, Default 10)
- `reorder_point` (Integer, Default 15)
- `daily_velocity` (Float, Default 0.0)
- `last_restocked_at` (DateTime, Nullable)

### `reviews` & `review_aspect_ratings`
Customer review submissions with Aspect-Based Sentiment Analysis.
- `reviews.rating` (Integer, 1 to 5)
- `reviews.sentiment_polarity` (Float, -1.0 to +1.0)
- `reviews.extracted_praises` (JSON Array)
- `reviews.extracted_complaints` (JSON Array)
- `review_aspect_ratings.aspect_name` (e.g. `battery`, `display`, `build`, `performance`)
- `review_aspect_ratings.score` (Integer, 0 to 100)

### `demand_forecasts`
Holt-Winters time-series forecast records.
- `product_id` (FK -> `products.id`)
- `seller_id` (FK -> `seller_profiles.id`)
- `horizon_days` (Integer, Default 14)
- `predicted_demand_total` (Integer)
- `predicted_daily_rate` (Float)
- `confidence_interval_low` (Integer)
- `confidence_interval_high` (Integer)
- `stockout_predicted` (Boolean)
- `estimated_days_to_stockout` (Float, Nullable)
- `recommended_reorder_qty` (Integer)
- `daily_projections` (JSON Array)
