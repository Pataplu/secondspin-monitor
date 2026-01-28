import json
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path
import os
import smtplib
from email.mime.text import MIMEText

LOCK_FILE = Path("last_run.txt")
MIN_INTERVAL = 15 * 60
now = int(time.time())

if LOCK_FILE.exists():
    last = int(LOCK_FILE.read_text().strip())
    if now - last < MIN_INTERVAL:
        exit(0)

LOCK_FILE.write_text(str(now))

URL = "https://www.secondspin.nl/shop/nieuw-binnen"
STATE_FILE = "state.json"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def extract_title(soup):
    h1 = soup.select_one("h1.page-title")
    if h1:
        return h1.get_text(strip=True)
    h1_any = soup.find("h1")
    return h1_any.get_text(strip=True) if h1_any else "UNKNOWN"

def extract_results(soup):
    for text in soup.stripped_strings:
        if "resultaten" in text.lower():
            return text
    return "UNKNOWN"

def send_mail(current, previous):
    body = (
        "Wijziging gedetecteerd op SecondSpin\n\n"
        f"Vorige:\n{previous}\n\n"
        f"Huidige:\n{current}\n"
    )

    msg = MIMEText(body)
    msg["Subject"] = "SecondSpin – wijziging gedetecteerd"
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(
            os.environ["EMAIL_FROM"],
            os.environ["EMAIL_PASSWORD"]
        )
        server.send_message(msg)

def run():
    html = requests.get(URL, headers=HEADERS, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")

    current = {
        "title": extract_title(soup),
        "results": extract_results(soup)
    }

    previous = load_state()

    if current != previous:
        send_mail(current, previous)

    save_state(current)

if __name__ == "__main__":
    run()
