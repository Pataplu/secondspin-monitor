from playwright.sync_api import sync_playwright

URL = "https://www.secondspin.nl/shop/nieuw-binnen"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(URL, wait_until="domcontentloaded")

        # Wacht expliciet tot er product-links in de DOM zitten
        page.wait_for_timeout(5000)

        # Print een stukje HTML om te zien wat er echt staat
        html_snippet = page.content()[:1000]
        print("HTML snippet:")
        print(html_snippet)

        # Veel bredere selector: alle links naar /shop/
        product_links = page.query_selector_all("a[href*='/shop/']")

        print(f"Aantal links naar producten gevonden: {len(product_links)}")

        browser.close()

run()
