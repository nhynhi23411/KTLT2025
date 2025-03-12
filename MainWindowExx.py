import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from MainWindow import Ui_MainWindow
from MainWindow2 import Ui_MainWindow2
from MainWindow3 import Ui_MainWindow3
from MainWindow7 import Ui_MainWindow7
from MainWindow4 import Ui_MainWindow4
from MainWindow6 import Ui_MainWindow6
from MainWindow8 import Ui_MainWindow8
from MainWindow9 import Ui_MainWindow9
from MainWindow10 import Ui_MainWindow10
from MainWindow11 import Ui_MainWindow11
from MainWindowEx5 import MainWindowEx5
from handlers import (
    AccountHandler,
    OrderHandler,
    ReservationHandler,
    MenuHandler
)
from handler1 import AccountHandler
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
        elif window_name == "mainwindow7":
            self.main_window = MainWindowEx7(user)
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

    def open_mainwindow5(self):
        self.main_window5 = MainWindowEx5(self.user.phone_number)
        self.main_window5.show()
        self.close()

    def open_mainwindow6(self):
        print("Mở MainWindowEx6...")  # Debug
        self.main_window6 = MainWindowEx6(self.user)
        self.main_window6.show()
        self.close()


class MainWindowEx4(QMainWindow, Ui_MainWindow4):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.selected_items = []
        self.menu_handler = MenuHandler()
        self.order_handler = OrderHandler()

        # Load menu and connect buttons
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

    def open_mainwindow5(self):
        self.main_window5 = MainWindowEx5(self.user.phone_number)
        self.main_window5.show()
        self.close()

    def load_menu(self):
        menu_items = self.menu_handler.load_menu()
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
        menu_items = self.menu_handler.load_menu()
        for item in menu_items:
            if item["id"] == item_id:
                self.selected_items.append({
                    "id": item_id,
                    "name": item["name"],
                    "quantity": quantity,
                    "price": item["price"]
                })
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
        if not self.selected_items:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ít nhất một món ăn.")
            return

        order_data = {
            "phone": self.user.phone_number,
            "items": self.selected_items,
            "total_price": self.lineEditTong.text()
        }

        order_id = self.order_handler.place_order(order_data)
        QMessageBox.information(self, "Đặt hàng thành công", f"Đơn hàng #{order_id} của bạn đã được đặt!")
        # Reset selected items
        self.selected_items = []
        self.update_order_table()


class MainWindowEx3(QMainWindow, Ui_MainWindow3):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
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
        self.tableWidget.setRowCount(6)
        self.tableWidget.setColumnCount(2)
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


class MainWindowEx6(QMainWindow, Ui_MainWindow6):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.reservation_handler = ReservationHandler()

        self.pushButtonDat.clicked.connect(self.save_booking)
        self.pushButtonTC.clicked.connect(self.go_to_mainwindow2)
        self.pushButtoDX.clicked.connect(self.logout)

        self.load_bookings()

    def save_booking(self):
        date = self.lineEditNgay.text().strip()
        guest_count = self.lineEditSL.text().strip()
        decoration = self.lineEdit_3.text().strip()

        if not date or not guest_count.isdigit():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin đặt bàn hợp lệ.")
            return

        guest_count = int(guest_count)

        if guest_count <= 0:
            QMessageBox.warning(self, "Lỗi", "Số khách phải lớn hơn 0.")
            return

        # Kiểm tra định dạng ngày
        try:
            from datetime import datetime
            datetime.strptime(date, "%Y-%m-%d")  # Định dạng YYYY-MM-DD
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Ngày đặt bàn không đúng định dạng (YYYY-MM-DD).")
            return

        reservation_id = self.reservation_handler.create_reservation(
            self.user.phone_number, date, guest_count, decoration
        )

        QMessageBox.information(self, "Thành công", f"Đặt bàn thành công với mã #{reservation_id}!")
        self.load_bookings()

    def load_bookings(self):
        reservations = self.reservation_handler.get_user_reservations(self.user.phone_number)

        self.tableWidget.setRowCount(len(reservations))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Ngày", "Số khách", "Trang trí", "Số bàn"])

        for row, booking in enumerate(reservations):
            table_number = booking.get("table_number", "Pending")
            self.tableWidget.setItem(row, 0, QTableWidgetItem(booking["date"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(booking["guest_count"])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(booking["decoration"]))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(table_number)))

    def go_to_mainwindow2(self):
        self.main_window2 = MainWindowEx2(self.user)
        self.main_window2.show()
        self.close()

    def logout(self):
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()


