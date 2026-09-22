from django.db.models import Sum, Count
from apps.orders.models import Order
from django.utils import timezone
from datetime import timedelta
from django.db import models


def get_orders_statistics():
    now = timezone.now()
    month_ago = now - timedelta(days=30)
    stats = Order.objects.aggregate(
        total_revenue=Sum("total_price"),
        total_orders=Count("id"),
        recent_orders=Count("id", filter=models.Q(created_at__gte=month_ago)),
    )
    return stats


def validate_stock(variant, quantity):
    if variant.stock < quantity:
        return False, f"Недостатньо товару на складі. Доступно: {variant.stock}"
    return True, "OK"
