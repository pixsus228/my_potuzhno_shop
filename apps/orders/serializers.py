from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "full_name",
            "phone",
            "city",
            "branch",
            "payment_method",
            "promo_code",
            "total_price",
            "status",
            "is_paid",
            "created_at",
            "items",
        ]
        read_only_fields = [
            "user",
            "total_price",
            "status",
            "is_paid",
            "created_at",
        ]
