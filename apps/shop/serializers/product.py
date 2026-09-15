from rest_framework import serializers

from apps.shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Ціна товару має бути більшою за 0!"
            )
        return value

    def validate(self, data):
        is_featured = data.get(
            "is_featured", getattr(self.instance, "is_featured", False)
        )
        stock = data.get("stock", getattr(self.instance, "stock", 0))

        if is_featured and stock <= 0:
            raise serializers.ValidationError(
                {
                    "stock": "Пропонований товар (is_featured=True) повинен мати залишок на складі більший за 0!"
                }
            )
        return data


from apps.shop.models import Size


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"
