from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = PageNumberPagination
    view_tags = ["Customers"]

    @swagger_auto_schema(responses={200: CustomerSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return Response(
            data=CustomerSerializer(self.get_queryset(), many=True).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(responses={200: CustomerSerializer})
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        customer = get_object_or_404(Customer, pk=pk)
        return Response(
            data=CustomerSerializer(customer).data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(responses={201: CustomerSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: CustomerSerializer})
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        customer = get_object_or_404(Customer, pk=pk)
        serializer = self.get_serializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={204: CustomerSerializer})
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response(
            data={"message": "Customer deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
