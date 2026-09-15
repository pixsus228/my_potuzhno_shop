from django.contrib.auth.models import User
from django.db import models

from apps.shop.models import Product


class Review(models.Model):
    # додав зв'язок з користувачем
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Користувач"
    )
    # додав зв'язок з продуктом
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Продукт",
    )
    # додав поле рейтингу
    rating = models.IntegerField(default=1, verbose_name="Рейтинг")
    # додав текст відгуку
    text = models.TextField(
        verbose_name="Текст відгуку", blank=True, null=True
    )
    # додав дату створення
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата створення"
    )

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["-created_at"]
        unique_together = ("user", "product")

    def __str__(self):
        return f"Відгук від {self.user.username} на {self.product.name}"


class Wishlist(models.Model):
    # додав зв'язок з користувачем
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Користувач"
    )
    # додав унікальний related_name для уникнення конфлікту з accounts.Profile
    products = models.ManyToManyField(
        Product, related_name="reviews_favourited_by", verbose_name="Продукти"
    )

    class Meta:
        verbose_name = "Список бажаного"
        verbose_name_plural = "Списки бажаного"

    def __str__(self):
        return f"Wishlist для {self.user.username}"
