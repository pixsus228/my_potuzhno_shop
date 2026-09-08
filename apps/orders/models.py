from django.db import models
from django.contrib.auth.models import User
from apps.shop.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=100, default='')
    branch = models.CharField(max_length=255, default='')
    payment_method = models.CharField(max_length=50, default='cash')
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default='Pending')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Замовлення №{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # змінив CASCADE на SET_NULL для збереження історії
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    # додав знімок назви товару на момент купівлі
    product_name = models.CharField(max_length=255, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        # записав знімок даних безпосередньо перед збереженням
        if self.product:
            if not self.product_name:
                self.product_name = self.product.name
            if not self.price:
                self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        name = self.product.name if self.product else (self.product_name or "Видалений товар")
        return f"{self.quantity} x {name}"