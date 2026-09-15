from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.reviews.views import ReviewViewSet, WishlistViewSet

app_name = 'reviews'

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
]
