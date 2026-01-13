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
