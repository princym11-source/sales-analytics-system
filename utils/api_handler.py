import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print(f"Successfully fetched {len(products)} products from API")
        return products

    except Exception as e:
        print("Failed to fetch products from API")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product information
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        if product_id is None:
            continue

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping
