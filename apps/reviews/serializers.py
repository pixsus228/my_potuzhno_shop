from rest_framework import serializers

from .models import Review, Wishlist


class ReviewSerializer(serializers.ModelSerializer):
    # додав серіалізацію відгуків
    class Meta:
        model = Review
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    # виправлено поле product на products у списку полів
    class Meta:
        model = Wishlist
        fields = ["id", "user", "products"]
