import os
import requests
from flask import Flask

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1463521320582250498/Oi0KYpKQzUVYLnRIKGSToqnrkfEd1A-BIPnDz5bmW7gsi5T46CrTzO7u2Eu1AuK1IoLA"

@app.route("/")
def home():
    print("🔥 ROUTE HIT")

    try:
        r = requests.post(
            WEBHOOK_URL,
            json={"content": "🚨 TEST ALERT FROM RENDER"},
            timeout=10
        )
        print("🔥 DISCORD STATUS:", r.status_code)
        print("🔥 DISCORD RESPONSE:", r.text)
    except Exception as e:
        print("🔥 ERROR:", e)

    return "OK - LIVE"

if __name__ == "__main__":
    print("🔥 APP STARTED")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
