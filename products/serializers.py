from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        ref_name = "CategorySerializer"

    class JSONAPIMeta:
        resource_name = "categories"


class ProductSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        category_id = validated_data.pop("category_id")
        category = Category.objects.get(category_id=category_id)
        return Product.objects.create(category=category, **validated_data)

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
        fields = "__all__"
        ref_name = "ProductSerializer"

    class JSONAPIMeta:
        resource_name = "products"
