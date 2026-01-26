import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.secondspin.nl/shop/nieuw-binnen"

def run():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    # WooCommerce zet productdata in JSON scripts
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") == "ItemList":
                for item in data.get("itemListElement", []):
                    products.append(item["item"]["name"])
        except Exception:
            pass

    print(f"Aantal albums gevonden: {len(products)}")

run()
