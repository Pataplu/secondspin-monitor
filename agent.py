import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.secondspin.nl/shop/nieuw-binnen"
STATE_FILE = "state.json"

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def run():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    soup = BeautifulSoup(response.text, "html.parser")

    # 1️⃣ Titel: "Nieuw Binnen week X"
    title = soup.find("h1")
    title_text = title.get_text(strip=True) if title else "UNKNOWN"

    # 2️⃣ Aantal resultaten: "24 resultaten"
    results_text = soup.find(string=lambda t: "resultaten" in t.lower())
    results_text = results_text.strip() if results_text else "UNKNOWN"

    current = {
        "title": title_text,
        "results": results_text
    }

    previous = load_state()

    print("Huidig:", current)
    print("Vorig:", previous)

    if current != previous:
        print("🔔 WIJZIGING GEDETECTEERD")
        # HIER komt straks e-mail
    else:
        print("Geen wijziging")

    save_state(current)

run()
