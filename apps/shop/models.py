from django.db import models
from django.utils import timezone

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категорія")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Назва")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Опис", default="Опис відсутній")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name
