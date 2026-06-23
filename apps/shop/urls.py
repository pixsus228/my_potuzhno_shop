from django.urls import path
from .views import HomeView, ProductListView, ProductDetailView

app_name = "shop"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]