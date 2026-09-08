from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.db.models import F
from rest_framework import viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer
from apps.shop.models import Product
from apps.cart.services.cart_service import CartService

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)

def checkout_view(request):
    cart_service = CartService(request)
    cart, total_price = cart_service.get_cart_data()

    if not cart:
        messages.warning(request, "Ваш кошик порожній!")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        branch = request.POST.get('branch', '')
        address = f"{city}, {branch}"
        payment_method = request.POST.get('payment_method', 'cash')
        promo_code = request.POST.get('promo_code', '')
        user = request.user if request.user.is_authenticated else None

        # обгортаю оформлення замовлення в атомарну транзакцію
        with transaction.atomic():
            final_total = Decimal('0.00')
            items_payload = []

            for pid, item in cart.items():
                # блокую товар на час операції для уникнення race condition
                product = Product.objects.select_for_update().filter(id=int(pid)).first()
                if product:
                    qty = item['quantity']
                    # перевірив залишок товару на складі
                    if hasattr(product, 'stock') and product.stock > 0 and product.stock < qty:
                        messages.error(request, f"Товару {product.name} недостатньо на складі.")
                        return redirect('cart:cart_detail')

                    price = Decimal(str(product.price))
                    final_total += price * qty
                    items_payload.append({
                        'product': product,
                        'product_name': product.name,
                        'price': price,
                        'quantity': qty
                    })

                    # списав залишок зі складу через F-вираз
                    if hasattr(product, 'stock') and product.stock >= qty:
                        Product.objects.filter(id=product.id).update(stock=F('stock') - qty)

            order = Order.objects.create(
                user=user,
                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                branch=branch,
                payment_method=payment_method,
                promo_code=promo_code,
                total_price=final_total,
                status='Pending'
            )

            for payload in items_payload:
                # зафіксував позицію знімком даних
                OrderItem.objects.create(
                    order=order,
                    product=payload['product'],
                    product_name=payload['product_name'],
                    price=payload['price'],
                    quantity=payload['quantity']
                )

            # чищу кошик після успішного збереження
            cart_service.clear()

        try:
            send_mail(
                f"Замовлення №{order.id} прийнято",
                f"Дякуємо за покупку, Сер! Ваше замовлення на суму {final_total} ₴ успішно оформлено.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email] if user and user.email else [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, f"Замовлення №{order.id} успішно оформлено!")
        return render(request, 'orders/success.html', {'order': order})

    return render(request, 'orders/checkout.html', {'cart': cart, 'total_price': total_price})