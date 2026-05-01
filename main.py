import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("🔥 ROUTE HIT")
    return "OK - LIVE"

if __name__ == "__main__":
    print("🔥 APP STARTED")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
