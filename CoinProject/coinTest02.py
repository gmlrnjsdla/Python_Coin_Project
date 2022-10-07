import requests

url = "https://api.upbit.com/v1/ticker"

param = {'markets': 'KRW-BTC'}

# headers = {"accept": "application/json"}

response = requests.get(url, params=param)

print(response.text)

result = response.json()
print(result[0]['trade_price'])