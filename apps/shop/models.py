from django.db import models
from django.db.models import Avg, Count


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name


from django.utils.text import slugify


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Розмір')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг', blank=True)

    class Meta:
        verbose_name = 'Розмір'
        verbose_name_plural = 'Розміри'
        ordering = ['name']

    def save(self, *args, **kwargs):
        # додав автогенерацію слагу перед збереженням
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def with_rating(self):
        return self.annotate(
            avg_rating=Avg("reviews__rating"),
            reviews_count=Count("reviews", distinct=True),
        )


class Product(models.Model):
    AUDIENCE_CHOICES = [
        ("unisex", "Унісекс"),
        ("man", "Чоловіче"),
        ("woman", "Жіноче"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=False,
        related_name="products",
        related_query_name="product"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, verbose_name="Пропонований?")

    sku = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        null=True, blank=True,
        verbose_name="Артикул",
    )

    audience = models.CharField(
        max_length=10,
        choices=AUDIENCE_CHOICES,
        default="unisex",
        verbose_name="Аудиторія"
    )

    stock = models.PositiveIntegerField(default=0, verbose_name="Залишок")
    sizes = models.ManyToManyField(Size, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    objects = ProductQuerySet.as_manager()
