from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order
from products.models import Product, Category
from customer.models import Customer
import datetime


class OrderModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            slug="laptop",
            price=1500.00,
            stock=10,
        )
        self.customer = Customer.objects.create(
            first_name="Alice",
            last_name="Wonder",
            email="alice@example.com",
            phone="123",
            password="pass",
        )
        self.order = Order.objects.create(
            product=self.product,
            customer=self.customer,
            quantity=1,
            price=1500,
            address="123 St",
        )

    def test_order_str(self):
        self.assertEqual(str(self.order), "Laptop - Alice Wonder")


class OrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Home", slug="home")
        self.product = Product.objects.create(
            category=self.category, name="Chair", slug="chair", price=50.00, stock=20
        )
        self.customer = Customer.objects.create(
            first_name="Bob",
            last_name="Builder",
            email="bob@example.com",
            phone="321",
            password="secure",
        )
        self.order = Order.objects.create(
            product=self.product,
            customer=self.customer,
            quantity=2,
            price=100,
            address="456 Ave",
        )
        self.url = "/api/orders/"

    def test_list_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        data = {
            "product_id": self.product.product_id,
            "customer_id": self.customer.customer_id,
            "quantity": 3,
            "price": 150,
            "address": "789 Blvd",
            "phone": "555",
        }
        # Note: OrderSerializer expects 'product_id' and 'customer_id' as PrimaryKeyRelatedField which accepts ID.
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_retrieve_order(self):
        url = f"{self.url}{self.order.order_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order(self):
        url = f"{self.url}{self.order.order_id}/"
        data = {"quantity": 5, "price": 250}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.quantity, 5)
        self.assertEqual(self.order.price, 250)

    def test_delete_order(self):
        url = f"{self.url}{self.order.order_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
