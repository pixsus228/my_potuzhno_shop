from django import forms
from .models import Product, Category, Brand

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "brand", "name", "slug", "description", "price", "is_active", "is_featured", "sku", "audience", "stock", "sizes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}),
            "slug": forms.TextInput(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}),
            "price": forms.NumberInput(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}),
            "sku": forms.TextInput(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}),
            "stock": forms.NumberInput(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}),
            "category": forms.Select(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}),
            "brand": forms.Select(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}),
            "audience": forms.Select(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}),
            "sizes": forms.CheckboxSelectMultiple(attrs={"class": "text-amber-500 bg-slate-950 border-slate-700 rounded"}),
        }

class ReviewForm(forms.Form):
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.Select(attrs={"class": "bg-slate-950 border border-slate-700 rounded-xl p-2 text-white"}))
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3, "class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}))

class ProductFilterForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Пошук...", "class": "bg-slate-950 border border-slate-700 rounded-xl p-2 text-white text-sm"}))
    min_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Від", "class": "bg-slate-950 border border-slate-700 rounded-xl p-2 text-white text-sm"}))
    max_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "До", "class": "bg-slate-950 border border-slate-700 rounded-xl p-2 text-white text-sm"}))

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "class": "w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white"}))
