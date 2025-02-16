import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow3 import Ui_MainWindow3
from handler1 import AccountHandler
from PyQt6.QtWidgets import QTableWidgetItem

import json
class MainWindowEx7(QMainWindow, Ui_MainWindow7):
    pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx7()
    window.show()
    sys.exit(app.exec())
