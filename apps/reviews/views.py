from rest_framework import permissions, viewsets

from apps.reviews.models import Review, Wishlist
from apps.reviews.serializers import ReviewSerializer, WishlistSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ["product", "user", "rating"]


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # додав перевірку для генерації документації swagger
        if getattr(self, "swagger_fake_view", False):
            return Wishlist.objects.none()
        # Фільтруємо обране виключно для поточного авторизованого юзера
        return Wishlist.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )
