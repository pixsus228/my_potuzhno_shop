from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# Стандартні класи для веб-сайту
from django.views.generic import ListView, DetailView, TemplateView

class HomeView(TemplateView):
    template_name = 'shop/home.html'

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

# API-представлення
class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
