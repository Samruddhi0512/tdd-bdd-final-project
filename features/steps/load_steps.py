import requests

from behave import given

from flask_api import status


@given("the following products")
def step_impl(context):
    """Delete all existing products and load new products"""

    rest_endpoint = f"{context.base_url}/products"

    # Get all existing products
    context.resp = requests.get(rest_endpoint)

    assert context.resp.status_code == status.HTTP_200_OK

    # Delete existing products
    for product in context.resp.json():
        context.resp = requests.delete(
            f"{rest_endpoint}/{product['id']}"
        )

        assert (
            context.resp.status_code
            == status.HTTP_204_NO_CONTENT
        )

    # Load products from the feature file
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "available": row["available"]
            in ["True", "true", "1"],
            "category": row["category"],
        }

        context.resp = requests.post(
            rest_endpoint,
            json=payload
        )

        assert (
            context.resp.status_code
            == status.HTTP_201_CREATED
        )
