import requests
import os

API_KEY = os.environ["GCAqzGwvpveABEjg92lZszGhAtbGJVYp"]
WEBHOOK = os.environ["https://discord.com/api/webhooks/1463521320582250498/Oi0KYpKQzUVYLnRIKGSToqnrkfEd1A-BIPnDz5bmW7gsi5T46CrTzO7u2Eu1AuK1IoLA"]

# Example symbols to watch (we expand later)
symbols = ["AAPL", "TSLA", "NVDA"]

def send(msg):
    requests.post(WEBHOOK, json={"content": msg})

for symbol in symbols:
    url = f"https://api.massive.com/v1/quote/{symbol}?apikey={API_KEY}"
    r = requests.get(url).json()

    price = r.get("price", 0)
    change = r.get("changePercent", 0)

    # 🚨 Spike detection (proxy for LULD)
    if abs(change) > 5:
        send(f"🚨 BIG MOVE: {symbol} {change:.2f}%")

    # 🚨 Halt detection (if API provides status field)
    if r.get("status") == "halted":
        send(f"⛔ HALT DETECTED: {symbol}")
