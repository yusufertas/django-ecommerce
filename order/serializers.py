from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        product_id = validated_data.pop("product_id")
        customer_id = validated_data.pop("customer_id")
        product = Product.objects.get(product_id=product_id)
        customer = Customer.objects.get(customer_id=customer_id)
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
        fields = "__all__"
        ref_name = "OrderSerializer"

    class JSONAPIMeta:
        resource_name = "orders"
