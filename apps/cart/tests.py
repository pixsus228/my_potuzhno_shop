import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from apps.cart.models import Cart, CartItem
from apps.cart.services.cart_service import CartService
from apps.shop.models import Product, Category

User = get_user_model()

@pytest.mark.django_db
def test_cart_item_addition():
    cat = Category.objects.create(name="Худі", slug="hoodies")
    product = Product.objects.create(name="Оверсайз Худі", price=1200.00, category=cat)
    user = User.objects.create_user(username="cartuser", password="password123")
    cart = Cart.objects.create(user=user)
    item = CartItem.objects.create(cart=cart, product=product, quantity=2)
    assert item.product.name == "Оверсайз Худі"
    assert item.quantity == 2

@pytest.mark.django_db
def test_cart_merge_on_login_service():
    # перевірив перенесення сесійного кошика в базу даних користувача
    cat = Category.objects.create(name="Мерч", slug="merch")
    product = Product.objects.create(name="Футболка", price=500.00, category=cat, stock=10)
    user = User.objects.create_user(username="merger", password="password123")
    
    rf = RequestFactory()
    request = rf.get("/")
    request.user = user
    request.session = {'cart': {str(product.id): {'quantity': 3}}}
    
    service = CartService(request=request, user=user)
    service.merge_session_cart()
    
    cart = Cart.objects.filter(user=user).first()
    assert cart is not None
    item = cart.items.filter(product=product).first()
    assert item is not None
    assert item.quantity == 3
    assert request.session['cart'] == {}