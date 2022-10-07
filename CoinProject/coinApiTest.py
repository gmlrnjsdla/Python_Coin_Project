import requests

url = "https://api.upbit.com/v1/ticker"

ticker = 'KRW-BTC'
param = {'markets': ticker}
response = requests.get(url, params=param)
# print(response.text)

ubbitResult = response.json()

print(ticker[4:7])
print(ubbitResult[0]['signed_change_rate'])    # 변화율
print(ubbitResult[0]['trade_price'])    # 코인의 현재가격
print(ubbitResult[0]['acc_trade_volume_24h'])    # 24시간 누적 거래량
print(ubbitResult[0]['acc_trade_price_24h'])    # 24시간 누적 거래 대금
print(ubbitResult[0]['trade_volume'])    # 최근 거래량
print(ubbitResult[0]['high_price'])    # 고가
print(ubbitResult[0]['low_price'])    # 저가
print(ubbitResult[0]['prev_closing_price'])    # 전일종가