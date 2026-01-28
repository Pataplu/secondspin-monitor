import json
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path
import os
import smtplib
from email.mime.text import MIMEText

STATE_FILE = Path("state.json")
LOCK_FILE = Path("last_run.txt")
MIN_INTERVAL = 15 * 60
now = int(time.time())

# 15-min guard
if LOCK_FILE.exists():
    last = int(LOCK_FILE.read_text())
    if now - last < MIN_INTERVAL:
        exit(0)

LOCK_FILE.write_text(str(now))

URL = "https://www.secondspin.nl/shop/nieuw-binnen"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def extract_title(soup):
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    return None  # <-- GEEN UNKNOWN MEER

def extract_results(soup):
    for t in soup.stripped_strings:
        if "resultaten" in t.lower():
            return t
    return None

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

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(os.environ["EMAIL_FROM"], os.environ["EMAIL_PASSWORD"])
        s.send_message(msg)

def run():
    html = requests.get(URL, headers=HEADERS, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")

    current = {
        "title": extract_title(soup),
        "results": extract_results(soup),
    }

    previous = load_state()

    # ❗ alleen mailen bij échte wijziging
    if current != previous:
        send_mail(current, previous)
        save_state(current)
    else:
        save_state(current)

if __name__ == "__main__":
    run()
