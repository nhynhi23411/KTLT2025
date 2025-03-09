import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from MainWindow11 import Ui_MainWindow11
import json
class MainWindowEx11(QMainWindow, Ui_MainWindow11):

    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx11()
    window.show()
    sys.exit(app.exec())
