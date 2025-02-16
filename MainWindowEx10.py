import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from MainWindow10 import Ui_MainWindow10
import json
class MainWindowEx10(QMainWindow, Ui_MainWindow10):

    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx10()
    window.show()
    sys.exit(app.exec())
