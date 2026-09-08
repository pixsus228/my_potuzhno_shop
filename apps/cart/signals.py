from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from apps.cart.services.cart_service import CartService

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    # викликаю злиття кошика при авторизації з явною передачею user
    if request is not None and hasattr(request, 'session'):
        service = CartService(request, user=user)
        service.merge_session_cart()