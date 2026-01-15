from django.urls import path
from rest_framework_json_api.views import ModelViewSet
from .models import Customer
from .serializers import CustomerSerializer

urlpatterns = [
    path("/customers", CustomerViewSet.as_view(), basename="customers"),
]
