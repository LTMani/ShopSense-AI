from datetime import datetime, timezone, timedelta
import secrets
from typing import Dict, Any, Optional
from app.models.user import User, Role, UserSession
from app.models.profile import CustomerProfile, SellerProfile
from app.models.cart import Cart
from app.models.wishlist import Wishlist
from app.repositories.user_repository import UserRepository, RoleRepository, CustomerProfileRepository, SellerProfileRepository, SessionRepository
from app.extensions import db


class AuthService:
    """Handles secure authentication, registration, session management, and RBAC."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.role_repo = RoleRepository()
        self.customer_profile_repo = CustomerProfileRepository()
        self.seller_profile_repo = SellerProfileRepository()
        self.session_repo = SessionRepository()

    def register_customer(self, email: str, password: str, first_name: str, last_name: str, phone: Optional[str] = None) -> Dict[str, Any]:
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("An account with this email address already exists.")

        role = self.role_repo.get_by_name('customer')
        if not role:
            role = self.role_repo.create(name='customer', display_name='Customer', description='Standard retail customer')

        user = User(
            email=email.strip().lower(),
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            phone=phone.strip() if phone else None,
            role_id=role.id,
            is_active=True,
            is_verified=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        # Initialize Customer Profile, Cart, and Wishlist
        profile = CustomerProfile(user_id=user.id)
        cart = Cart(user_id=user.id)
        wishlist = Wishlist(user_id=user.id, name='My Wishlist')
        db.session.add_all([profile, cart, wishlist])
        db.session.commit()

        return user.to_dict(include_profile=True)

    def register_seller(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        business_name: str,
        store_slug: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("An account with this email address already exists.")

        role = self.role_repo.get_by_name('seller')
        if not role:
            role = self.role_repo.create(name='seller', display_name='Seller', description='Merchant/Seller partner')

        slug = store_slug or business_name.lower().replace(' ', '-').replace('&', 'and')
        # Ensure unique slug
        existing_seller = self.seller_profile_repo.get_by_slug(slug)
        if existing_seller:
            slug = f"{slug}-{secrets.token_hex(2)}"

        user = User(
            email=email.strip().lower(),
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            phone=phone.strip() if phone else None,
            role_id=role.id,
            is_active=True,
            is_verified=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        seller_profile = SellerProfile(
            user_id=user.id,
            business_name=business_name.strip(),
            store_slug=slug,
            business_phone=phone,
            business_email=email
        )
        db.session.add(seller_profile)
        db.session.commit()

        return user.to_dict(include_profile=True)

    def authenticate_user(self, email: str, password: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Optional[User]:
        user = self.user_repo.get_by_email(email)
        if not user or not user.is_active or not user.check_password(password):
            return None

        self.user_repo.update_last_login(user)
        return user

    def create_user_session(self, user_id: int, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> str:
        token = secrets.token_urlsafe(48)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        self.session_repo.create(
            user_id=user_id,
            session_token=token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
            is_active=True
        )
        return token
