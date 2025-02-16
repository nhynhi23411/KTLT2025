import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow3 import Ui_MainWindow3
from handler1 import AccountHandler
from PyQt6.QtWidgets import QTableWidgetItem
from MainWindowEx import MainWindowEx1
from MainWindowEx2 import MainWindowEx2
from MainWindowEx4 import MainWindowEx4
from MainWindowEx5 import MainWindowEx5
from MainWindowEx6 import MainWindowEx6

class MainWindowEx3(QMainWindow, Ui_MainWindow3):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user  # Lưu thông tin user
        self.display_user_info(user)
        self.pushButton.clicked.connect(self.go_to_mainwindow2)
        self.pushButton_2.clicked.connect(self.logout)

    def go_to_mainwindow2(self):
        self.main_window2 = MainWindowEx2(self.user)
        self.main_window2.show()
        self.close()

    def logout(self):
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()

    def display_user_info(self, user):
        self.tableWidget.setRowCount(6)  # Số hàng cố định
        self.tableWidget.setColumnCount(2)  # 2 cột: tiêu đề - giá trị
        self.tableWidget.setHorizontalHeaderLabels(["Thông tin", "Giá trị"])

        user_data = [
            ("Mã số KH", user.user_id),
            ("Tên", user.get_full_name()),
            ("Email", user.email),
            ("Số điện thoại", user.phone_number),
            ("Địa chỉ", user.address),
            ("Tiền trong tài khoản", f"{user.money} VND")
        ]

        for row, (label, value) in enumerate(user_data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(label))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(value))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx3()
    window.show()
    sys.exit(app.exec())
