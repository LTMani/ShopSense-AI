from typing import Optional, List
from app.models.inventory import ProductInventory, InventoryTransaction, InventoryAlert
from app.repositories.base import BaseRepository
from app.extensions import db


class InventoryRepository(BaseRepository[ProductInventory]):
    def __init__(self):
        super().__init__(ProductInventory)

    def get_by_product_id(self, product_id: int) -> Optional[ProductInventory]:
        return self.find_one_by(product_id=product_id)

    def get_low_stock_items(self, seller_id: Optional[int] = None) -> List[ProductInventory]:
        query = ProductInventory.query.filter(
            ProductInventory.available_quantity <= ProductInventory.reorder_point
        )
        if seller_id:
            query = query.filter_by(seller_id=seller_id)
        return query.all()

    def get_out_of_stock_items(self, seller_id: Optional[int] = None) -> List[ProductInventory]:
        query = ProductInventory.query.filter(ProductInventory.available_quantity <= 0)
        if seller_id:
            query = query.filter_by(seller_id=seller_id)
        return query.all()

    def get_seller_inventory(self, seller_id: int) -> List[ProductInventory]:
        return ProductInventory.query.filter_by(seller_id=seller_id).all()


class InventoryTransactionRepository(BaseRepository[InventoryTransaction]):
    def __init__(self):
        super().__init__(InventoryTransaction)

    def get_by_inventory_id(self, inventory_id: int, limit: int = 50) -> List[InventoryTransaction]:
        return InventoryTransaction.query.filter_by(inventory_id=inventory_id).order_by(InventoryTransaction.created_at.desc()).limit(limit).all()


class InventoryAlertRepository(BaseRepository[InventoryAlert]):
    def __init__(self):
        super().__init__(InventoryAlert)

    def get_unresolved_by_seller(self, seller_id: int) -> List[InventoryAlert]:
        return InventoryAlert.query.filter_by(seller_id=seller_id, is_resolved=False).order_by(InventoryAlert.created_at.desc()).all()
