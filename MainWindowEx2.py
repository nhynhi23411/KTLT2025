import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow2 import Ui_MainWindow2
from handler1 import AccountHandler
from MainWindowEx3 import MainWindowEx3

class MainWindowEx2(QMainWindow, Ui_MainWindow2):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.pushButton.clicked.connect(self.open_customer_info)

    def open_customer_info(self):
        self.main_window3 = MainWindowEx3(self.user)
        self.main_window3.show()
        self.close()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx2()
    window.show()
    sys.exit(app.exec())
