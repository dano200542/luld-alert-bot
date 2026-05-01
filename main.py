import requests

API_KEY = "GCAqzGwvpveABEjg92lZszGhAtbGJVYp"
WEBHOOK = "https://discord.com/api/webhooks/1463521320582250498/Oi0KYpKQzUVYLnRIKGSToqnrkfEd1A-BIPnDz5bmW7gsi5T46CrTzO7u2Eu1AuK1IoLA"

SYMBOLS = ["AAPL", "TSLA", "NVDA"]

def send(msg):
    requests.post(WEBHOOK, json={"content": msg})

for symbol in SYMBOLS:
    url = f"https://api.massive.com/v1/quote/{symbol}?apikey={API_KEY}"

    try:
        r = requests.get(url, timeout=10).json()

        change = r.get("changePercent", 0)
        status = r.get("status", "")

        if abs(change) >= 5:
            send(f"🚨 MOVE ALERT: {symbol} {change:.2f}%")

        if status == "halted":
            send(f"⛔ HALT ALERT: {symbol}")

    except Exception as e:
        print("error:", e)
