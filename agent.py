from playwright.sync_api import sync_playwright

URL = "https://www.secondspin.nl/shop/nieuw-binnen"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="networkidle")

        products = page.query_selector_all("a.product-item-link")
        print(f"Aantal albums gevonden: {len(products)}")

        browser.close()

run()
