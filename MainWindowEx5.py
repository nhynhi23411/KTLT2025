import json
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from MainWindow5 import Ui_MainWindow5  # Đảm bảo bạn có file Ui_MainWindow5.py

class MainWindowEx5(QMainWindow, Ui_MainWindow5):
    def __init__(self, user_phone):
        super().__init__()
        self.setupUi(self)
        self.user_phone = user_phone  # Lưu số điện thoại của khách hàng đang đăng nhập
        self.load_orders()
        self.pushButton.clicked.connect(self.go_to_mainwindow2)
        self.pushButton_2.clicked.connect(self.logout)

    def go_to_mainwindow2(self):
        from MainWindowEx import MainWindowEx2  # Import tại đây để tránh vòng lặp
        self.main_window2 = MainWindowEx2(self.user_phone)  # Giữ thông tin user khi quay lại
        self.main_window2.show()
        self.close()

    def logout(self):
        from MainWindowEx import MainWindowEx1  # Import tại đây để tránh vòng lặp
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()

    def load_orders(self):
        if not self.user_phone:
            QMessageBox.warning(self, "Lỗi", "Không có số điện thoại người dùng!")
            return

        try:
            with open("donhang.json", "r", encoding="utf-8") as file:
                orders = json.load(file)
                filtered_orders = [order for order in orders if order.get("phone") == self.user_phone]
                self.populate_table(filtered_orders)
        except FileNotFoundError:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy file donhang.json!")
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Lỗi", "Dữ liệu trong donhang.json không hợp lệ!")

    def populate_table(self, orders):
        self.tableWidget.setRowCount(len(orders))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Số điện thoại", "Tổng tiền", "Món ăn", "Trạng thái"])

        for row, order in enumerate(orders):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(order.get("phone", "N/A")))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(order.get("total_price", "0")))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(
                ", ".join([f"{item['name']} (x{item['quantity']})" for item in order.get("items", [])])))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(order.get("status", "Chưa xác định")))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_phone = sys.argv[1] if len(sys.argv) > 1 else None  # Nhận số điện thoại từ đối số dòng lệnh

    if not user_phone:
        QMessageBox.warning(None, "Lỗi", "Không có số điện thoại người dùng!")
        sys.exit(1)

    window = MainWindowEx5(user_phone)
    window.show()
    sys.exit(app.exec())
