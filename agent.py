import json
import time
import requests
import smtplib
import os
from pathlib import Path
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

STATE_FILE = Path("state.json")
LOCK_FILE = Path("last_run.txt")

URL = "https://www.secondspin.nl/shop/nieuw-binnen"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))

def extract_results(soup):
    for t in soup.stripped_strings:
        if "resultaten" in t.lower():
            return " ".join(t.split())
    return None

def extract_week_title(soup):
    h2 = soup.find("h2", class_="jw-heading-100")
    if h2:
        return h2.get_text(strip=True)
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
    now = int(time.time())
    LOCK_FILE.write_text(str(now))

    html = requests.get(URL, headers=HEADERS, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")

    current = {
        "title": extract_week_title(soup),   # 👈 handmatige titel
        "results": extract_results(soup),
        "last_run": now                      # 👈 altijd wijzigen
    }

    previous = load_state()

    # Mail bij:
    # - ander aantal resultaten
    # - OF andere titel ("Nieuw Binnen week X")
    if (
        previous.get("results") != current.get("results")
        or previous.get("title") != current.get("title")
    ):
        send_mail(current, previous)

    save_state(current)

if __name__ == "__main__":
    run()
