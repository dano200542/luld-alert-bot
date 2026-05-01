import requests

API_KEY = "GCAqzGwvpveABEjg92lZszGhAtbGJVYp"
WEBHOOK = "https://discord.com/api/webhooks/1463521320582250498/Oi0KYpKQzUVYLnRIKGSToqnrkfEd1A-BIPnDz5bmW7gsi5T46CrTzO7u2Eu1AuK1IoLA"

def test_api():
    url = f"https://api.massive.com/v1/quote/AAPL?apikey={API_KEY}"
    
    try:
        r = requests.get(url, timeout=10)
        print("STATUS:", r.status_code)
        print("TEXT:", r.text[:300])
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    test_api()
