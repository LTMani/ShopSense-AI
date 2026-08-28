# ShopSense AI Repositories Generator
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / 'app' / 'repositories'
BASE.mkdir(parents=True, exist_ok=True)

# 1. base.py
(BASE / 'base.py').write_text('''from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from app.extensions import db

T = TypeVar('T', bound=db.Model)


class BaseRepository(Generic[T]):
    """Generic Data Access Object providing robust CRUD, pagination, and atomic transaction operations."""

    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self.model_class.query.get(entity_id)

    def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        query = self.model_class.query
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def filter_by(self, **kwargs) -> List[T]:
        return self.model_class.query.filter_by(**kwargs).all()

    def find_one_by(self, **kwargs) -> Optional[T]:
        return self.model_class.query.filter_by(**kwargs).first()

    def create(self, **kwargs) -> T:
        instance = self.model_class(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def save(self, instance: T) -> T:
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        db.session.commit()
        return instance

    def delete(self, instance: T) -> bool:
        db.session.delete(instance)
        db.session.commit()
        return True

    def delete_by_id(self, entity_id: int) -> bool:
        instance = self.get_by_id(entity_id)
        if instance:
            return self.delete(instance)
        return False

    def count(self, **kwargs) -> int:
        query = self.model_class.query
        if kwargs:
            query = query.filter_by(**kwargs)
        return query.count()

    def paginate(self, page: int = 1, per_page: int = 12, **kwargs) -> Dict[str, Any]:
        query = self.model_class.query
        if kwargs:
            query = query.filter_by(**kwargs)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }

    def bulk_create(self, instances: List[T]) -> List[T]:
        db.session.add_all(instances)
        db.session.commit()
        return instances
''', encoding='utf-8')

# 2. user_repository.py
(BASE / 'user_repository.py').write_text('''from datetime import datetime, timezone
from typing import Optional, List
from app.models.user import User, Role, UserSession
from app.models.profile import CustomerProfile, SellerProfile
from app.repositories.base import BaseRepository
from app.extensions import db


class RoleRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(Role)

    def get_by_name(self, name: str) -> Optional[Role]:
        return self.find_one_by(name=name)


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        if not email:
            return None
        return User.query.filter(User.email.ilike(email.strip())).first()

    def get_sellers(self, active_only: bool = True) -> List[User]:
        query = User.query.join(Role).filter(Role.name == 'seller')
        if active_only:
            query = query.filter(User.is_active.is_(True))
        return query.all()

    def get_customers(self, active_only: bool = True) -> List[User]:
        query = User.query.join(Role).filter(Role.name == 'customer')
        if active_only:
            query = query.filter(User.is_active.is_(True))
        return query.all()

    def update_last_login(self, user: User) -> None:
        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()


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

    def get_by_slug(self, slug: str) -> Optional[SellerProfile]:
        return self.find_one_by(store_slug=slug)

    def get_top_rated(self, limit: int = 10) -> List[SellerProfile]:
        return SellerProfile.query.filter_by(is_verified_seller=True).order_by(SellerProfile.average_rating.desc()).limit(limit).all()


class SessionRepository(BaseRepository[UserSession]):
    def __init__(self):
        super().__init__(UserSession)

    def get_active_session(self, token: str) -> Optional[UserSession]:
        return UserSession.query.filter(
            UserSession.session_token == token,
            UserSession.is_active.is_(True),
            UserSession.expires_at > datetime.now(timezone.utc)
        ).first()

    def revoke_session(self, token: str) -> bool:
        session = self.find_one_by(session_token=token)
        if session:
            session.is_active = False
            db.session.commit()
            return True
        return False
''', encoding='utf-8')

# 3. category_repository.py
(BASE / 'category_repository.py').write_text('''from typing import Optional, List
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
''', encoding='utf-8')

# 4. product_repository.py
(BASE / 'product_repository.py').write_text('''from typing import Optional, List, Dict, Any
from sqlalchemy import or_, and_, desc, asc
from app.models.product import Product, ProductAttribute, ProductImage
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
        query = Product.query.filter_by(is_active=True)

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
                        Product.key_features.ilike(pattern)
                    )
                )
            query = query.filter(and_(*term_filters))

        if category_id:
            query = query.filter_by(category_id=category_id)

        if brand:
            query = query.filter(Product.brand.ilike(f"%{brand}%"))

        if min_price is not None:
            query = query.filter(Product.sale_price >= min_price)

        if max_price is not None:
            query = query.filter(Product.sale_price <= max_price)

        if min_rating is not None:
            query = query.filter(Product.average_rating >= min_rating)

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
''', encoding='utf-8')

