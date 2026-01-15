from django.db import models
from products.models import Product
from customer.models import Customer
import uuid
import datetime


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=225, default="", blank=True)
    phone = models.CharField(max_length=225, default="", blank=True)
    date = models.DateField(default=datetime.datetime.now)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.customer.first_name} {self.customer.last_name}"
