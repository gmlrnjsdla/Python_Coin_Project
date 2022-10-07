import pyupbit

# 업비트 거래 코인 티커 조회
upbit_ticker = pyupbit.get_tickers()

# 해당 코인의 현재 가격 조회
coin_price = pyupbit.get_current_price(['KRW-BTC', 'KRW-XRP'])
print(coin_price)

# 해당 코인의 과거 데이터 조회
df = pyupbit.get_ohlcv("KRW-BTC")
print(df)

# 해당 코인의 호가 조회
orderbook = pyupbit.get_orderbook('KRW-XRP')
print(orderbook[0]['orderbook_units'])


