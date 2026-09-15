from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "orders"

router = DefaultRouter()
router.register(r"", views.OrderViewSet, basename="order")

urlpatterns = [
    path("checkout/", views.checkout_view, name="checkout"),
    path("", include(router.urls)),
]
