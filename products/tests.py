from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
import tempfile
from PIL import Image


class ModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="iPhone 13",
            slug="iphone-13",
            price=999.99,
            stock=10,
            description="The latest iPhone",
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")

    def test_product_str(self):
        self.assertEqual(str(self.product), "iPhone 13")


class CategoryApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Books", slug="books")
        self.url = "/api/category/"

    def test_list_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        data = {"name": "Fashion", "slug": "fashion"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_retrieve_category(self):
        url = f"{self.url}{self.category.category_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Books")

    def test_update_category(self):
        url = f"{self.url}{self.category.category_id}/"
        data = {"name": "Literature"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Literature")

    def test_delete_category(self):
        url = f"{self.url}{self.category.category_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class ProductApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Toys", slug="toys")
        self.product = Product.objects.create(
            category=self.category,
            name="Lego Set",
            slug="lego-set",
            price=49.99,
            stock=5,
            description="Building blocks",
        )
        self.url = "/api/products/"

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        data = {
            "category": self.category.category_id,
            "name": "Action Figure",
            "slug": "action-figure",
            "price": "19.99",
            "stock": 10,
            "description": "Hero figure",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_retrieve_product(self):
        url = f"{self.url}{self.product.product_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Lego Set")

    def test_update_product(self):
        url = f"{self.url}{self.product.product_id}/"
        data = {"price": 59.99}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(float(self.product.price), 59.99)

    def test_delete_product(self):
        url = f"{self.url}{self.product.product_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
