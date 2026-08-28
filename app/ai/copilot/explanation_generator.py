from typing import List, Dict, Any, Optional
from app.models.product import Product


class ExplanationGenerator:
    """Generates transparent, human-readable explanations answering 'Why am I seeing this product?'."""

    @classmethod
    def generate_explanation(
        cls,
        product: Product,
        match_score: float,
        reasons: List[str],
        user_budget: Optional[float] = None,
        priorities: Optional[List[str]] = None
    ) -> str:
        parts = [f"Recommended with a **{match_score}% match score**."]
        
        if reasons:
            bullets = ", ".join(reasons)
            parts.append(f"Key factors: {bullets}.")
        
        if user_budget and product.current_price <= user_budget:
            savings = user_budget - product.current_price
            if savings > 1000:
                parts.append(f"Saves you ₹{savings:,.0f} compared to your maximum budget ceiling.")

        return " ".join(parts)
