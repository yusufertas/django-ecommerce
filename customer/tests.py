from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer


class CustomerModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            password="password123",
        )

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "John Doe")

    def test_set_password(self):
        self.customer.set_password("newpassword")
        self.assertNotEqual(self.customer.password, "newpassword")
        self.assertTrue(self.customer.check_password("newpassword"))


class CustomerApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="0987654321",
            password="secretpassword",
        )
        self.url = "/api/customers"

    def test_list_customers(self):
        # We need to construct URL correctly.
        url = "/api/customers/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_customer(self):
        url = "/api/customers/"
        data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "phone": "5555555555",
            "password": "securepassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)

    def test_retrieve_customer(self):
        url = f"/api/customers/{self.customer.customer_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Jane")

    def test_update_customer_password(self):
        url = f"/api/customers/{self.customer.customer_id}/"
        data = {"password": "newsecurepassword"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertTrue(self.customer.check_password("newsecurepassword"))

    def test_update_customer_details(self):
        url = f"/api/customers/{self.customer.customer_id}/"
        data = {"first_name": "Janet", "phone": "1112223333"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, "Janet")
        self.assertEqual(self.customer.phone, "1112223333")

    def test_delete_customer(self):
        url = f"/api/customers/{self.customer.customer_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)
