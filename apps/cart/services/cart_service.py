from decimal import Decimal
from django.shortcuts import get_object_or_404
from apps.cart.models import Cart, CartItem
from apps.shop.models import Product

class CartService:
    def __init__(self, request=None, user=None):
        self.request = request
        # безпечно отримую користувача з параметрів або реквесту
        if user is not None:
            self.user = user if getattr(user, 'is_authenticated', False) else None
        else:
            req_user = getattr(request, 'user', None)
            self.user = req_user if (req_user and getattr(req_user, 'is_authenticated', False)) else None

        self.session = getattr(request, 'session', None) if request else None
        if not self.user and self.session is not None:
            self.cart_session = self.session.get('cart', {})
        else:
            self.cart_session = {}

    def _mark_modified(self):
        # зафіксував зміну сесії за наявності відповідного атрибута
        if self.session is not None and hasattr(self.session, 'modified'):
            self.session.modified = True

    def add(self, product_id, quantity=1):
        product = get_object_or_404(Product, id=product_id)
        if self.user:
            # записав позицію в базу даних для авторизованого користувача
            cart, _ = Cart.objects.get_or_create(user=self.user)
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity
            item.save()
        elif self.session is not None:
            # зберіг мінімальні дані в сесію для гостя
            pid = str(product_id)
            current_qty = self.cart_session.get(pid, {}).get('quantity', 0) if isinstance(self.cart_session.get(pid), dict) else self.cart_session.get(pid, 0)
            self.cart_session[pid] = {'quantity': current_qty + quantity}
            self.session['cart'] = self.cart_session
            self._mark_modified()

    def increase(self, product_id):
        if self.user:
            cart = Cart.objects.filter(user=self.user).first()
            if cart:
                item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
                if item:
                    item.quantity += 1
                    item.save()
        elif self.session is not None:
            pid = str(product_id)
            if pid in self.cart_session:
                current_qty = self.cart_session[pid].get('quantity', 1) if isinstance(self.cart_session[pid], dict) else self.cart_session[pid]
                self.cart_session[pid] = {'quantity': current_qty + 1}
                self.session['cart'] = self.cart_session
                self._mark_modified()

    def decrease(self, product_id):
        if self.user:
            cart = Cart.objects.filter(user=self.user).first()
            if cart:
                item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
                if item:
                    if item.quantity > 1:
                        item.quantity -= 1
                        item.save()
                    else:
                        item.delete()
        elif self.session is not None:
            pid = str(product_id)
            if pid in self.cart_session:
                current_qty = self.cart_session[pid].get('quantity', 1) if isinstance(self.cart_session[pid], dict) else self.cart_session[pid]
                if current_qty > 1:
                    self.cart_session[pid] = {'quantity': current_qty - 1}
                else:
                    del self.cart_session[pid]
                self.session['cart'] = self.cart_session
                self._mark_modified()

    def clear(self):
        if self.user:
            # чищу кошик користувача в базі даних
            CartItem.objects.filter(cart__user=self.user).delete()
        if self.session is not None:
            self.session['cart'] = {}
            self._mark_modified()

    def merge_session_cart(self):
        # переношу товари із сесії в базу даних при вході користувача
        if not self.user or not self.session:
            return
        session_cart = self.session.get('cart', {})
        if not session_cart or not isinstance(session_cart, dict):
            return
        cart, _ = Cart.objects.get_or_create(user=self.user)
        for pid_str, val in session_cart.items():
            if not str(pid_str).isdigit():
                continue
            qty = val.get('quantity', 1) if isinstance(val, dict) else int(val)
            product = Product.objects.filter(id=int(pid_str)).first()
            if product:
                item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not created:
                    item.quantity += qty
                else:
                    item.quantity = qty
                item.save()
        self.session['cart'] = {}
        self._mark_modified()

    def get_cart_data(self):
        # отримую актуальні ціни з БД та розраховую суму в Decimal
        cart_data = {}
        total_price = Decimal('0.00')

        if self.user:
            cart = Cart.objects.filter(user=self.user).first()
            if cart:
                for item in cart.items.select_related('product').all():
                    if not item.product:
                        continue
                    p = item.product
                    qty = item.quantity
                    item_total = Decimal(str(p.price)) * qty
                    total_price += item_total
                    img_url = p.image.url if hasattr(p, 'image') and p.image else ''
                    cart_data[str(p.id)] = {
                        'id': p.id,
                        'name': p.name,
                        'price': Decimal(str(p.price)),
                        'quantity': qty,
                        'total_price': item_total,
                        'image': img_url,
                        'product': p
                    }
        elif self.session is not None:
            pids = [int(pid) for pid in self.cart_session.keys() if str(pid).isdigit()]
            products = Product.objects.filter(id__in=pids)
            p_map = {p.id: p for p in products}

            for pid_str, val in list(self.cart_session.items()):
                if not str(pid_str).isdigit():
                    continue
                p = p_map.get(int(pid_str))
                if not p:
                    continue
                qty = val.get('quantity', 1) if isinstance(val, dict) else int(val)
                item_total = Decimal(str(p.price)) * qty
                total_price += item_total
                img_url = p.image.url if hasattr(p, 'image') and p.image else ''
                cart_data[pid_str] = {
                    'id': p.id,
                    'name': p.name,
                    'price': Decimal(str(p.price)),
                    'quantity': qty,
                    'total_price': item_total,
                    'image': img_url,
                    'product': p
                }

        return cart_data, total_price