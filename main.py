import os
import time
import csv
import requests
from io import StringIO
import json

# Discord webhook
WEBHOOK_URL = os.environ.get("https://discord.com/api/webhooks/1463521320582250498/Oi0KYpKQzUVYLnRIKGSToqnrkfEd1A-BIPnDz5bmW7gsi5T46CrTzO7u2Eu1AuK1IoL")

URL = "https://www.nyse.com/api/trade-halts/current/download"

SEEN_FILE = "seen.json"


# -----------------------------
# Load / Save seen alerts
# -----------------------------
def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    try:
        with open(SEEN_FILE, "w") as f:
            json.dump(list(seen), f)
    except Exception as e:
        print("Failed to save seen:", e)


seen = load_seen()


# -----------------------------
# Discord sender
# -----------------------------
def send_discord(msg):
    if not WEBHOOK_URL:
        print("Missing DISCORD_WEBHOOK")
        return

    try:
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)
    except Exception as e:
        print("Discord error:", e)


# -----------------------------
# Fetch NYSE data
# -----------------------------
def fetch_data():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return r.text


# -----------------------------
# Process CSV
# -----------------------------
def process(csv_text):
    global seen

    reader = csv.DictReader(StringIO(csv_text))

    for row in reader:
        symbol = row.get("Symbol") or row.get("symbol")
        reason = (row.get("Reason") or row.get("reason") or "").upper()

        if not symbol:
            continue

        # ONLY LULD HALTS
        if "LULD" not in reason:
            continue

        key = f"{symbol}-{reason}"

        if key in seen:
            continue

        seen.add(key)
        save_seen(seen)

        send_discord(
            "🚨 NYSE LULD HALT\n"
            f"Symbol: {symbol}\n"
            f"Reason: {reason}"
        )


# -----------------------------
# Main loop
# -----------------------------
def main():
    print("LULD bot running...")

    while True:
        try:
            csv_text = fetch_data()
            process(csv_text)

        except Exception as e:
            print("Error:", e)

        time.sleep(10)  # faster polling = lower latency


if __name__ == "__main__":
    main()
