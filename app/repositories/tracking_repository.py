from typing import Optional, List
from app.models.tracking import BrowsingEvent, SearchHistory, ProductComparison
from app.repositories.base import BaseRepository


class BrowsingRepository(BaseRepository[BrowsingEvent]):
    def __init__(self):
        super().__init__(BrowsingEvent)

    def get_recent_user_views(self, user_id: int, limit: int = 20) -> List[BrowsingEvent]:
        return BrowsingEvent.query.filter_by(user_id=user_id, event_type='view_product').order_by(BrowsingEvent.created_at.desc()).limit(limit).all()


class SearchRepository(BaseRepository[SearchHistory]):
    def __init__(self):
        super().__init__(SearchHistory)

    def get_top_searches(self, limit: int = 10) -> List[SearchHistory]:
        return SearchHistory.query.order_by(SearchHistory.created_at.desc()).limit(limit).all()


class ComparisonRepository(BaseRepository[ProductComparison]):
    def __init__(self):
        super().__init__(ProductComparison)
