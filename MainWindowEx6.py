import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow3 import Ui_MainWindow3
from handler1 import AccountHandler
from PyQt6.QtWidgets import QTableWidgetItem
from MainWindowEx2 import MainWindowEx2

class MainWindowEx6(QMainWindow, Ui_MainWindow3):
    pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx4()
    window.show()
    sys.exit(app.exec())
