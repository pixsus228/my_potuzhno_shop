from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.cart.models import Cart
from .models import Order, OrderItem

def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, "Ваш кошик порожній!")
        return redirect('cart:cart_detail')
        
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            address=address,
            phone=phone,
            total_price=total_price
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )

        # Очищуємо кошик після створення замовлення
        cart.items.all().delete()
        
        # Перенаправляємо на сторінку симуляції оплати
        return redirect('orders:payment', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        order.is_paid = True
        order.save()
        messages.success(request, f"Замовлення #{order.id} успішно оплачено! Дякуємо за покупку ⚡")
        return redirect('shop:product_list')
        
    return render(request, 'orders/payment.html', {'order': order})
