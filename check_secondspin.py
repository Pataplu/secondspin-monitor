import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.message import EmailMessage

URL = "https://www.secondspin.nl/shop/nieuw-binnen"
DATA_FILE = "previous_products.json"

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

def send_email(new_items):
    msg = EmailMessage()
    msg["Subject"] = "🔥 Nieuwe platen bij Second Spin"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    body = "Er zijn nieuwe platen binnengekomen:\n\n"
    for item in new_items:
        body += f"- {item['title']}\n  {item['link']}\n\n"

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
        smtp.send_message(msg)

def get_products():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    products = []
    for product in soup.select("li.product"):
        title = product.select_one("h2")
        link = product.select_one("a")
        if title and link:
            products.append({
                "title": title.text.strip(),
                "link": link["href"]
            })
    return products

def main():
    current = get_products()

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            previous = json.load(f)
    else:
        previous = []

    previous_links = {p["link"] for p in previous}
    new_items = [p for p in current if p["link"] not in previous_links]

    if new_items:
        send_email(new_items)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
