import os

from django.core.management.utils import get_random_secret_key

from .settings import *

# додав виробничі налаштування безпеки та генерацію безпечного ключа
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_secret_key())
