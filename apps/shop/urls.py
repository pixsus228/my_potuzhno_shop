from django.urls import path
from .views import HomeView, ProductListView, ProductDetailView, ProductListAPIView

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('api/products/', ProductListAPIView.as_view(), name='product_list_api'),
]
