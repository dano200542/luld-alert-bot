import os
import time
import requests
from flask import Flask

app = Flask(__name__)

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

@app.route("/")
def home():
    return "OK"

def send_discord():
    print("TRYING DISCORD")

    if not WEBHOOK_URL:
        print("NO WEBHOOK SET")
        return

    r = requests.post(WEBHOOK_URL, json={"content": "🧪 BOT IS RUNNING ON RENDER"})
    print("STATUS:", r.status_code)

def run():
    print("STARTED PYTHON FILE")
    time.sleep(5)
    send_discord()

    while True:
        print("LOOP RUNNING")
        time.sleep(30)

if __name__ == "__main__":
    run()
