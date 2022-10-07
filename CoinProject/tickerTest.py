import pyupbit

ticker_list = pyupbit.get_tickers(fiat="KRW")

# print(ticker_list)

coinname_list = []

for ticker in ticker_list:
    tickers = ticker[4:10]
    tickers = tickers.strip()
    coinname_list.append(tickers)
coinname_list.remove('BTC')
coinname_list1 =['BTC']
coinname_list = sorted(coinname_list)
coinname_list = coinname_list1 + coinname_list
print(coinname_list)
