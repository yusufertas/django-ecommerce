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
        self.url = "/api/customers"  # Note: trailing slash handling in standard routers often matters, but let's assume no trailing slash as per urls.py if defined that way.
        # Wait, urls.py had `path("/customers" ...)` which is unusual for standard django (usually it's `customers/`).
        # User defined: path("/customers", ...) in customer/urls.py
        # And in ecommerce/urls.py: router.register(r"customers", ...) -> /api/customers/ (with trailing slash usually)
        # Let's check ecommerce/urls.py again to be sure how it's routed.
        # It used `router.register(r"customers", CustomerViewSet, basename="customers")`.
        # So it should be `/api/customers/`. The user added `customer/urls.py` but also added it to router in `ecommerce/urls.py`.
        # If both are active, it might be confusing.
        # But `router.urls` is included under `api/`. So `/api/customers/` is the standard router path.
        # I will use `/api/customers/`.

    def test_list_customers(self):
        # We need to construct URL correctly.
        url = "/api/customers/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming JSON:API or standard DRF?
        # User installed `django-rest-framework-jsonapi` and `requirements.txt` has it.
        # And serializers have `JSONAPIMeta`.
        # So the response might be JSON:API formatted.
        # Standard valid JSON:API response check strictly might be hard, but let's check status at least.

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
