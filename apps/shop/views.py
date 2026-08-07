from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

def product_list_view(request):
    # Показуємо абсолютно всі активні товари без обрізання
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
        
    sort = request.GET.get('sort')
    if sort == 'price' or sort == 'price_asc':
        products = products.order_by('price')
    elif sort == '-price' or sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
        
    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories})

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.all() if hasattr(product, 'reviews') else []
    return render(request, 'shop/product_detail.html', {'product': product, 'reviews': reviews})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
