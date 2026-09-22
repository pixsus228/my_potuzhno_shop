from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.shop.models import Product


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Користувач"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Продукт",
    )
    # встановив рейтинг за замовчуванням 1 та валідатор
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг",
    )
    text = models.TextField(blank=True, null=True, verbose_name="Текст відгуку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["-created_at"]
        unique_together = ("user", "product")

    def __str__(self):
        return f"Відгук від {self.user.username} на {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Користувач"
    )
    products = models.ManyToManyField(
        Product, related_name="reviews_favourited_by", verbose_name="Продукти"
    )

    class Meta:
        verbose_name = "Список бажаного"
        verbose_name_plural = "Списки бажаного"

    def __str__(self):
        return f"Список бажаного від {self.user.username}"
