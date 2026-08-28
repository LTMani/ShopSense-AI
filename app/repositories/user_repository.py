from datetime import datetime, timezone
from typing import Optional, List
from app.models.user import User, Role
from app.models.profile import CustomerProfile, SellerProfile
from app.repositories.base import BaseRepository
from app.extensions import db


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        if not email:
            return None
        return self.find_one_by(email=email.strip().lower())

    def is_email_registered(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def update_last_login(self, user: User) -> None:
        try:
            user.last_login_at = datetime.now(timezone.utc)
            db.session.commit()
        except Exception:
            db.session.rollback()


class RoleRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(Role)

    def get_by_name(self, name: str) -> Optional[Role]:
        return self.find_one_by(name=name)


class CustomerProfileRepository(BaseRepository[CustomerProfile]):
    def __init__(self):
        super().__init__(CustomerProfile)

    def get_by_user_id(self, user_id: int) -> Optional[CustomerProfile]:
        return self.find_one_by(user_id=user_id)


class SellerProfileRepository(BaseRepository[SellerProfile]):
    def __init__(self):
        super().__init__(SellerProfile)

    def get_by_user_id(self, user_id: int) -> Optional[SellerProfile]:
        return self.find_one_by(user_id=user_id)

    def get_by_slug(self, store_slug: str) -> Optional[SellerProfile]:
        return self.find_one_by(store_slug=store_slug)


class SessionRepository:
    """Ephemeral session lookup DAO."""
    pass
