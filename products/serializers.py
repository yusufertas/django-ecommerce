from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        ref_name = "CategorySerializer"

    class JSONAPIMeta:
        resource_name = "categories"


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.stock = validated_data.get("stock", instance.stock)
        instance.description = validated_data.get("description", instance.description)
        instance.image = validated_data.get("image", instance.image)
        instance.price = validated_data.get("price", instance.price)
        instance.available = validated_data.get("available", instance.available)
        instance.save()
        return instance

    class Meta:
        model = Product
        fields = (
            "product_id",
            "category",
            "name",
            "slug",
            "image",
            "description",
            "price",
            "stock",
            "available",
            "created_at",
            "updated_at",
        )
        ref_name = "ProductSerializer"
        extra_kwargs = {
            "category": {"required": True},
            "product_id": {"read_only": True},
        }

    class JSONAPIMeta:
        resource_name = "products"
