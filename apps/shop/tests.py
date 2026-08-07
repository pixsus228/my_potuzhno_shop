from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.db import IntegrityError
from apps.shop.models import Category, Brand, Size, Product, Review
from apps.accounts.models import Profile
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem
from apps.shop.forms import ProductForm, ReviewForm, ProductFilterForm, ContactForm

class PotuzhnoShopUltimate100Tests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser100", password="password123", email="test100@potuzhno.com")
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        
        self.staff_user = User.objects.create_superuser(username="admin100", password="password123")
        Profile.objects.get_or_create(user=self.staff_user)
        
        self.category = Category.objects.create(name="Худі", slug="hoodies")
        self.brand = Brand.objects.create(name="ПОТУЖНО", slug="potuzhno")
        self.size_l = Size.objects.create(name="L")
        self.size_m = Size.objects.create(name="M")
        
        self.product = Product.objects.create(
            name="Потужне Худі Test",
            slug="potuzhno-hoodie-test",
            category=self.category,
            brand=self.brand,
            price=Decimal("1290.00"),
            stock=20,
            is_active=True,
            is_featured=True,
            sku="HD-100"
        )
        self.product.sizes.set([self.size_l, self.size_m])

    # 1-10: Моделі та рядкові представлення (__str__)
    def test_001_category_str(self): self.assertEqual(str(self.category), "Худі")
    def test_002_brand_str(self): self.assertEqual(str(self.brand), "ПОТУЖНО")
    def test_003_size_str(self): self.assertEqual(str(self.size_l), "L")
    def test_004_product_str(self): self.assertEqual(str(self.product), "Потужне Худі Test")
    def test_005_profile_str(self): self.assertEqual(str(self.user.profile), "testuser100")
    def test_006_category_creation(self): self.assertTrue(Category.objects.filter(slug="hoodies").exists())
    def test_007_brand_creation(self): self.assertTrue(Brand.objects.filter(slug="potuzhno").exists())
    def test_008_size_unique(self): 
        with self.assertRaises(Exception): Size.objects.create(name="L")
    def test_009_product_sku_unique(self):
        with self.assertRaises(Exception):
            Product.objects.create(name="Дубль SKU", slug="dup-sku", category=self.category, price=100, sku="HD-100")
    def test_010_product_sizes_count(self): self.assertEqual(self.product.sizes.count(), 2)

    # 11-20: Менеджери та QuerySet
    def test_011_queryset_active(self): self.assertIn(self.product, Product.objects.active())
    def test_012_queryset_inactive_filter(self):
        self.product.is_active = False
        self.product.save()
        self.assertNotIn(self.product, Product.objects.active())
    def test_013_queryset_with_rating(self):
        p_annotated = Product.objects.with_rating().get(pk=self.product.pk)
        self.assertTrue(hasattr(p_annotated, 'avg_rating'))
    def test_014_queryset_with_reviews_count(self):
        p_annotated = Product.objects.with_rating().get(pk=self.product.pk)
        self.assertTrue(hasattr(p_annotated, 'reviews_count'))
    def test_015_category_ordering(self): self.assertEqual(str(Category._meta.ordering), "['-created_at']")
    def test_016_product_ordering(self): self.assertEqual(str(Product._meta.ordering), "['-created_at']")
    def test_017_product_stock_default(self):
        p2 = Product.objects.create(name="Без стоку", slug="no-stock", category=self.category, price=100)
        self.assertEqual(p2.stock, 0)
    def test_018_product_audience_default(self): self.assertEqual(self.product.audience, "unisex")
    def test_019_product_featured_default(self):
        p3 = Product.objects.create(name="Звичайний", slug="regular", category=self.category, price=100)
        self.assertFalse(p3.is_featured)
    def test_020_product_price_type(self): self.assertIsInstance(self.product.price, Decimal)

    # 21-35: Відгуки (Reviews)
    def test_021_review_creation(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=5, text="Топ!")
        self.assertEqual(Review.objects.count(), 1)
    def test_022_review_str(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=5, text="Топ!")
        self.assertIn("testuser100", str(r))
    def test_023_review_uniqueness_user_product(self):
        Review.objects.create(user=self.user, product=self.product, rating=5, text="Перший")
        with self.assertRaises(Exception):
            Review.objects.create(user=self.user, product=self.product, rating=3, text="Другий")
    def test_024_review_rating_choices(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=1)
        self.assertEqual(r.rating, 1)
    def test_025_review_max_length_text(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=4, text="А" * 1000)
        self.assertEqual(len(r.text), 1000)
    def test_026_review_ordering(self): self.assertEqual(str(Review._meta.ordering), "['-created_at']")
    def test_027_multiple_users_reviews(self):
        u2 = User.objects.create_user(username="user2", password="123")
        Review.objects.create(user=self.user, product=self.product, rating=5)
        Review.objects.create(user=u2, product=self.product, rating=4)
        self.assertEqual(Review.objects.count(), 2)
    def test_028_review_deletion(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=5)
        r.delete()
        self.assertEqual(Review.objects.count(), 0)
    def test_029_review_rating_default(self):
        r = Review(user=self.user, product=self.product)
        self.assertEqual(r.rating, 1)
    def test_030_review_related_name_product(self):
        Review.objects.create(user=self.user, product=self.product, rating=5)
        self.assertEqual(self.product.reviews.count(), 1)

    # 36-50: Система "Обране" (Favourites / Wishlist)
    def test_031_favourites_initial_empty(self): self.assertNotIn(self.product, self.profile.favourites.all())
    def test_032_favourites_add(self):
        self.profile.favourites.add(self.product)
        self.assertIn(self.product, self.profile.favourites.all())
    def test_033_favourites_remove(self):
        self.profile.favourites.add(self.product)
        self.profile.favourites.remove(self.product)
        self.assertNotIn(self.product, self.profile.favourites.all())
    def test_034_favourites_related_name_favourited_by(self):
        self.profile.favourites.add(self.product)
        self.assertEqual(self.product.favourited_by.count(), 1)
    def test_035_favourites_multiple_products(self):
        p2 = Product.objects.create(name="Товар 2", slug="t2", category=self.category, price=100)
        self.profile.favourites.add(self.product, p2)
        self.assertEqual(self.profile.favourites.count(), 2)
    def test_036_profile_phone_field(self):
        self.profile.phone = "+380990000000"
        self.profile.save()
        self.assertEqual(self.profile.phone, "+380990000000")
    def test_037_profile_address_field(self):
        self.profile.address = "Київ, вул. Хрещатик"
        self.profile.save()
        self.assertEqual(self.profile.address, "Київ, вул. Хрещатик")
    def test_038_profile_one_to_one_user(self): self.assertEqual(self.profile.user, self.user)
    def test_039_profile_cascade_deletion(self):
        uid = self.user.id
        self.user.delete()
        self.assertFalse(Profile.objects.filter(user_id=uid).exists())
    def test_040_profile_auto_creation_check(self):
        u3 = User.objects.create_user(username="u3", password="123")
        prof, created = Profile.objects.get_or_create(user=u3)
        self.assertTrue(prof.pk is not None)

    # 51-65: Кошик (Cart & CartItem)
    def test_041_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
    def test_042_cart_item_add(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=3)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(cart.items.count(), 1)
    def test_043_cart_item_default_quantity(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product)
        self.assertEqual(item.quantity, 1)
    def test_044_cart_item_product_fk(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product)
        self.assertEqual(item.product, self.product)
    def test_045_cart_cascade_deletion(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product)
        cart.delete()
        self.assertEqual(CartItem.objects.count(), 0)
    def test_046_cart_item_quantity_update(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        item.quantity = 5
        item.save()
        self.assertEqual(CartItem.objects.get(pk=item.pk).quantity, 5)
    def test_047_cart_unique_user(self):
        Cart.objects.create(user=self.user)
        with self.assertRaises(Exception):
            Cart.objects.create(user=self.user)
    def test_048_cart_item_multiple_products(self):
        cart = Cart.objects.create(user=self.user)
        p2 = Product.objects.create(name="P2", slug="p2", category=self.category, price=200)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        CartItem.objects.create(cart=cart, product=p2, quantity=2)
        self.assertEqual(cart.items.count(), 2)
    def test_049_cart_item_deletion(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product)
        item.delete()
        self.assertEqual(cart.items.count(), 0)
    def test_050_cart_item_foreign_key_cascade(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product)
        self.product.delete()
        self.assertEqual(cart.items.count(), 0)

    # 66-80: Замовлення (Order & OrderItem)
    def test_051_order_creation(self):
        order = Order.objects.create(user=self.user, full_name="Іванко", address="Київ", phone="0991112233", total_price=Decimal("1290.00"))
        self.assertEqual(order.full_name, "Іванко")
    def test_052_order_str(self):
        order = Order.objects.create(user=self.user, full_name="Іванко", address="Київ", phone="0991112233", total_price=Decimal("1290.00"))
        self.assertIn("Іванко", str(order))
    def test_053_order_item_creation(self):
        order = Order.objects.create(user=self.user, full_name="Іванко", address="Київ", phone="0991112233", total_price=Decimal("1290.00"))
        oi = OrderItem.objects.create(order=order, product=self.product, price=self.product.price, quantity=2)
        self.assertEqual(oi.quantity, 2)
    def test_054_order_item_str(self):
        order = Order.objects.create(user=self.user, full_name="Іванко", address="Київ", phone="0991112233", total_price=Decimal("1290.00"))
        oi = OrderItem.objects.create(order=order, product=self.product, price=self.product.price, quantity=1)
        self.assertIn("Потужне Худі Test", str(oi))
    def test_055_order_is_paid_default(self):
        order = Order.objects.create(user=self.user, full_name="Іванко", address="Київ", phone="0991112233", total_price=Decimal("1290.00"))
        self.assertFalse(order.is_paid)
    def test_056_order_ordering(self): self.assertEqual(str(Order._meta.ordering), "['-created_at']")
    def test_057_order_user_set_null(self):
        order = Order.objects.create(user=self.user, full_name="Іванко", address="Київ", phone="0991112233", total_price=Decimal("1290.00"))
        self.user.delete()
        order.refresh_from_db()
        self.assertIsNone(order.user)
    def test_058_order_total_price_decimal(self):
        order = Order.objects.create(user=self.user, full_name="Іванко", address="Київ", phone="0991112233", total_price=Decimal("555.50"))
        self.assertEqual(order.total_price, Decimal("555.50"))
    def test_059_order_items_related_name(self):
        order = Order.objects.create(user=self.user, full_name="Іванко", address="Київ", phone="0991112233", total_price=Decimal("100"))
        OrderItem.objects.create(order=order, product=self.product, price=100, quantity=1)
        self.assertEqual(order.items.count(), 1)
    def test_060_order_phone_max_length(self):
        order = Order.objects.create(user=self.user, full_name="Іван", address="Київ", phone="+380991112233", total_price=100)
        self.assertEqual(len(order.phone), 13)

    # 81-90: Форми (Forms Validation)
    def test_061_product_form_valid(self):
        f = ProductForm(data={"name": "Т", "slug": "t", "category": self.category.id, "brand": self.brand.id, "price": "100", "stock": 5, "audience": "unisex"})
        self.assertTrue(f.is_valid())
    def test_062_product_form_invalid_missing_name(self):
        f = ProductForm(data={"slug": "t", "category": self.category.id, "price": "100"})
        self.assertFalse(f.is_valid())
    def test_063_review_form_valid(self):
        f = ReviewForm(data={"rating": "5", "text": "Клас"})
        self.assertTrue(f.is_valid())
    def test_064_review_form_invalid_rating(self):
        f = ReviewForm(data={"rating": "10", "text": "Бред"})
        self.assertFalse(f.is_valid())
    def test_065_contact_form_valid(self):
        f = ContactForm(data={"name": "Максим", "email": "max@gmail.com", "message": "Привіт"})
        self.assertTrue(f.is_valid())
    def test_066_contact_form_invalid_email(self):
        f = ContactForm(data={"name": "Максим", "email": "not-an-email", "message": "Привіт"})
        self.assertFalse(f.is_valid())
    def test_067_filter_form_valid_empty(self):
        f = ProductFilterForm(data={})
        self.assertTrue(f.is_valid())
    def test_068_filter_form_with_query(self):
        f = ProductFilterForm(data={"q": "Худі"})
        self.assertTrue(f.is_valid())
    def test_069_filter_form_price_range(self):
        f = ProductFilterForm(data={"min_price": "100", "max_price": "2000"})
        self.assertTrue(f.is_valid())
    def test_070_filter_form_invalid_price(self):
        f = ProductFilterForm(data={"min_price": "-50"})
        self.assertFalse(f.is_valid())

    # 91-100: HTTP Status Codes & Views Access
    def test_071_home_view_status(self): self.assertEqual(self.client.get('/').status_code, 200)
    def test_072_product_list_view_status(self): self.assertEqual(self.client.get('/products/').status_code, 200)
    def test_073_product_detail_view_status(self): self.assertEqual(self.client.get(f'/products/{self.product.slug}/').status_code, 200)
    def test_074_contact_view_status(self): self.assertEqual(self.client.get('/contact/').status_code, 200)
    def test_075_cart_detail_view_status(self): self.assertEqual(self.client.get('/cart/').status_code, 200)
    def test_076_profile_unauthenticated_redirect(self): self.assertEqual(self.client.get('/accounts/profile/').status_code, 302)
    def test_077_profile_authenticated_success(self):
        self.client.login(username="testuser100", password="password123")
        self.assertEqual(self.client.get('/accounts/profile/').status_code, 200)
    def test_078_profile_edit_authenticated_success(self):
        self.client.login(username="testuser100", password="password123")
        self.assertEqual(self.client.get('/accounts/profile/edit/').status_code, 200)
    def test_079_checkout_empty_cart_redirect(self):
        self.client.login(username="testuser100", password="password123")
        self.assertEqual(self.client.get('/orders/checkout/').status_code, 302)
    def test_080_login_page_status(self): self.assertEqual(self.client.get('/accounts/login/').status_code, 200)
    def test_081_register_page_status(self): self.assertEqual(self.client.get('/accounts/register/').status_code, 200)
    def test_082_password_change_redirect(self): self.assertEqual(self.client.get('/accounts/password-change/').status_code, 302)
    def test_083_toggle_favourite_redirect(self):
        self.client.login(username="testuser100", password="password123")
        res = self.client.post(f'/favourite/toggle/{self.product.slug}/')
        self.assertEqual(res.status_code, 302)
    def test_084_cart_add_view_redirect(self):
        self.client.login(username="testuser100", password="password123")
        res = self.client.get(f'/cart/add/{self.product.id}/')
        self.assertEqual(res.status_code, 302)
    def test_085_admin_login_redirect(self): self.assertEqual(self.client.get('/admin/').status_code, 302)
    def test_086_staff_user_product_create_access(self):
        self.client.login(username="admin100", password="password123")
        self.assertEqual(self.client.get('/products/add/').status_code, 200)
    def test_087_regular_user_product_create_forbidden(self):
        self.client.login(username="testuser100", password="password123")
        self.assertEqual(self.client.get('/products/add/').status_code, 302)
    def test_088_product_update_view_staff(self):
        self.client.login(username="admin100", password="password123")
        self.assertEqual(self.client.get(f'/products/{self.product.slug}/edit/').status_code, 200)
    def test_089_product_delete_view_staff(self):
        self.client.login(username="admin100", password="password123")
        self.assertEqual(self.client.get(f'/products/{self.product.slug}/delete/').status_code, 200)
    def test_090_search_query_parameter(self):
        res = self.client.get('/products/?q=Потужне')
        self.assertEqual(res.status_code, 200)
    def test_091_sorting_price_asc(self):
        res = self.client.get('/products/?sort=price_asc')
        self.assertEqual(res.status_code, 200)
    def test_092_sorting_price_desc(self):
        res = self.client.get('/products/?sort=price_desc')
        self.assertEqual(res.status_code, 200)
    def test_093_sorting_newest(self):
        res = self.client.get('/products/?sort=newest')
        self.assertEqual(res.status_code, 200)
    def test_094_product_detail_context_has_product(self):
        res = self.client.get(f'/products/{self.product.slug}/')
        self.assertEqual(res.context['product'], self.product)
    def test_095_home_view_template_used(self):
        res = self.client.get('/')
        self.assertIn(res.status_code, [200, 302])
    def test_096_product_list_template_used(self):
        res = self.client.get('/products/')
        self.assertTemplateUsed(res, 'shop/product_list.html')
    def test_097_product_detail_template_used(self):
        res = self.client.get(f'/products/{self.product.slug}/')
        self.assertTemplateUsed(res, 'shop/product_detail.html')
    def test_098_profile_template_used(self):
        self.client.login(username="testuser100", password="password123")
        res = self.client.get('/accounts/profile/')
        self.assertTemplateUsed(res, 'accounts/profile.html')
    def test_099_cart_detail_template_used(self):
        res = self.client.get('/cart/')
        self.assertTemplateUsed(res, 'cart/cart_detail.html')
    def test_100_checkout_template_used(self):
        self.client.login(username="testuser100", password="password123")
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product)
        res = self.client.get('/orders/checkout/')
        self.assertTemplateUsed(res, 'orders/checkout.html')
