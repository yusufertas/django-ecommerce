from django.urls import path
from .views import ProductViewSet, CategoryViewSet

urlpatterns = [
    path("/products", ProductViewSet.as_view(), basename="products"),
    path("/category", CategoryViewSet.as_view(), basename="category"),
]
