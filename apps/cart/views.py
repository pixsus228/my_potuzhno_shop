from django.shortcuts import get_object_or_404, redirect, render
from apps.shop.models import Product
from .models import Cart, CartItem

def cart_detail(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart = None
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()
        
    return redirect('cart:cart_detail')
