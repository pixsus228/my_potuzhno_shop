import pytest
from apps.orders.models import Order

@pytest.mark.django_db
def test_create_order():
    order = Order.objects.create(
        user=None,
        full_name="Максим Потужний",
        address="м. Київ, вул. Хрещатик, 1",
        phone="+380991112233",
        total_price=1500.00
    )
    assert order.id is not None
    assert order.total_price == 1500.00


@pytest.mark.django_db
def test_order_item_snapshot_and_set_null():
    # перевірив збереження знімка товару та зв'язок SET_NULL при видаленні
    from decimal import Decimal
    from apps.shop.models import Product, Category
    from apps.orders.models import Order, OrderItem

    cat = Category.objects.create(name="Штани", slug="pants-cat")
    product = Product.objects.create(name="Карго", price=Decimal("1500.00"), category=cat, stock=5)
    order = Order.objects.create(total_price=Decimal("3000.00"))
    item = OrderItem.objects.create(order=order, product=product, quantity=2)

    assert item.product_name == "Карго"
    assert item.price == Decimal("1500.00")

    product.delete()
    item.refresh_from_db()
    assert item.product is None
    assert item.product_name == "Карго"
    assert item.price == Decimal("1500.00")