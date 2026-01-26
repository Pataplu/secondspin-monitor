import requests
from bs4 import BeautifulSoup

URL = "https://www.secondspin.nl/shop/nieuw-binnen"

def run():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Zoek alle links naar producten
    product_links = soup.select("a[href*='/shop/']")

    # Uniek maken (zelfde album kan meerdere links hebben)
    unique_products = set(link["href"] for link in product_links)

    print(f"Aantal albums gevonden: {len(unique_products)}")

run()
