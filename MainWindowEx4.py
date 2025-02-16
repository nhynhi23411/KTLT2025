import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow3 import Ui_MainWindow3
from handler1 import AccountHandler
from PyQt6.QtWidgets import QTableWidgetItem
from MainWindowEx import MainWindowEx1
from MainWindowEx2 import MainWindowEx2
from MainWindowEx3 import MainWindowEx3
from MainWindowEx5 import MainWindowEx5
from MainWindowEx6 import MainWindowEx6
from menu import menu_items
from donhang import save_order
from MainWindow4 import Ui_MainWindow4
class MainWindowEx4(QMainWindow, Ui_MainWindow4):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.selected_items = []
        self.load_menu()
        self.pushButton.clicked.connect(self.add_to_order)
        self.pushDat.clicked.connect(self.place_order)
        self.pushDat_2.clicked.connect(self.open_mainwindow5)
        self.pushButton_2.clicked.connect(self.go_to_mainwindow2)
        self.pushButton_3.clicked.connect(self.logout)

    def go_to_mainwindow2(self):
        self.main_window2 = MainWindowEx2(self.user)
        self.main_window2.show()
        self.close()

    def logout(self):
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()

    def open_mainwindow5(self):  # Mở MainWindowEx5 với số điện thoại người dùng
        self.main_window5 = MainWindowEx5(self.user.phone_number)  # Truyền số điện thoại
        self.main_window5.show()
        self.main_window5.show()
        self.close()
    def load_menu(self):
        self.tableWidget1.setRowCount(len(menu_items))
        for row, item in enumerate(menu_items):
            self.tableWidget1.setItem(row, 0, QTableWidgetItem(item["id"]))
            self.tableWidget1.setItem(row, 1, QTableWidgetItem(item["name"]))
            self.tableWidget1.setItem(row, 2, QTableWidgetItem(str(item["price"])))

    def add_to_order(self):
        item_id = self.lineEditID.text().strip()
        quantity = self.lineEditSL.text().strip()
        if not item_id or not quantity.isdigit():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID món ăn và số lượng hợp lệ.")
            return

        quantity = int(quantity)
        for item in menu_items:
            if item["id"] == item_id:
                self.selected_items.append(
                    {"id": item_id, "name": item["name"], "quantity": quantity, "price": item["price"]})
                break

        self.update_order_table()

    def update_order_table(self):
        self.tableWidget_2.setRowCount(len(self.selected_items))
        total_price = 0
        for row, item in enumerate(self.selected_items):
            self.tableWidget_2.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.tableWidget_2.setItem(row, 1, QTableWidgetItem(item["id"]))
            self.tableWidget_2.setItem(row, 2, QTableWidgetItem(item["name"]))
            self.tableWidget_2.setItem(row, 3, QTableWidgetItem(str(item["quantity"])))
            self.tableWidget_2.setItem(row, 4, QTableWidgetItem(str(item["price"])))
            total_price += item["quantity"] * item["price"]

        self.lineEditTong.setText(str(total_price))

    def place_order(self):
        order_data = {
            "phone": self.user.phone_number,
            "items": self.selected_items,
            "total_price": self.lineEditTong.text()
        }
        save_order(order_data)
        print("Đơn hàng đã đặt:", order_data)
        QMessageBox.information(self, "Đặt hàng thành công", "Đơn hàng của bạn đã được đặt!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx4()
    window.show()
    sys.exit(app.exec())
