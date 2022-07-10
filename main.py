from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QProcess
from UI import Ui_MainWindow
from FundScraper import *
import sys

F = FundScraper()


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.p = None  # FundScraper process
        self.setup_control()

    def setup_control(self):

        self.ui.comboBox_fundList.addItem('全部')  # add items to first comboBox
        self.ui.comboBox_fundList.addItem('單筆top20')
        self.ui.comboBox_fundList.addItem('定額top20')

        self.ui.pushButton_fundList.clicked.connect(self.onFundListButtonClick)

    def onFundListButtonClick(self):
        s = self.ui.comboBox_fundList.currentText()
        if s == '全部':
            self.start_process(1)
        elif s == '單筆top20':
            self.start_process(2)
        elif s == '定額top20':
            self.start_process(3)

    def message(self, s):
        self.ui.textEdit.append(s)

    def clearMessage(self):
        self.ui.textEdit.clear()

    def start_process(self, num):
        if self.p is None:
            self.message('\nTerminal connected.\n')
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardOutput.connect(self.handle_stderr)
            self.p.finished.connect(self.process_finished)
            if num == 1:
                self.p.start("python3", ['fund_scrape_script1.py'])
            elif num == 2:
                self.p.start("python3", ['fund_scrape_script2.py'])
            elif num == 3:
                self.p.start("python3", ['fund_scrape_script3.py'])

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def process_finished(self):
        self.message("Process finished.")
        self.p = None


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec_())
