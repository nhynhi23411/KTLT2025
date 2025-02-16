import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow2 import Ui_MainWindow2
from handler1 import AccountHandler
from MainWindowEx import MainWindowEx1
from MainWindowEx3 import MainWindowEx3
from MainWindowEx4 import MainWindowEx4
from MainWindowEx5 import MainWindowEx5
from MainWindowEx6 import MainWindowEx6

class MainWindowEx2(QMainWindow, Ui_MainWindow2):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.pushButton.clicked.connect(self.open_customer_info)
        self.pushButton_2.clicked.connect(self.open_menu_list)
        self.pushButton_3.clicked.connect(self.open_mainwindow5)
        self.pushButton_4.clicked.connect(self.open_mainwindow6)
        self.pushButton_5.clicked.connect(self.logout)
    def logout(self):
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()
    def open_customer_info(self):
        self.main_window3 = MainWindowEx3(self.user)
        self.main_window3.show()
        self.close()

    def open_menu_list(self):
        self.main_window4 = MainWindowEx4(self.user)
        self.main_window4.show()
        self.close()

    def open_mainwindow5(self):  # Mở MainWindowEx5 với số điện thoại người dùng
        self.main_window5 = MainWindowEx5(self.user.phone_number)  # Truyền số điện thoại
        self.main_window5.show()
        self.close()

    def open_mainwindow6(self):  # Mở MainWindowEx5 với số điện thoại người dùng
        print("Mở MainWindowEx6...")  # Debug
        self.main_window6 = MainWindowEx6(self.user)
        self.main_window6.show()
        self.main_window6.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx2()
    window.show()
    sys.exit(app.exec())
