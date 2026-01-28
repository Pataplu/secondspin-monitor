import json
import requests
from bs4 import BeautifulSoup

import time
from pathlib import Path

LOCK_FILE = Path("last_run.txt")
MIN_INTERVAL = 15 * 60  # 15 minuten

now = int(time.time())

if LOCK_FILE.exists():
    last = int(LOCK_FILE.read_text().strip())
    if now - last < MIN_INTERVAL:
        print("⏭️ Skip: run was less than 15 minutes ago")
        exit(0)

LOCK_FILE.write_text(str(now))

URL = "https://www.secondspin.nl/shop/nieuw-binnen"
STATE_FILE = "state.json"
# cron wake-up

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def extract_title(soup):
    # Probeer meerdere opties, in volgorde van betrouwbaarheid
    candidates = []

    h1 = soup.select_one("h1.page-title")
    if h1:
        candidates.append(h1.get_text(strip=True))

    h1_any = soup.find("h1")
    if h1_any:
        candidates.append(h1_any.get_text(strip=True))

    # Fallback: zoek tekst die met "Nieuw Binnen" begint
    for text in soup.stripped_strings:
        if text.lower().startswith("nieuw binnen"):
            candidates.append(text)
            break

    return candidates[0] if candidates else "UNKNOWN"

def extract_results(soup):
    for text in soup.stripped_strings:
        if "resultaten" in text.lower():
            return text
    return "UNKNOWN"

def run():
    response = requests.get(URL, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = extract_title(soup)
    results = extract_results(soup)

    current = {
        "title": title,
        "results": results
    }

    previous = load_state()

    print("Huidig:", current)
    print("Vorig:", previous)

    changed = False

    if previous:
        if current["title"] != previous.get("title"):
            print("🔔 Titel gewijzigd")
            changed = True

        if current["results"] != previous.get("results"):
            print("🔔 Aantal resultaten gewijzigd")
            changed = True
    else:
        # Eerste run
        changed = True

    if changed:
        print("🚨 WIJZIGING GEDETECTEERD")
    else:
        print("Geen wijziging")

    save_state(current)

if __name__ == "__main__":
    run()
