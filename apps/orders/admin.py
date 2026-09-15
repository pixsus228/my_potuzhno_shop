from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "phone",
        "total_price",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("full_name", "phone", "address")
    inlines = [OrderItemInline]
    readonly_fields = ("total_price", "created_at")
