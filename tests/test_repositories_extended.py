from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.wishlist_repository import WishlistRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.inventory_repository import InventoryRepository


def test_user_repository_methods(app):
    with app.app_context():
        repo = UserRepository()
        u = repo.get_by_email('customer@shopsense.ai')
        assert u is not None
        assert u.email == 'customer@shopsense.ai'
        assert repo.is_email_registered('customer@shopsense.ai') is True
        assert repo.is_email_registered('random_nonexistent@test.com') is False


def test_product_repository_methods(app):
    with app.app_context():
        repo = ProductRepository()
        featured = repo.get_featured(limit=3)
        assert len(featured) > 0
        first_prod = featured[0]
        by_slug = repo.get_by_slug(first_prod.slug)
        assert by_slug is not None
        assert by_slug.id == first_prod.id


def test_order_repository_methods(app):
    with app.app_context():
        u_repo = UserRepository()
        o_repo = OrderRepository()
        u = u_repo.get_by_email('customer@shopsense.ai')
        orders = o_repo.get_by_user(u.id, limit=5)
        assert isinstance(orders, list)


def test_inventory_repository_methods(app):
    with app.app_context():
        p_repo = ProductRepository()
        i_repo = InventoryRepository()
        prod = p_repo.get_all()[0]
        inv = i_repo.get_by_product_id(prod.id)
        if inv:
            assert inv.product_id == prod.id
