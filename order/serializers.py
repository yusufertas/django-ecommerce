from rest_framework import serializers
from .models import Order
from products.models import Product
from customer.models import Customer
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404


class OrderSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    def create(self, validated_data):
        product = validated_data.pop("product_id")
        customer = validated_data.pop("customer_id")
        return Order.objects.create(
            product=product, customer=customer, **validated_data
        )

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.price = validated_data.get("price", instance.price)
        instance.address = validated_data.get("address", instance.address)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    class Meta:
        model = Order
        fields = [
            "product_id",
            "customer_id",
            "quantity",
            "price",
            "address",
            "phone",
            "status",
        ]
        ref_name = "OrderSerializer"

    class JSONAPIMeta:
        resource_name = "orders"
