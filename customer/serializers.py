from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.address = validated_data.get("address", instance.address)
        if instance.password != validated_data.get("password", instance.password):
            instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance

    class Meta:
        model = Customer
        fields = "__all__"
        ref_name = "CustomerSerializer"
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    class JSONAPIMeta:
        resource_name = "customers"
