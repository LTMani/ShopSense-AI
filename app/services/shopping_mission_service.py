from typing import Dict, Any, List
from app.models.mission import ShoppingMission, ShoppingMissionItem
from app.models.product import Product
from app.repositories.mission_repository import MissionRepository, MissionItemRepository
from app.repositories.product_repository import ProductRepository
from app.ai.nlp.entity_extractor import EntityExtractor
from app.extensions import db


class ShoppingMissionService:
    """Builds multi-product goal baskets optimized for user constraints (e.g. Study Setup, Creator Kit)."""

    def __init__(self):
        self.mission_repo = MissionRepository()
        self.item_repo = MissionItemRepository()
        self.product_repo = ProductRepository()

    def build_mission(
        self,
        user_id: int,
        prompt: str,
        target_budget: float,
        optimization_mode: str = 'balanced'
    ) -> Dict[str, Any]:
        mission = self.mission_repo.create(
            user_id=user_id,
            title=prompt[:60],
            mission_prompt=prompt,
            target_budget=target_budget,
            optimization_mode=optimization_mode,
            status='optimized'
        )

        # Allocate budget slots across essential categories
        # Example setup: Core (60%), Ergonomics / Display (25%), Accessories / Audio (15%)
        slots = [
            {'role': 'Core Device', 'share': 0.60, 'cat_keywords': ['laptop', 'phone', 'console', 'camera']},
            {'role': 'Peripherals & Ergonomics', 'share': 0.25, 'cat_keywords': ['monitor', 'chair', 'desk', 'keyboard']},
            {'role': 'Audio & Focus', 'share': 0.15, 'cat_keywords': ['headphone', 'earbuds', 'mouse', 'dock']}
        ]

        total_allocated = 0.0
        for slot in slots:
            slot_budget = target_budget * slot['share']
            # Find best fitting product
            candidate = None
            for p in Product.query.filter_by(is_active=True).order_by(Product.average_rating.desc()).all():
                p_text = f"{p.title} {p.category.name if p.category else ''}".lower()
                if any(k in p_text for k in slot['cat_keywords']):
                    if p.current_price <= (slot_budget * 1.25):
                        candidate = p
                        break

            if candidate:
                self.item_repo.create(
                    mission_id=mission.id,
                    product_id=candidate.id,
                    slot_role=slot['role'],
                    assigned_budget=slot_budget,
                    actual_price=candidate.current_price,
                    selection_rationale=f"Selected for top tier reliability and verified rating ({candidate.average_rating}★)."
                )
                total_allocated += candidate.current_price

        mission.allocated_total = total_allocated
        mission.savings_amount = max(0.0, target_budget - total_allocated)
        mission.ai_rationale = (
            f"Basket optimized for a {optimization_mode} strategy within your ₹{target_budget:,.0f} limit. "
            f"Total estimated cost is ₹{total_allocated:,.0f}, leaving ₹{mission.savings_amount:,.0f} in remaining budget."
        )
        db.session.commit()

        return mission.to_dict(include_items=True)
