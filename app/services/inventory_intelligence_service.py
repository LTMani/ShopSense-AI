from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.models.inventory import ProductInventory, InventoryAlert
from app.repositories.inventory_repository import InventoryRepository, InventoryAlertRepository
from app.repositories.analytics_repository import ProductPerformanceRepository
from app.extensions import db


class InventoryIntelligenceService:
    """Manages inventory health, safety stocks, stockout warnings, and dead-stock identification."""

    def __init__(self):
        self.inventory_repo = InventoryRepository()
        self.alert_repo = InventoryAlertRepository()
        self.performance_repo = ProductPerformanceRepository()

    def get_inventory_summary(self, seller_id: int) -> Dict[str, Any]:
        items = self.inventory_repo.get_seller_inventory(seller_id)
        alerts = self.alert_repo.get_unresolved_by_seller(seller_id)
        dead_stock = self.performance_repo.get_dead_stock(seller_id)

        low_stock_count = sum(1 for i in items if i.available_quantity <= i.reorder_point and i.available_quantity > 0)
        out_of_stock_count = sum(1 for i in items if i.available_quantity <= 0)
        total_units_on_hand = sum(i.total_on_hand for i in items)

        return {
            'total_sku_count': len(items),
            'total_units_on_hand': total_units_on_hand,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'dead_stock_count': len(dead_stock),
            'active_alerts': [a.to_dict() for a in alerts],
            'inventory_items': [i.to_dict() for i in items]
        }

    def restock_inventory(self, inventory_id: int, quantity_added: int) -> Dict[str, Any]:
        inv = self.inventory_repo.get_by_id(inventory_id)
        if not inv:
            raise ValueError("Inventory record not found.")

        inv.available_quantity += quantity_added
        inv.last_restocked_at = datetime.now(timezone.utc)
        inv.stock_status = 'in_stock'
        db.session.commit()
        return inv.to_dict()
