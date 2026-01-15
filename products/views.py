from rest_framework import viewsets, mixins
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    view_tags = ["Categories"]


class ProductViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    parser_classes = (MultiPartParser, FormParser)
    view_tags = ["Products"]

    @swagger_auto_schema(responses={200: ProductSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return Response(
            data=ProductSerializer(self.get_queryset(), many=True).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(responses={200: ProductSerializer})
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        product = get_object_or_404(Product, pk=pk)
        return Response(data=ProductSerializer(product).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={201: ProductSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: ProductSerializer})
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        product = get_object_or_404(Product, pk=pk)
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={204: ProductSerializer})
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(
            data={"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
