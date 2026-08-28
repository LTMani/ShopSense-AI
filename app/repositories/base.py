from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
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
