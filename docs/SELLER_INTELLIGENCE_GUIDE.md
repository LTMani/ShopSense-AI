# ShopSense AI — Seller Intelligence & Mathematical Modeling Guide

This document describes the mathematical algorithms, statistical models, and operational methodologies governing ShopSense AI's Seller Intelligence Portal.

---

## 1. Time-Series Demand Forecasting (Holt-Winters Method)

ShopSense AI utilizes an additive **Triple Exponential Smoothing (Holt-Winters)** forecasting model suited for retail demand patterns characterized by trend and weekly cycles:

### Core Equations:
1. **Level Update ($L_t$):**
   $$L_t = \alpha (Y_t - S_{t-m}) + (1 - \alpha)(L_{t-1} + b_{t-1})$$
2. **Trend Update ($b_t$):**
   $$b_t = \beta (L_t - L_{t-1}) + (1 - \beta)b_{t-1}$$
3. **Seasonal Update ($S_t$):**
   $$S_t = \gamma (Y_t - L_t) + (1 - \gamma)S_{t-m}$$
4. **$k$-step Forward Projection ($\hat{Y}_{t+k}$):**
   $$\hat{Y}_{t+k} = L_t + k \cdot b_t + S_{t - m + (k \pmod m)}$$

### Confidence Intervals:
Residual standard deviation $\sigma_e$ is computed over the historical window. The 95% prediction interval is determined by:
$$\hat{Y}_{t+k} \pm 1.96 \cdot \sigma_e \sqrt{1 + \frac{k-1}{m}}$$

---

## 2. Dynamic Safety Stock & Reorder Points (ROP)

To prevent costly stockout events while avoiding capital lockup in dead inventory, the system continuously solves for optimal **Reorder Point (ROP)**:

$$ROP = (\bar{d} \times L) + SS$$

Where:
- $\bar{d}$ = Average Daily Demand Velocity (units/day)
- $L$ = Supplier Lead Time (days, default = 7 days)
- $SS$ = Dynamic Safety Stock = $Z \times \sqrt{L \cdot \sigma_d^2 + \bar{d}^2 \cdot \sigma_L^2}$
- $Z$ = Service Level Factor ($Z = 1.645$ for 95% service level)

---

## 3. Price Elasticity of Demand (PED) & Liquidation Markdown

The dynamic pricing engine quantifies customer price sensitivity:

$$PED = \frac{\% \Delta Q}{\% \Delta P} = \frac{(Q_1 - Q_0) / Q_0}{(P_1 - P_0) / P_0}$$

### Decision Rules:
- **$|PED| > 1.2$ (Highly Elastic)**: Price cuts produce net revenue expansion. Recommend aggressive promotion.
- **$|PED| < 0.8$ (Inelastic)**: Price increases preserve volume while drastically boosting gross margin.
- **Dead-Stock Liquidation**: SKUs with zero sales in $\ge 60$ days are scheduled for step-down liquidation markdowns (10% $\rightarrow$ 20% $\rightarrow$ 35%) while enforcing cost price floors ($P_{sale} \ge P_{cost} \times 1.05$).

---

## 4. Customer RFM Cohort Clustering

Customers are segmented into behavioral cohorts using quantile-ranked Recency, Frequency, and Monetary scores:

| Cohort Name | R Score | F Score | M Score | Strategic Playbook |
| :--- | :---: | :---: | :---: | :--- |
| **Champions** | 4–5 | 4–5 | 4–5 | VIP loyalty perks, early access to new releases |
| **Loyal Customers** | 3–5 | 3–5 | 3–5 | Upsell cross-category bundles, value add-ons |
| **Potential Loyalists** | 4–5 | 1–2 | 2–4 | Membership recommendations, second-purchase incentives |
| **At Risk** | 1–2 | 3–5 | 3–5 | Win-back personalized discounts, customer success outreach |
| **Bargain Hunters** | 2–4 | 1–3 | 1–2 | Flash sales, discount clearance promotions |
| **Hibernating** | 1 | 1 | 1 | Re-engagement automated drip sequence |
