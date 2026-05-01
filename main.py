import requests

API_KEY = "GCAqzGwvpveABEjg92lZszGhAtbGJVYp"

symbol = "AAPL"

url = f"https://api.massive.com/v1/quote/{symbol}?apikey={API_KEY}"

r = requests.get(url)

print("STATUS CODE:", r.status_code)
print("RAW RESPONSE:")
print(r.text)
