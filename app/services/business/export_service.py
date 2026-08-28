import csv
import io
from typing import List, Dict, Any
from app.models.product import Product
from app.models.inventory import ProductInventory


class CatalogExportService:
    """Exports merchant catalog, inventory logs, and performance metrics to CSV/JSON."""

    @staticmethod
    def export_products_csv(products: List[Product]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['ID', 'SKU', 'Title', 'Brand', 'Category', 'Base Price', 'Sale Price', 'Cost Price', 'Stock', 'Rating', 'Sales Count'])

        for p in products:
            stock = p.inventory.available_quantity if p.inventory else 0
            cat_name = p.category.name if p.category else ''
            writer.writerow([
                p.id, p.sku, p.title, p.brand, cat_name,
                p.base_price, p.sale_price, p.cost_price, stock,
                p.average_rating, p.purchases_count
            ])

        return output.getvalue()

    @staticmethod
    def export_inventory_csv(inventory_items: List[ProductInventory]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(['Inventory ID', 'Product SKU', 'Product Title', 'Available Qty', 'Reserved Qty', 'Safety Stock', 'Reorder Point', 'Days of Supply', 'Stock Status'])

        for item in inventory_items:
            writer.writerow([
                item.id, item.product.sku if item.product else '',
                item.product.title if item.product else '',
                item.available_quantity, item.reserved_quantity,
                item.safety_stock, item.reorder_point,
                item.days_of_supply, item.stock_status
            ])

        return output.getvalue()
