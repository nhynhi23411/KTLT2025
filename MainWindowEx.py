import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow import Ui_MainWindow
from MainWindow2 import Ui_MainWindow2
from MainWindow3 import Ui_MainWindow3
from MainWindow4 import Ui_MainWindow4
from handler1 import AccountHandler
from PyQt6.QtWidgets import QTableWidgetItem
from menu import menu_items
from donhang import save_order

class MainWindowEx1(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.account_handler = AccountHandler()
        self.pushLogin.clicked.connect(self.handle_login)

    def handle_login(self):
        phone = self.lineEditSDT.text().strip()
        password = self.lineEditPW.text().strip()

        success, user, next_window = self.account_handler.verify_login(phone, password)
        if success:
            QMessageBox.information(self, "Đăng nhập thành công", f"Chào mừng {user.get_full_name()}!")
            self.open_next_window(next_window, user)
        else:
            QMessageBox.warning(self, "Đăng nhập thất bại", "Số điện thoại hoặc mật khẩu không đúng!")

    def open_next_window(self, window_name, user):
        if window_name == "mainwindow2":
            self.main_window = MainWindowEx2(user)
        elif window_name == "mainwindow8":
            pass
            #self.main_window = QMainWindow()
            #self.ui_main_window = Ui_MainWindow8()
            #self.ui_main_window.setupUi(self.main_window)
        else:
            return

        self.main_window.show()
        self.close()


class MainWindowEx2(QMainWindow, Ui_MainWindow2):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.pushButton.clicked.connect(self.open_customer_info)
        self.pushButton_2.clicked.connect(self.open_menu_list)

    def open_customer_info(self):
        self.main_window3 = MainWindowEx3(self.user)
        self.main_window3.show()
        self.close()

    def open_menu_list(self):
        self.main_window4 = MainWindowEx4(self.user)
        self.main_window4.show()
        self.close()


class MainWindowEx4(QMainWindow, Ui_MainWindow4):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.selected_items = []
        self.load_menu()
        self.pushButton.clicked.connect(self.add_to_order)
        self.pushDat.clicked.connect(self.place_order)

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
class MainWindowEx3(QMainWindow, Ui_MainWindow3):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.display_user_info(user)

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
    window = MainWindowEx1()
    window.show()
    sys.exit(app.exec())
