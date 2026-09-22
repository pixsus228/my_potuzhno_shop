from django.db import models
from django.conf import settings
from apps.shop.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Користувач",
    )
    full_name = models.CharField(max_length=255, verbose_name="ПІБ")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адреса доставки")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Загальна сума"
    )
    status = models.CharField(max_length=50, default="Pending", verbose_name="Статус")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk and self.items.exists():
            self.total_price = sum(item.get_total_price() for item in self.items.all())
            super().save(update_fields=["total_price"])

    def __str__(self):
        return f"Замовлення №{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Замовлення"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Товар"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    # додав знімок назви товару для збереження історії
    product_name = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Назва товару (знімок)"
    )

    def save(self, *args, **kwargs):
        if not self.price and self.product:
            self.price = self.product.price
        if not self.product_name and self.product:
            self.product_name = self.product.name
        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        name = (
            self.product.name
            if self.product
            else (self.product_name or "Видалений товар")
        )
        return f"{self.quantity} x {name}"
