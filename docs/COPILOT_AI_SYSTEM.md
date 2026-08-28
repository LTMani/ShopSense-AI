# ShopSense AI — Conversational AI Copilot System

This document outlines the architecture, entity extraction pipeline, contextual candidate scoring, and transparency engine governing the AI Shopping Copilot.

---

## 1. Conversational Copilot Pipeline

```
 User Input Prompt
        │
        ▼
 ┌──────────────────────────────────────────────┐
 │ 1. Intent Classification & Slot Extraction   │
 │   - Budget parsing (₹, Lakhs, k, INR)        │
 │   - Category & Brand recognition             │
 │   - Usage pattern extraction (Coding, etc.)  │
 │   - Hardware spec constraints (RAM, SSD)     │
 └──────────────────────┬───────────────────────┘
                        │
                        ▼
 ┌──────────────────────────────────────────────┐
 │ 2. Context Slot Accumulation                 │
 │   - Merge with historical session memory     │
 │   - Slot fill confirmation & refinement      │
 └──────────────────────┬───────────────────────┘
                        │
                        ▼
 ┌──────────────────────────────────────────────┐
 │ 3. Candidate Retrieval & Multi-Factor Scoring│
 │   - Hard Constraint Filter (Budget, Stock)   │
 │   - Cosine Vector Document Similarity        │
 │   - Aspect Rating & Sentiment Alignment      │
 │   - Price-to-Value Efficiency Bonus          │
 └──────────────────────┬───────────────────────┘
                        │
                        ▼
 ┌──────────────────────────────────────────────┐
 │ 4. Explainable Response Generation           │
 │   - Generate conversational rationale        │
 │   - "Why am I seeing this product?" badge    │
 │   - Actionable rich product cards payload    │
 └──────────────────────────────────────────────┘
```

---

## 2. Multi-Factor Scoring Formula

For every candidate product $P_i$ matching the category or usage query, the total relevance score $S(P_i)$ is computed as:

$$S(P_i) = w_v \cdot V(P_i, q) + w_a \cdot A(P_i, u) + w_b \cdot B(P_i, C_{budget}) + w_r \cdot R(P_i)$$

Where:
- $V(P_i, q)$ = Cosine Vector Similarity of query tokens against product specs and descriptions ($w_v = 0.35$).
- $A(P_i, u)$ = Aspect Alignment Score matching requested usage dimensions (e.g. `performance` for coding, `battery` for travel) ($w_a = 0.25$).
- $B(P_i, C_{budget})$ = Budget Efficiency Score penalizing products exceeding budget ceiling while rewarding optimal value utilization ($w_b = 0.25$).
- $R(P_i)$ = Bayesian Average Customer Rating & Review Volume ($w_r = 0.15$).

---

## 3. Explainability Engine

ShopSense AI prioritizes consumer trust by providing deterministic, transparent reasons for each recommendation:

- **Budget Alignment**: *"Priced at ₹64,990, leaving ₹10,010 under your ₹75,000 budget."*
- **Hardware Match**: *"Meets your requirement with 16GB RAM and 512GB NVMe SSD."*
- **Aspect Validation**: *"Rated 96/100 by verified purchasers for sustained computational performance."*
- **Trade-off Highlight**: *"Offers 14-hour battery endurance in exchange for a 0.2kg heavier chassis."*
