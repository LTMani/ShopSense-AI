from typing import Dict, Any, Optional, List
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository


class CatalogService:
    """Manages catalog browsing, category hierarchy, product specifications, and stock status."""

    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_repo = CategoryRepository()

    def get_categories(self, include_children: bool = True) -> List[Dict[str, Any]]:
        categories = self.category_repo.get_root_categories(active_only=True)
        return [c.to_dict(include_children=include_children) for c in categories]

    def get_product_by_id(self, product_id: int, detailed: bool = True) -> Optional[Dict[str, Any]]:
        product = self.product_repo.get_by_id(product_id)
        if not product or not product.is_active:
            return None
        self.product_repo.increment_view_count(product_id)
        return product.to_dict(detailed=detailed)

    def get_product_by_slug(self, slug: str, detailed: bool = True) -> Optional[Dict[str, Any]]:
        product = self.product_repo.get_by_slug(slug)
        if not product or not product.is_active:
            return None
        self.product_repo.increment_view_count(product.id)
        return product.to_dict(detailed=detailed)

    def get_featured_products(self, limit: int = 8) -> List[Dict[str, Any]]:
        products = self.product_repo.get_featured(limit=limit)
        return [p.to_dict() for p in products]

    def get_related_products(self, product_id: int, limit: int = 4) -> List[Dict[str, Any]]:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            return []
        related = Product.query.filter(
            Product.category_id == product.category_id,
            Product.id != product.id,
            Product.is_active.is_(True)
        ).order_by(Product.average_rating.desc()).limit(limit).all()
        return [p.to_dict() for p in related]

    def get_paginated_products(
        self,
        page: int = 1,
        per_page: int = 20,
        category_id: Optional[int] = None,
        brand: Optional[str] = None,
        sort_by: str = 'featured'
    ) -> Dict[str, Any]:
        query = Product.query.filter_by(is_active=True)
        if category_id:
            query = query.filter_by(category_id=category_id)
        if brand:
            query = query.filter(Product.brand.ilike(f"%{brand}%"))

        if sort_by == 'price_asc':
            query = query.order_by(Product.sale_price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Product.sale_price.desc())
        elif sort_by == 'rating_desc':
            query = query.order_by(Product.average_rating.desc())
        else:
            query = query.order_by(Product.is_featured.desc(), Product.average_rating.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next
        }
