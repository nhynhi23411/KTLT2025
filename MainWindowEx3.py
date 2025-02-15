import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow3 import Ui_MainWindow3
from handler1 import AccountHandler
from PyQt6.QtWidgets import QTableWidgetItem
from MainWindowEx2 import MainWindowEx2

class MainWindowEx3(QMainWindow, Ui_MainWindow3):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.display_user_info(user)

    def display_user_info(self, user):
        user_data = [
            user.get_full_name(),
            user.phone_number,
            user.address,
            f"{user.money} VND"
        ]

        for row, value in enumerate(user_data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(value))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx3()
    window.show()
    sys.exit(app.exec())
