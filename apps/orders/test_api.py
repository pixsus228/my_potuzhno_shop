import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.orders.models import Order
from apps.shop.models import Category, Product

User = get_user_model()

@pytest.mark.django_db
class TestOrderApi:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Тест Категорія', slug='test-cat')
        self.product = Product.objects.create(name='Тест Товар', slug='test-prod', price=100.00, category=self.category)
        self.client.force_authenticate(user=self.user)
        self.url = reverse('orders:order-list')

    def test_create_order(self):
        data = {
            "full_name": "Олексій Карнаух",
            "phone": "+380991234567",
            "total_price": "100.00",
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 1,
                    "price": "100.00"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
        assert Order.objects.first().full_name == "Олексій Карнаух"
        # записав тест для перевірки створення замовлення
