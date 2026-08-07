from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import product_list_view, product_detail_view, ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

app_name = 'shop'

urlpatterns = [
    path('', product_list_view, name='product_list'),
    path('products/<slug:slug>/', product_detail_view, name='product_detail'),
    path('api/', include(router.urls)),
]