# 5. inventory_repository.py
(BASE / 'inventory_repository.py').write_text('''from typing import Optional, List
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
''', encoding='utf-8')

# 6. order_repository.py
(BASE / 'order_repository.py').write_text('''from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from app.models.order import Order, OrderItem, OrderStatusHistory
from app.repositories.base import BaseRepository
from app.extensions import db


class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(Order)

    def get_by_order_number(self, order_number: str) -> Optional[Order]:
        return self.find_one_by(order_number=order_number)

    def get_by_user(self, user_id: int, limit: int = 50) -> List[Order]:
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).limit(limit).all()

    def get_seller_orders(self, seller_id: int, limit: int = 50) -> List[Order]:
        return Order.query.join(OrderItem).filter(OrderItem.seller_id == seller_id).distinct().order_by(Order.created_at.desc()).limit(limit).all()

    def get_revenue_summary(self, seller_id: Optional[int] = None, days: int = 30) -> Dict[str, Any]:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        query = db.session.query(
            func.count(Order.id).label('total_orders'),
            func.sum(Order.total_amount).label('total_revenue')
        ).filter(Order.created_at >= since, Order.status != 'cancelled')
        
        if seller_id:
            query = query.join(OrderItem).filter(OrderItem.seller_id == seller_id)

        result = query.first()
        return {
            'total_orders': result.total_orders or 0,
            'total_revenue': float(result.total_revenue or 0.0)
        }


class OrderItemRepository(BaseRepository[OrderItem]):
    def __init__(self):
        super().__init__(OrderItem)

    def get_by_seller(self, seller_id: int, limit: int = 100) -> List[OrderItem]:
        return OrderItem.query.filter_by(seller_id=seller_id).order_by(OrderItem.created_at.desc()).limit(limit).all()

    def get_sales_by_product(self, product_id: int) -> int:
        total = db.session.query(func.sum(OrderItem.quantity)).filter_by(product_id=product_id).scalar()
        return int(total or 0)
''', encoding='utf-8')

# 7. review_repository.py
(BASE / 'review_repository.py').write_text('''from typing import Optional, List, Dict, Any
from sqlalchemy import func
from app.models.review import Review, ReviewAspectRating, ReviewHelpfulness
from app.repositories.base import BaseRepository
from app.extensions import db


class ReviewRepository(BaseRepository[Review]):
    def __init__(self):
        super().__init__(Review)

    def get_by_product(self, product_id: int, limit: int = 50) -> List[Review]:
        return Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).limit(limit).all()

    def get_by_user(self, user_id: int) -> List[Review]:
        return Review.query.filter_by(user_id=user_id).order_by(Review.created_at.desc()).all()

    def get_aspect_breakdown_for_product(self, product_id: int) -> Dict[str, Dict[str, Any]]:
        aspects = db.session.query(
            ReviewAspectRating.aspect_name,
            func.avg(ReviewAspectRating.sentiment_score).label('avg_score'),
            func.count(ReviewAspectRating.id).label('mention_count')
        ).join(Review).filter(Review.product_id == product_id).group_by(ReviewAspectRating.aspect_name).all()

        breakdown = {}
        for a in aspects:
            breakdown[a.aspect_name] = {
                'average_score': round(float(a.avg_score or 0.0) * 100, 1),
                'mention_count': a.mention_count,
                'sentiment': 'positive' if (a.avg_score or 0) >= 0.6 else ('neutral' if (a.avg_score or 0) >= 0.4 else 'negative')
            }
        return breakdown


class ReviewAspectRepository(BaseRepository[ReviewAspectRating]):
    def __init__(self):
        super().__init__(ReviewAspectRating)
''', encoding='utf-8')

