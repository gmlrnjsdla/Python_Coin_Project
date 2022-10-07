import time
import requests
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

form_class = uic.loadUiType('../ui/UpbitCoinTrade.ui')[0]

# 시그널 클래스(쓰레드)
class CoinViewThread(QThread):
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)

    def __init__(self):
        super().__init__()
        self.ticker = 'BTC'
        self.alive = True

    def run(self):
        while self.alive:
            url = "https://api.upbit.com/v1/ticker"
            ticker = 'KRW-BTC'
            param = {'markets': ticker}
            response = requests.get(url, params=param)
            ubbitResult = response.json()
            trade_price = ubbitResult[0]['trade_price']  # 코인의 현재가격
            acc_trade_volume_24h = ubbitResult[0]['acc_trade_volume_24h']  # 24시간 누적 거래량
            acc_trade_price_24h = ubbitResult[0]['acc_trade_price_24h']  # 24시간 누적 거래 대금
            trade_volume = ubbitResult[0]['trade_volume']  # 최근 거래량
            high_price = ubbitResult[0]['high_price']  # 고가
            low_price = ubbitResult[0]['low_price']  # 저가
            prev_closing_price = ubbitResult[0]['prev_closing_price']     # 전일 종가
            signed_change_rate = ubbitResult[0]['signed_change_rate']     # 변화율

            self.coinDataSent.emit(float(trade_price),
                                   float(acc_trade_volume_24h),
                                   float(acc_trade_price_24h),
                                   float(trade_volume),
                                   float(high_price),
                                   float(low_price),
                                   float(prev_closing_price),
                                   float(signed_change_rate))

            time.sleep(1)     # 서버에 요청하는 delay Time

    def close(self):    # run 함수 while문 정지
        self.alive = False


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('UPBIT COIN TRADE')
        self.setWindowIcon(QIcon('../icons/upbit.png'))
        self.statusBar().showMessage('UPBIT COIN TRADE VER 0.5')
        self.ticker = "BTC"

        self.cvt = CoinViewThread()
        # 코인정보를 가져오는 쓰레드 클래스를 멤버객체(변수)로 선언
        self.cvt.coinDataSent.connect(self.fillcoinData)
        # 쓰레드 클래스의 시그널 함수에서 보내온 데이터를 슬롯함수와 연결
        self.cvt.start()
        # 쓰레드 클래스의 run함수가 자동으로 호출(run 함수 시작)

    def fillcoinData(self, trade_price, acc_trade_volume_24h, acc_trade_price_24h, trade_volume
                     , high_price, low_price, prev_closing_price, signed_change_rate):
        self.coin_price_label.setText(f"{trade_price:,.0f} 원")                  # 코인 현재 가격 출력
        self.acc_trade_volume_label.setText(f"{acc_trade_volume_24h:,.2f} {self.ticker}")   # 24시간 거래량
        self.acc_trade_price_label.setText(f"{acc_trade_price_24h:,.0f} 원")     # 24시간 거래금액
        self.trade_volume_label.setText(f"{trade_volume:,.5f} {self.ticker}")               # 최근 거래량
        self.high_price_label.setText(f"{high_price:,.0f} 원")                   # 최고가
        self.low_price_label.setText(f"{low_price:,.0f} 원")                     # 최저가
        self.prev_closing_price_label.setText(f"{prev_closing_price:,.0f} 원")   # 전일종가
        self.coin_changerate_label.setText(f"{signed_change_rate*100:+.2f}%")      # 가격 변화율
        self.__updateStyle()

    def __updateStyle(self):
        if '-' in self.coin_changerate_label.text():
        # 가격 변화율 레이블의 값을 가져와서 '-'이 포함되어 있으면 참
            self.coin_changerate_label.setStyleSheet('background-color:blue;color:white;')
            self.coin_price_label.setStyleSheet('color:blue;')
        else:
            self.coin_changerate_label.setStyleSheet('background-color:red;color:white;')
            self.coin_price_label.setStyleSheet('color:red;')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
