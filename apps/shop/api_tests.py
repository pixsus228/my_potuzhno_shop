from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.shop.models import Category, Product


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Електроніка", slug="electronics"
        )
        self.product = Product.objects.create(
            name="Потужний Павербанк",
            slug="powerful-powerbank",
            description="Заряджає все навіть під час блекауту",
            price=2500.00,
            category=self.category,
        )
        self.list_url = reverse("api:product-list")
        self.detail_url = reverse(
            "api:product-detail", kwargs={"slug": self.product.slug}
        )

    def test_get_product_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)
