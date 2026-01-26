import requests
from bs4 import BeautifulSoup

URL = "https://www.secondspin.nl/shop/nieuw-binnen"

def run():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    albums = soup.select(".product-item")
    print(f"Aantal albums gevonden: {len(albums)}")

run()
