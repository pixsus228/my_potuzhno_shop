from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm, ProductFilterForm, ContactForm

class HomeView(ListView):
    model = Product
    template_name = "shop/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_featured=True)[:8]

class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

@login_required
def toggle_favourite(request, slug):
    user_profile = request.user.profile
    product = get_object_or_404(Product, slug=slug)
    if user_profile.favourites.filter(pk=product.pk).exists():
        user_profile.favourites.remove(product)
        messages.info(request, "Товар видалено з обраного")
    else:
        user_profile.favourites.add(product)
        messages.success(request, "Товар додано в обране")
    return redirect("shop:product_detail", slug=slug)

def contact(request):
    return render(request, "shop/contact.html")

@login_required
def review_create(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={
                    "rating": form.cleaned_data["rating"],
                    "text": form.cleaned_data["text"]
                }
            )
            if not created:
                review.rating = form.cleaned_data["rating"]
                review.text = form.cleaned_data["text"]
                review.save()
                messages.success(request, "Ваш відгук оновлено!")
            else:
                messages.success(request, "Ваш відгук додано!")
            return redirect("shop:product_detail", slug=slug)
    return redirect("shop:product_detail", slug=slug)

@user_passes_test(lambda u: u.is_staff)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Товар успішно створено!")
            return redirect("shop:product_detail", slug=product.slug)
    else:
        form = ProductForm()
    return render(request, "shop/product_form.html", {"form": form})

@user_passes_test(lambda u: u.is_staff)
def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар оновлено!")
            return redirect("shop:product_detail", slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, "shop/product_form.html", {"form": form, "product": product})

@user_passes_test(lambda u: u.is_staff)
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Товар видалено!")
        return redirect("shop:product_list")
    return render(request, "shop/product_confirm_delete.html", {"product": product})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, "Відгук видалено!")
    return redirect("shop:product_detail", slug=product_slug)
