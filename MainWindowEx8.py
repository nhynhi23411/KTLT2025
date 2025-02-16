import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow3 import Ui_MainWindow3
from handler1 import AccountHandler
from PyQt6.QtWidgets import QTableWidgetItem
from MainWindowEx2 import MainWindowEx2
from MainWindowEx import MainWindowEx1
from MainWindowEx2 import MainWindowEx2
from MainWindowEx3 import MainWindowEx3
from MainWindowEx5 import MainWindowEx5
from MainWindowEx4 import MainWindowEx4
from MainWindow8 import Ui_MainWindow8
import json
class MainWindowEx8(QMainWindow, Ui_MainWindow8):

    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx8()
    window.show()
    sys.exit(app.exec())
