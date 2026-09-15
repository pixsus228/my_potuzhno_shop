import graphene
from graphene_django import DjangoObjectType

from apps.orders.models import Order
from apps.shop.models import Category, Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "price",
            "category",
            "created_at",
        )


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "products")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "user", "created_at", "total_price", "phone", "items")


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product_by_slug = graphene.Field(
        ProductType, slug=graphene.String(required=True)
    )
    all_categories = graphene.List(CategoryType)
    all_orders = graphene.List(OrderType)

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_product_by_slug(self, info, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return None

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_all_orders(self, info):
        return Order.objects.all()


schema = graphene.Schema(query=Query)
