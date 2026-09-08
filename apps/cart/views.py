from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from apps.shop.models import Product
from .services.cart_service import CartService

def cart_add(request, product_id):
    # додав товар через сервіс
    service = CartService(request)
    service.add(product_id)
    product = get_object_or_404(Product, id=product_id)
    messages.success(request, f'Товар {product.name} успішно додано до кошика!')
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))

def cart_increase(request, product_id):
    # збільшив кількість через сервіс
    service = CartService(request)
    service.increase(product_id)
    return redirect('cart:cart_detail')

def cart_decrease(request, product_id):
    # зменшив кількість або видалив через сервіс
    service = CartService(request)
    service.decrease(product_id)
    return redirect('cart:cart_detail')

def cart_detail(request):
    # рендерю кошик з динамічними даними з бази
    service = CartService(request)
    cart, total_price = service.get_cart_data()
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'total_price': total_price})