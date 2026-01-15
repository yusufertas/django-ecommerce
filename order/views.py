from rest_framework import viewsets, mixins
from .models import Order
from .serializers import OrderSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class OrderViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = PageNumberPagination
    view_tags = ["Orders"]

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return OrderSerializer(self.get_queryset(), many=True)

    @swagger_auto_schema(responses={200: OrderSerializer})
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        order = get_object_or_404(Order, pk=pk)
        return OrderSerializer(order)

    @swagger_auto_schema(responses={201: OrderSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    @swagger_auto_schema(responses={200: OrderSerializer})
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        order = get_object_or_404(Order, pk=pk)
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    @swagger_auto_schema(responses={204: OrderSerializer})
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return {"message": "Order deleted successfully"}
