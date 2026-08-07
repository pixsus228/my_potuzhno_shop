from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адреса доставки")
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, verbose_name="Фото профілю")
    
    favourites = models.ManyToManyField(
        "shop.Product",
        related_name="favourited_by",
        blank=True
    )

    def __str__(self):
        return self.user.username
