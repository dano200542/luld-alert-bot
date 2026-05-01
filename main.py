import requests
import time

API_KEY = "GCAqzGwvpveABEjg92lZszGhAtbGJVYp"
WEBHOOK = "https://discord.com/api/webhooks/1463521320582250498/Oi0KYpKQzUVYLnRIKGSToqnrkfEd1A-BIPnDz5bmW7gsi5T46CrTzO7u2Eu1AuK1IoLA"


SYMBOLS = ["AAPL", "TSLA", "NVDA"]

def alert(msg):
    requests.post(WEBHOOK, json={"content": msg})

while True:
    print("checking market...")

    for symbol in SYMBOLS:
        url = f"https://api.massive.com/v1/quote/{symbol}?apikey={API_KEY}"
        data = requests.get(url).json()

        print(symbol, data)

    time.sleep(60)
