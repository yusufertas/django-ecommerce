from django.urls import path
from rest_framework_json_api.views import ModelViewSet
from .models import Order
from .serializers import OrderSerializer

urlpatterns = [
    path("/orders", OrderViewSet.as_view(), basename="orders"),
]