# 8. cart_repository.py
(BASE / 'cart_repository.py').write_text('''from typing import Optional
from app.models.cart import Cart, CartItem
from app.repositories.base import BaseRepository
from app.extensions import db


class CartRepository(BaseRepository[Cart]):
    def __init__(self):
        super().__init__(Cart)

    def get_by_user_id(self, user_id: int) -> Optional[Cart]:
        cart = self.find_one_by(user_id=user_id)
        if not cart:
            cart = self.create(user_id=user_id)
        return cart


class CartItemRepository(BaseRepository[CartItem]):
    def __init__(self):
        super().__init__(CartItem)

    def get_item(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        return self.find_one_by(cart_id=cart_id, product_id=product_id)

    def clear_cart(self, cart_id: int) -> None:
        CartItem.query.filter_by(cart_id=cart_id).delete()
        db.session.commit()
''', encoding='utf-8')

# 9. wishlist_repository.py
(BASE / 'wishlist_repository.py').write_text('''from typing import Optional, List
from app.models.wishlist import Wishlist, WishlistItem
from app.repositories.base import BaseRepository
from app.extensions import db


class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self):
        super().__init__(Wishlist)

    def get_by_user_id(self, user_id: int) -> Optional[Wishlist]:
        wishlist = self.find_one_by(user_id=user_id)
        if not wishlist:
            wishlist = self.create(user_id=user_id, name='My Wishlist')
        return wishlist


class WishlistItemRepository(BaseRepository[WishlistItem]):
    def __init__(self):
        super().__init__(WishlistItem)

    def get_item(self, wishlist_id: int, product_id: int) -> Optional[WishlistItem]:
        return self.find_one_by(wishlist_id=wishlist_id, product_id=product_id)

    def get_price_dropped_items(self, user_id: int) -> List[WishlistItem]:
        wishlist = Wishlist.query.filter_by(user_id=user_id).first()
        if not wishlist:
            return []
        items = WishlistItem.query.filter_by(wishlist_id=wishlist.id).all()
        return [i for i in items if i.price_drop_amount > 0]
''', encoding='utf-8')

# 10. mission_repository.py
(BASE / 'mission_repository.py').write_text('''from typing import Optional, List
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
''', encoding='utf-8')

# 11. conversation_repository.py
(BASE / 'conversation_repository.py').write_text('''from typing import Optional, List
from app.models.conversation import Conversation, ConversationMessage, AIInteractionLog
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self):
        super().__init__(Conversation)

    def get_user_conversations(self, user_id: int, copilot_type: str = 'customer_shopping') -> List[Conversation]:
        return Conversation.query.filter_by(
            user_id=user_id,
            copilot_type=copilot_type,
            is_archived=False
        ).order_by(Conversation.updated_at.desc()).all()


class ConversationMessageRepository(BaseRepository[ConversationMessage]):
    def __init__(self):
        super().__init__(ConversationMessage)

    def get_messages(self, conversation_id: int) -> List[ConversationMessage]:
        return ConversationMessage.query.filter_by(conversation_id=conversation_id).order_by(ConversationMessage.created_at.asc()).all()


class AIInteractionLogRepository(BaseRepository[AIInteractionLog]):
    def __init__(self):
        super().__init__(AIInteractionLog)
''', encoding='utf-8')

# 12. analytics_repository.py
(BASE / 'analytics_repository.py').write_text('''from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta, timezone
from sqlalchemy import func
from app.models.analytics import SellerMetricDaily, CustomerSegment, ProductPerformanceScore
from app.repositories.base import BaseRepository
from app.extensions import db


class SellerMetricDailyRepository(BaseRepository[SellerMetricDaily]):
    def __init__(self):
        super().__init__(SellerMetricDaily)

    def get_metrics_range(self, seller_id: int, start_date: date, end_date: date) -> List[SellerMetricDaily]:
        return SellerMetricDaily.query.filter(
            SellerMetricDaily.seller_id == seller_id,
            SellerMetricDaily.metric_date >= start_date,
            SellerMetricDaily.metric_date <= end_date
        ).order_by(SellerMetricDaily.metric_date.asc()).all()

    def get_latest_metrics(self, seller_id: int, days: int = 30) -> List[SellerMetricDaily]:
        start = date.today() - timedelta(days=days)
        return SellerMetricDaily.query.filter(
            SellerMetricDaily.seller_id == seller_id,
            SellerMetricDaily.metric_date >= start
        ).order_by(SellerMetricDaily.metric_date.asc()).all()


class CustomerSegmentRepository(BaseRepository[CustomerSegment]):
    def __init__(self):
        super().__init__(CustomerSegment)


class ProductPerformanceRepository(BaseRepository[ProductPerformanceScore]):
    def __init__(self):
        super().__init__(ProductPerformanceScore)

    def get_dead_stock(self, seller_id: Optional[int] = None) -> List[ProductPerformanceScore]:
        query = ProductPerformanceScore.query.filter_by(is_dead_stock=True)
        if seller_id:
            query = query.filter_by(seller_id=seller_id)
        return query.order_by(ProductPerformanceScore.overall_score.asc()).all()

    def get_top_performers(self, seller_id: Optional[int] = None, limit: int = 10) -> List[ProductPerformanceScore]:
        query = ProductPerformanceScore.query
        if seller_id:
            query = query.filter_by(seller_id=seller_id)
        return query.order_by(ProductPerformanceScore.overall_score.desc()).limit(limit).all()
''', encoding='utf-8')

