from django.urls import path
from .views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    toggle_favourite,
    contact,
    review_create,
    product_create,
    product_update,
    product_delete,
    review_delete
)

app_name = "shop"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/add/", product_create, name="product_create"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<slug:slug>/edit/", product_update, name="product_update"),
    path("products/<slug:slug>/delete/", product_delete, name="product_delete"),
    path("products/<slug:slug>/review/", review_create, name="review_create"),
    path("favourite/toggle/<slug:slug>/", toggle_favourite, name="toggle_favourite"),
    path("contact/", contact, name="contact"),
    path("review/<int:pk>/", review_delete, name="review_delete"),
]
