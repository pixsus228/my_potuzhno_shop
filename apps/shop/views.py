from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Brand, Category, Product, Size
from .serializers.product import ProductSerializer, SizeSerializer


# --- Web Views ---
class HomeView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        # додав фільтрацію за пошуком, категоріями, брендами та сортуванням
        qs = Product.objects.all().select_related('category', 'brand')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        brand_slug = self.request.GET.get('brand')
        if brand_slug:
            qs = qs.filter(brand__slug=brand_slug)

        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')
        else:
            qs = qs.order_by('-id')
        return qs

    def get_context_data(self, **kwargs):
        # записав дані фільтрів у контекст шаблону
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_brand'] = self.request.GET.get('brand', '')
        context['selected_sort'] = self.request.GET.get('sort', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ProductListView(HomeView):
    pass

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

class CategoryProductListView(HomeView):
    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get('slug'))

class BrandProductListView(HomeView):
    def get_queryset(self):
        return super().get_queryset().filter(brand__slug=self.kwargs.get('slug'))

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('/accounts/login/')
    model = Product
    fields = '__all__'
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('shop:product_list')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('/accounts/login/')
    model = Product
    fields = '__all__'
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('shop:product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    success_url = reverse_lazy('shop:product_list')

class ContactView(TemplateView):
    template_name = 'shop/contact.html'

def contact(request):
    return render(request, 'shop/contact.html')

@login_required
def toggle_favourite(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        from apps.reviews.models import Wishlist
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            messages.warning(request, f'Товар {product.name} видалено з обраного.')
        else:
            wishlist.products.add(product)
            messages.success(request, f'Товар {product.name} додано до обраного.')
    except ImportError:
        messages.error(request, "Модуль Wishlist недоступний.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def review_create(request, slug=None):
    if slug:
        product = get_object_or_404(Product, slug=slug)
        if request.method == 'POST':
            text = request.POST.get('text')
            rating = request.POST.get('rating', 5)
            if text:
                from apps.reviews.models import Review
                Review.objects.create(
                    product=product,
                    user=request.user if request.user.is_authenticated else None,
                    text=text,
                    rating=rating
                )
                messages.success(request, 'Дякуємо за ваш відгук!')
                return redirect(product.get_absolute_url())
    return redirect('/')

def review_update(request, pk=None):
    if pk:
        from apps.reviews.models import Review
        review = get_object_or_404(Review, pk=pk)
        if (
            request.user.is_authenticated
            and (request.user == review.user or request.user.is_staff)
            and request.method == 'POST'
        ):
            text = request.POST.get('text')
            rating = request.POST.get('rating', review.rating)
            if text:
                review.text = text
                review.rating = rating
                review.save()
                messages.success(request, 'Відгук оновлено.')
                return redirect(review.product.get_absolute_url())
    return redirect('/')

def review_delete(request, pk=None):
    if pk:
        from apps.reviews.models import Review
        review = get_object_or_404(Review, pk=pk)
        if request.user.is_authenticated and (request.user == review.user or request.user.is_staff):
            review.delete()
            messages.warning(request, 'Відгук видалено.')
    return redirect('/')

# --- API ViewSets ---
class ProductViewSet(viewsets.ModelViewSet):
    # оновив ProductViewSet: lookup_field через slug, додано фільтрацію за is_active
    queryset = Product.objects.all().select_related('category', 'brand')
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['category', 'brand', 'is_active']
    ordering_fields = ['price', 'created_at', 'id']

    def get_queryset(self):
        qs = super().get_queryset()
        is_active = self.request.GET.get('is_active')
        if is_active is not None:
            if is_active.lower() == 'true':
                qs = qs.filter(is_active=True)
            elif is_active.lower() == 'false':
                qs = qs.filter(is_active=False)
        return qs

class SizeViewSet(viewsets.ModelViewSet):
    # додав SizeViewSet для роботи DRF едпоінтів та тестів
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

# Додаю необхідні аліаси для зворотної сумісності з urls.py
def product_create(request, *args, **kwargs):
    return ProductCreateView.as_view()(request, *args, **kwargs)

def product_update(request, *args, **kwargs):
    return ProductUpdateView.as_view()(request, *args, **kwargs)

def product_delete(request, *args, **kwargs):
    return ProductDeleteView.as_view()(request, *args, **kwargs)
