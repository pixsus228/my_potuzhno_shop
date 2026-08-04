from django.db import models
from django.contrib.auth.models import User
from apps.shop.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255, verbose_name="Повне ім'я")
    address = models.TextField(verbose_name="Адреса доставки")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Загальна сума")
    is_paid = models.BooleanField(default=False, verbose_name="Сплачено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f"Замовлення #{self.id} ({self.full_name})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
