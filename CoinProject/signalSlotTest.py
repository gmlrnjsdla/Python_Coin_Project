import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SignalThread(QThread):
    signal1 = pyqtSignal(int)

    def run(self):
        self.signal1.emit(100)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        sigThread = SignalThread()

        sigThread.signal1.connect(self.signal1_print)
        sigThread.run()

    @pyqtSlot(int)
    def signal1_print(self, arg1):
        print('signal1 emit 실행!!! 받은 숫자:',arg1)


app = QApplication(sys.argv)
win = MainWin()
win.show()
app.exec_()