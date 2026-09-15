from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.shop.models import Brand, Category, Product

User = get_user_model()

class AdvancedAPITests(APITestCase):
    def setUp(self):
        # Підготовка тестової БД
        self.user = User.objects.create_user(username='jarvis_test', password='StrongPassword123!')
        self.category = Category.objects.create(name='Test Category', slug='test-cat')
        self.brand = Brand.objects.create(name='Test Brand', slug='test-brand')
        
        self.product_active = Product.objects.create(
            name='Active Product', slug='p-active', price=100, stock=10, 
            is_active=True, category=self.category, brand=self.brand
        )
        self.product_inactive = Product.objects.create(
            name='Inactive Product', slug='p-inactive', price=50, stock=0, 
            is_active=False, category=self.category, brand=self.brand
        )

    def test_jwt_token_generation(self):
        # Перевірив видачу токенів доступу
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'jarvis_test', 'password': 'StrongPassword123!'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_product_filtering_by_active_status(self):
        # Перевірив роботу django-filter (фільтрація за is_active)
        url = reverse('api:product-list')
        response = self.client.get(url, {'is_active': 'true'})
        
        self.assertEqual(response.status_code, 200)
        # Має повернути лише 1 активний товар
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Active Product')
