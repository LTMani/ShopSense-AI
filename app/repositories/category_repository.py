from typing import Optional, List
from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return self.find_one_by(slug=slug)

    def get_root_categories(self, active_only: bool = True) -> List[Category]:
        query = Category.query.filter_by(parent_id=None)
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(Category.display_order.asc(), Category.name.asc()).all()

    def get_all_active(self) -> List[Category]:
        return Category.query.filter_by(is_active=True).order_by(Category.display_order.asc()).all()
