import os
import time
import requests

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

def send(msg):
    print("SENDING...")
    r = requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

print("STARTED")

time.sleep(5)

send("🧪 TEST: BOT IS WORKING")

while True:
    print("ALIVE")
    time.sleep(30)
