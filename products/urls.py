from django.urls import path
from .serializers import ProductSerializer

urlpatterns = [
    path("/products", ProductViewSet.as_view(), basename="products"),
]
