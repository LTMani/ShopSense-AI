from datetime import datetime, timezone
from app.extensions import db


class Category(db.Model):
    """Hierarchical product category entity supporting nested catalog classification."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    icon_name = db.Column(db.String(50), default='package', nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Self-referential hierarchy
    parent = db.relationship('Category', remote_side=[id], backref=db.backref('children', lazy='dynamic'))
    products = db.relationship('Product', back_populates='category', lazy='dynamic')

    def to_dict(self, include_children=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'icon_name': self.icon_name,
            'image_url': self.image_url,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'display_order': self.display_order
        }
        if include_children:
            data['children'] = [child.to_dict() for child in self.children.filter_by(is_active=True).all()]
        return data
