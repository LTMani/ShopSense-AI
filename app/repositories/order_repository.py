from typing import Optional, List, Dict, Any
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
