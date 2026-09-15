from datetime import timedelta

from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone

from apps.orders.models import Order


def get_orders_statistics():
    now = timezone.now()
    month_ago = now - timedelta(days=30)
    return Order.objects.aggregate(
        total_revenue=Sum("total_price"),
        total_orders=Count("id"),
        recent_orders=Count("id", filter=models.Q(created_at__gte=month_ago)),
    )


def validate_stock(variant, quantity):
    if variant.stock < quantity:
        return (
            False,
            f"Недостатньо товару на складі. Доступно: {variant.stock}",
        )
    return True, "OK"
