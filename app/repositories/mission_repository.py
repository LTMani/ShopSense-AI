from typing import Optional, List
from app.models.mission import ShoppingMission, ShoppingMissionItem
from app.repositories.base import BaseRepository


class MissionRepository(BaseRepository[ShoppingMission]):
    def __init__(self):
        super().__init__(ShoppingMission)

    def get_by_user(self, user_id: int) -> List[ShoppingMission]:
        return ShoppingMission.query.filter_by(user_id=user_id).order_by(ShoppingMission.created_at.desc()).all()


class MissionItemRepository(BaseRepository[ShoppingMissionItem]):
    def __init__(self):
        super().__init__(ShoppingMissionItem)
