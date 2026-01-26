import requests

URL = "https://www.secondspin.nl/wp-json/wc/store/products?orderby=date&order=desc"

def run():
    response = requests.get(URL)
    response.raise_for_status()

    products = response.json()

    print(f"Aantal albums gevonden: {len(products)}")

run()
