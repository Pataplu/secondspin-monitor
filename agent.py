import requests

URL = "https://www.secondspin.nl/wp-json/wc/store/products?orderby=date&order=desc"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SecondSpinAgent/1.0)"
}

def run():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()

    products = response.json()

    print(f"Aantal albums gevonden: {len(products)}")

run()
