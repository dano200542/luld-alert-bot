print("🔥 SCRIPT IS RUNNING")

import requests

API_KEY = "TEST"

url = "https://httpbin.org/get"

r = requests.get(url)

print("STATUS CODE:", r.status_code)
print("RESPONSE OK")
