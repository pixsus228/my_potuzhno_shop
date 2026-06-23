from django.views.generic import ListView, DetailView, TemplateView
from .models import Product

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