from typing import Optional, List, Dict, Any
from sqlalchemy import or_, and_, desc, asc
from app.models.product import Product, ProductAttribute, ProductImage
from app.models.category import Category
from app.repositories.base import BaseRepository
from app.extensions import db


class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)

    def get_by_sku(self, sku: str) -> Optional[Product]:
        return self.find_one_by(sku=sku)

    def get_by_slug(self, slug: str) -> Optional[Product]:
        return self.find_one_by(slug=slug)

    def get_featured(self, limit: int = 8) -> List[Product]:
        return Product.query.filter_by(is_active=True, is_featured=True).order_by(Product.average_rating.desc()).limit(limit).all()

    def get_by_seller(self, seller_id: int, active_only: bool = False) -> List[Product]:
        query = Product.query.filter_by(seller_id=seller_id)
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(Product.created_at.desc()).all()

    def get_by_category(self, category_id: int, limit: int = 20) -> List[Product]:
        return Product.query.filter_by(category_id=category_id, is_active=True).order_by(Product.average_rating.desc()).limit(limit).all()

    def search_products(
        self,
        query_text: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        brand: Optional[str] = None,
        min_rating: Optional[float] = None,
        in_stock_only: bool = False,
        sort_by: str = 'relevance',
        page: int = 1,
        per_page: int = 12
    ) -> Dict[str, Any]:
        query = Product.query.join(Category).filter(Product.is_active.is_(True))

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if brand:
            query = query.filter(Product.brand.ilike(f"%{brand}%"))

        if min_price is not None:
            query = query.filter(Product.sale_price >= min_price)

        if max_price is not None:
            query = query.filter(Product.sale_price <= max_price)

        if min_rating is not None:
            query = query.filter(Product.average_rating >= min_rating)

        if query_text and query_text.strip():
            terms = query_text.strip().split()
            term_filters = []
            for t in terms:
                pattern = f"%{t}%"
                term_filters.append(
                    or_(
                        Product.title.ilike(pattern),
                        Product.brand.ilike(pattern),
                        Product.short_description.ilike(pattern),
                        Product.target_usage.ilike(pattern),
                        Product.key_features.ilike(pattern),
                        Category.name.ilike(pattern)
                    )
                )
            query = query.filter(or_(*term_filters))

        # Sorting strategy
        if sort_by == 'price_asc':
            query = query.order_by(Product.sale_price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Product.sale_price.desc())
        elif sort_by == 'rating':
            query = query.order_by(Product.average_rating.desc(), Product.total_reviews_count.desc())
        elif sort_by == 'popularity':
            query = query.order_by(Product.purchases_count.desc(), Product.views_count.desc())
        elif sort_by == 'newest':
            query = query.order_by(Product.created_at.desc())
        else:  # default 'relevance'
            query = query.order_by(Product.is_featured.desc(), Product.average_rating.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }

    def increment_view_count(self, product_id: int) -> None:
        Product.query.filter_by(id=product_id).update({Product.views_count: Product.views_count + 1})
        db.session.commit()


class ProductAttributeRepository(BaseRepository[ProductAttribute]):
    def __init__(self):
        super().__init__(ProductAttribute)

    def get_by_product(self, product_id: int) -> List[ProductAttribute]:
        return ProductAttribute.query.filter_by(product_id=product_id).order_by(ProductAttribute.display_order.asc()).all()
