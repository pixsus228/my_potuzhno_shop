from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from apps.shop.views import ProductViewSet, SizeViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'sizes', SizeViewSet, basename='size')

urlpatterns = [
    # Swagger & ReDoc
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),

    path('', include(router.urls)),
]