# 13. forecast_repository.py
(BASE / 'forecast_repository.py').write_text('''from typing import Optional, List
from app.models.forecast import DemandForecast, ForecastEvaluation
from app.repositories.base import BaseRepository


class ForecastRepository(BaseRepository[DemandForecast]):
    def __init__(self):
        super().__init__(DemandForecast)

    def get_latest_by_product(self, product_id: int) -> Optional[DemandForecast]:
        return DemandForecast.query.filter_by(product_id=product_id).order_by(DemandForecast.forecast_date.desc()).first()

    def get_stockout_risks(self, seller_id: Optional[int] = None) -> List[DemandForecast]:
        query = DemandForecast.query.filter_by(stockout_predicted=True)
        if seller_id:
            query = query.filter_by(seller_id=seller_id)
        return query.order_by(DemandForecast.estimated_days_to_stockout.asc()).all()
''', encoding='utf-8')

# 14. tracking_repository.py
(BASE / 'tracking_repository.py').write_text('''from typing import Optional, List
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
''', encoding='utf-8')

# 15. __init__.py
(BASE / '__init__.py').write_text('''from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository, RoleRepository, CustomerProfileRepository, SellerProfileRepository, SessionRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository, ProductAttributeRepository
from app.repositories.inventory_repository import InventoryRepository, InventoryTransactionRepository, InventoryAlertRepository
from app.repositories.order_repository import OrderRepository, OrderItemRepository
from app.repositories.review_repository import ReviewRepository, ReviewAspectRepository
from app.repositories.cart_repository import CartRepository, CartItemRepository
from app.repositories.wishlist_repository import WishlistRepository, WishlistItemRepository
from app.repositories.mission_repository import MissionRepository, MissionItemRepository
from app.repositories.conversation_repository import ConversationRepository, ConversationMessageRepository, AIInteractionLogRepository
from app.repositories.analytics_repository import SellerMetricDailyRepository, CustomerSegmentRepository, ProductPerformanceRepository
from app.repositories.forecast_repository import ForecastRepository
from app.repositories.tracking_repository import BrowsingRepository, SearchRepository, ComparisonRepository

__all__ = [
    'BaseRepository',
    'UserRepository',
    'RoleRepository',
    'CustomerProfileRepository',
    'SellerProfileRepository',
    'SessionRepository',
    'CategoryRepository',
    'ProductRepository',
    'ProductAttributeRepository',
    'InventoryRepository',
    'InventoryTransactionRepository',
    'InventoryAlertRepository',
    'OrderRepository',
    'OrderItemRepository',
    'ReviewRepository',
    'ReviewAspectRepository',
    'CartRepository',
    'CartItemRepository',
    'WishlistRepository',
    'WishlistItemRepository',
    'MissionRepository',
    'MissionItemRepository',
    'ConversationRepository',
    'ConversationMessageRepository',
    'AIInteractionLogRepository',
    'SellerMetricDailyRepository',
    'CustomerSegmentRepository',
    'ProductPerformanceRepository',
    'ForecastRepository',
    'BrowsingRepository',
    'SearchRepository',
    'ComparisonRepository'
]
''', encoding='utf-8')

print('All 15 repository modules written successfully!')
