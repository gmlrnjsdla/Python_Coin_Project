import time

import pyupbit
import requests
import sys

import telegram
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

form_class = uic.loadUiType('ui/UpbitCoinTrade.ui')[0]

# 시그널 클래스(쓰레드)
class CoinViewThread(QThread):
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)
    alarmDataSent = pyqtSignal(float)   # 알람용 코인현재가격 시그널 함수

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            url = "https://api.upbit.com/v1/ticker"
            param = {'markets': f"KRW-{self.ticker}"}
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

            self.alarmDataSent.emit(float(trade_price))

            time.sleep(0.5)     # 서버에 요청하는 delay Time

    def close(self):    # run 함수 while문 정지
        self.alive = False


class MainWindow(QMainWindow, form_class):
    def __init__(self, ticker='BTC'):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('UPBIT COIN TRADE')
        self.setWindowIcon(QIcon('../icons/upbit.png'))
        self.statusBar().showMessage('UPBIT COIN TRADE VER 1.0')
        self.ticker = ticker

        self.cvt = CoinViewThread(self.ticker)
        # 코인정보를 가져오는 쓰레드 클래스를 멤버객체(변수)로 선언
        self.cvt.coinDataSent.connect(self.fillcoinData)
        self.cvt.alarmDataSent.connect(self.fillAlarmPrice)
        # 쓰레드 클래스의 시그널 함수에서 보내온 데이터를 슬롯함수와 연결
        self.cvt.start()
        # 쓰레드 클래스의 run함수가 자동으로 호출(run 함수 시작)
        self.combobox_set()
        # 콤보박스 초기화 설정 함수 호출
        self.alarm_btn.clicked.connect(self.alarmButtonAction)

    def combobox_set(self):     # 코인리스트 콤보박스 셋팅
        ticker_list = pyupbit.get_tickers(fiat="KRW")
        coinname_list = []

        for ticker in ticker_list:
            tickers = ticker[4:10]
            tickers = tickers.strip()
            coinname_list.append(tickers)

        coinname_list.remove('BTC')
        coinname_list1 = ['BTC']
        coinname_list = sorted(coinname_list)
        coinname_list = coinname_list1 + coinname_list

        self.coin_comboBox.addItems(coinname_list)
        self.coin_comboBox.currentIndexChanged.connect(self.coin_select_comboBox)

    def coin_select_comboBox(self):
        coin_ticker = self.coin_comboBox.currentText()
        # 콤보박스에서 현재 선택된 값(ticker)을 가져와서 저장
        self.ticker = coin_ticker
        # 멤버변수인 self.ticker 의 값을 콤보박스에서 선택된 ticker값으로 변경
        self.coin_ticker_label.setText(coin_ticker)
        # 콤보박스에 선택된 ticker 값으로 코인의 이름이 변경
        self.cvt.close()
        # 현재 실행 중인 쓰레드를 정지 시킴(while 종료)
        self.cvt = CoinViewThread(coin_ticker)
        self.cvt.coinDataSent.connect(self.fillcoinData)
        self.cvt.alarmDataSent.connect(self.fillAlarmPrice)
        self.cvt.start()

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

    def alarmButtonAction(self):
        self.alarmFlag = 0
        if self.alarm_btn.text() == '알람시작':
            self.alarm_btn.setText('알람중지')
            self.alarm_btn.setStyleSheet('background-color:red;color:white;')
        else:
            self.alarm_btn.setText('알람시작')
            self.alarm_btn.setStyleSheet('background-color:rgb(246, 235, 255);color:black;')

    def fillAlarmPrice(self, trade_price):  # 텔레그램 알람 메시지 슬롯 함수
        alarmButtonText = self.alarm_btn.text() # 알람 버튼의 텍스트(알람시작 or 알람중지)
        if alarmButtonText == '알람중지':
            if self.alarm_price1.text() == '' or self.alarm_price2.text() == '':
                if self.alarmFlag == 0:
                    self.alarmFlag = 1
                    QMessageBox.warning(self, '입력오류', '알람금액을 입력해주세요')
                    self.alarm_btn.setText('알람시작')
                    self.alarm_btn.setStyleSheet('background-color:rgb(246, 235, 255);color:black;')

            else:
                if self.alarmFlag == 0:
                    alarm_price1 = float(self.alarm_price1.text())
                    alarm_price2 = float(self.alarm_price2.text())
                    if alarm_price1 <= float(trade_price):  # 매도가격
                        self.telegramBot(f"********************{self.ticker} 매도타이밍********************")
                        self.telegramBot(f"{self.ticker}의 현재가격이 {alarm_price1:,.0f}원을 초과하였습니다!!")
                        self.alarmFlag = 1
                    if alarm_price2 >= float(trade_price):  # 매수가격
                        self.telegramBot(f"********************{self.ticker} 매수타이밍********************")
                        self.telegramBot(f"{self.ticker}의 현재가격이 {alarm_price2:,.0f}원보다 낮아졌습니다!!")
                        self.alarmFlag = 1

# 텔레그램 호출함수
    def telegramBot(self, text):
        self.token = '5580478919:AAFEtLVmb7ZH1dKzMkCp4aMCI9G_Aif4pQY'
        # 사용자의 텔레그램 토큰
        self.chatID = 5400256265
        # 사용자의 chat id 입력
        self.bot = telegram.Bot(token=self.token)
        self.bot.sendMessage(chat_id=self.chatID, text=text)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
