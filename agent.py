from playwright.sync_api import sync_playwright

URL = "https://www.secondspin.nl/shop/nieuw-binnen"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        products = []

        def handle_response(response):
            url = response.url
            if "/wp-json/" in url and "products" in url:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        products.extend(data)
                except:
                    pass

        page.on("response", handle_response)

        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(5000)

        print(f"Aantal albums gevonden via netwerk: {len(products)}")

        browser.close()

run()
