import unittest

from urllib.parse import quote_plus

from flask_api import status

from service import app
from service.models import Product
from tests.factories import ProductFactory


BASE_URL = "/products"


class TestProductRoutes(unittest.TestCase):
    """Test Product API routes"""

    def setUp(self):
        """Runs before each test"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False

        self.client = app.test_client()

        with app.app_context():
            Product.remove_all()

    def tearDown(self):
        """Runs after each test"""
        with app.app_context():
            Product.remove_all()

    def _create_products(self, count=1):
        """Create products for testing"""
        products = []

        for _ in range(count):
            product = ProductFactory()
            product.create()
            products.append(product)

        return products

    def get_product_count(self):
        """Get number of products"""
        return Product.query.count()

    def test_get_product(self):
        """It should Get a single Product"""
        products = self._create_products(1)
        test_product = products[0]

        response = self.client.get(
            f"{BASE_URL}/{test_product.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        data = response.get_json()

        self.assertEqual(
            data["id"],
            test_product.id
        )

        self.assertEqual(
            data["name"],
            test_product.name
        )

    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = ProductFactory()

        response = self.client.post(
            BASE_URL,
            json=test_product.serialize()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        new_product = response.get_json()

        new_product["description"] = "unknown"

        response = self.client.put(
            f"{BASE_URL}/{new_product['id']}",
            json=new_product
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        updated_product = response.get_json()

        self.assertEqual(
            updated_product["description"],
            "unknown"
        )

    def test_delete_product(self):
        """It should Delete a Product"""
        products = self._create_products(5)

        product_count = self.get_product_count()

        test_product = products[0]

        response = self.client.delete(
            f"{BASE_URL}/{test_product.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            len(response.data),
            0
        )

        response = self.client.get(
            f"{BASE_URL}/{test_product.id}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        new_count = self.get_product_count()

        self.assertEqual(
            new_count,
            product_count - 1
        )

    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)

        response = self.client.get(BASE_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        data = response.get_json()

        self.assertEqual(
            len(data),
            5
        )

    def test_query_by_name(self):
        """It should Query Products by name"""
        products = self._create_products(5)

        test_name = products[0].name

        name_count = len(
            [
                product
                for product in products
                if product.name == test_name
            ]
        )

        response = self.client.get(
            BASE_URL,
            query_string={
                "name": test_name
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        data = response.get_json()

        self.assertEqual(
            len(data),
            name_count
        )

        for product in data:
            self.assertEqual(
                product["name"],
                test_name
            )

    def test_query_by_category(self):
        """It should Query Products by category"""
        products = self._create_products(10)

        category = products[0].category

        found = [
            product
            for product in products
            if product.category == category
        ]

        found_count = len(found)

        response = self.client.get(
            BASE_URL,
            query_string={
                "category": category.name
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        data = response.get_json()

        self.assertEqual(
            len(data),
            found_count
        )

        for product in data:
            self.assertEqual(
                product["category"],
                category.name
            )

    def test_query_by_availability(self):
        """It should Query Products by availability"""
        products = self._create_products(10)

        available_products = [
            product
            for product in products
            if product.available is True
        ]

        available_count = len(available_products)

        response = self.client.get(
            BASE_URL,
            query_string={
                "available": "true"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        data = response.get_json()

        self.assertEqual(
            len(data),
            available_count
        )

        for product in data:
            self.assertEqual(
                product["available"],
                True
            )