class MainWindowEx7(QMainWindow, Ui_MainWindow7):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user

        self.pushButtonDB.clicked.connect(self.go_to_mainwindow8)
        self.pushButton_4.clicked.connect(self.logout)
        self.pushButtonDH.clicked.connect(self.go_to_mainwindow9)
        self.pushButtonKH.clicked.connect(self.go_to_mainwindow10)

    def go_to_mainwindow8(self):
        self.main_window8 = MainWindowEx8(self.user)
        self.main_window8.show()
        self.close()

    def go_to_mainwindow9(self):
        self.main_window9 = MainWindowEx9(self.user)
        self.main_window9.show()
        self.close()

    def go_to_mainwindow10(self):
        self.main_window10 = MainWindowEx10(self.user)
        self.main_window10.show()
        self.close()

    def logout(self):
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()


class MainWindowEx8(QMainWindow, Ui_MainWindow8):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.reservation_handler = ReservationHandler()

        self.pushButtonDX.clicked.connect(self.logout)
        self.pushButtonTC.clicked.connect(self.go_to_mainwindow7)
        self.pushButtonXN1.clicked.connect(self.confirm_reservation)
        self.pushButtonXN2.clicked.connect(self.confirm_guest_arrival)
        self.pushButtonHuy.clicked.connect(self.cancel_reservation)

        self.load_reservations()

    def load_reservations(self):
        reservations = self.reservation_handler.load_reservations()

        self.tableWidget.setRowCount(len(reservations))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Ngày", "Số khách", "Số bàn", "Trạng thái"])

        for row, res in enumerate(reservations):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(res["reservation_id"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(res["date"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(res["guest_count"])))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(res.get("table_number", "Pending"))))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(res.get("status", "Pending")))

    def confirm_reservation(self):
        res_id = self.lineEditID1.text().strip()
        table_number = self.lineEditSoban.text().strip()

        if not res_id or not table_number:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID đặt bàn và số bàn.")
            return

        success = self.reservation_handler.update_reservation_status(
            res_id, "Confirmed", table_number
        )

        if success:
            QMessageBox.information(self, "Thành công", "Đã xác nhận đặt bàn thành công!")
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy ID đặt bàn!")

        self.load_reservations()

    def confirm_guest_arrival(self):
        res_id = self.lineEditID2.text().strip()

        if not res_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID đặt bàn.")
            return

        success = self.reservation_handler.update_reservation_status(res_id, "Arrived")

        if success:
            QMessageBox.information(self, "Thành công", "Đã xác nhận khách đến!")
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy ID đặt bàn!")

        self.load_reservations()

    def cancel_reservation(self):
        res_id = self.lineEditID1.text().strip()

        if not res_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID đặt bàn.")
            return

        success = self.reservation_handler.update_reservation_status(res_id, "Cancelled")

        if success:
            QMessageBox.information(self, "Thành công", "Đã xác nhận đặt bàn bị hủy!")
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy ID đặt bàn!")

        self.load_reservations()

    def go_to_mainwindow7(self):
        self.main_window7 = MainWindowEx7(self.user)
        self.main_window7.show()
        self.close()

    def logout(self):
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()
class MainWindowEx9(QMainWindow, Ui_MainWindow9):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user

        self.pushButtonDX.clicked.connect(self.logout)
        self.pushButtonTC.clicked.connect(self.go_to_mainwindow7)
        self.pushButtonXN1.clicked.connect(self.cancel_order)
        self.pushButtonXN2.clicked.connect(self.confirm_delivery)

        self.load_orders()

    def load_orders(self):
        orders = OrderHandler.load_orders()
        self.tableWidget.setRowCount(len(orders))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Số điện thoại", "Tổng tiền", "Trạng thái", "Món ăn"])

        for row, order in enumerate(orders):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(order["order_id"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(order["phone"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(order["total_price"])))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(order.get("status", "Pending")))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(
                ", ".join([f"{item['name']} (x{item['quantity']})" for item in order.get("items", [])])
            ))

    def cancel_order(self):
        order_id = self.lineEditID1.text().strip()
        reason = self.lineEditSoban.text().strip()

        if not order_id or not reason:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID đơn hàng và lý do hủy.")
            return

        if OrderHandler.cancel_order(order_id, reason):
            QMessageBox.information(self, "Thành công", "Đã hủy đơn hàng thành công!")
            self.load_orders()
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy ID đơn hàng!")

    def confirm_delivery(self):
        order_id = self.lineEditID2.text().strip()

        if not order_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID đơn hàng.")
            return

        if OrderHandler.confirm_delivery(order_id):
            QMessageBox.information(self, "Thành công", "Đã xác nhận giao hàng thành công!")
            self.load_orders()
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy ID đơn hàng!")
class MainWindowEx10(QMainWindow, Ui_MainWindow10):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user

        # Kết nối các nút với chức năng tương ứng
        self.pushButtonThem.clicked.connect(self.add_money)  # Thêm tiền vào tài khoản
        self.pushButton_2.clicked.connect(self.delete_account)  # Xóa tài khoản khách hàng
        self.pushButton.clicked.connect(self.open_mainwindow11)  # Mở màn hình thêm khách hàng
        self.pushButtonThem_2.clicked.connect(self.logout)  # Đăng xuất
        self.pushButtonThem_3.clicked.connect(self.go_to_mainwindow7)  # Quay lại quản lý

        self.load_customers()

    def load_customers(self):
        """Tải danh sách khách hàng từ account.json và hiển thị lên bảng."""
        accounts = AccountHandler.load_accounts()
        customers = [acc for acc in accounts.values() if acc.get("role") == "customer"]

        self.tableWidget.setRowCount(len(customers))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID KH", "Họ và tên", "SĐT", "Email", "Số tiền"])

        for row, customer in enumerate(customers):
            full_name = f"{customer.get('first_name', 'N/A')} {customer.get('last_name', 'N/A')}".strip()
            customer_id = customer.get("customer_id", "N/A")
            phone = customer.get("phone", "N/A")
            email = customer.get("email", "N/A")
            money = str(customer.get("money", 0.0))

            self.tableWidget.setItem(row, 0, QTableWidgetItem(customer_id))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(full_name))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(phone))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(email))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(money))

    def add_money(self):
        """Thêm tiền vào tài khoản khách hàng."""
        customer_id = self.lineEditID.text().strip()
        amount = self.lineEditST.text().strip()

        if not customer_id or not amount.isdigit():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID khách hàng và số tiền hợp lệ!")
            return

        amount = float(amount)

        if AccountHandler.add_money(customer_id, amount):
            QMessageBox.information(self, "Thành công", f"Đã thêm {amount} VND vào tài khoản {customer_id}!")
            self.load_customers()  # Cập nhật lại danh sách khách hàng
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy khách hàng!")

    def delete_account(self):
        """Xóa tài khoản khách hàng."""
        customer_id = self.lineEditID2.text().strip()

        if not customer_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID khách hàng cần xóa!")
            return

        if AccountHandler.delete_account(customer_id):
            QMessageBox.information(self, "Thành công", f"Đã xóa tài khoản khách hàng {customer_id}!")
            self.load_customers()  # Cập nhật lại danh sách khách hàng
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy khách hàng!")

    def open_mainwindow11(self):
        """Mở màn hình thêm khách hàng."""
        self.main_window11 = MainWindowEx11(self.user)
        self.main_window11.show()
        self.close()

    def go_to_mainwindow7(self):
        """Quay về màn hình quản lý."""
        self.main_window7 = MainWindowEx7(self.user)
        self.main_window7.show()
        self.close()

    def logout(self):
        """Đăng xuất về màn hình chính."""
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()
class MainWindowEx11(QMainWindow, Ui_MainWindow11):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user

        self.pushButton.clicked.connect(self.save_customer_info)
        self.pushButton_2.clicked.connect(self.return_to_mainwindow10)

    def save_customer_info(self):
        """Lưu thông tin khách hàng vào account.json."""
        first_name = self.lineEdit.text().strip()
        last_name = self.lineEdit_2.text().strip()
        address = self.lineEdit_3.text().strip()
        email = self.lineEdit_4.text().strip()
        phone = self.lineEdit_5.text().strip()

        if not first_name or not last_name or not address or not email or not phone:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        if AccountHandler.add_customer(first_name, last_name, address, email, phone):
            QMessageBox.information(self, "Thành công", "Thông tin khách hàng đã được lưu!")

            # Xóa nội dung trong các ô nhập
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
        else:
            QMessageBox.warning(self, "Lỗi", "Email hoặc số điện thoại đã tồn tại!")

    def return_to_mainwindow10(self):
        """Quay lại màn hình quản lý tài khoản."""
        self.main_window10 = MainWindowEx10(self.user)
        self.main_window10.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx1()
    window.show()
    sys.exit(app.exec())
