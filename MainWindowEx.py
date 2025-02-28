import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow import Ui_MainWindow
from MainWindow2 import Ui_MainWindow2
from MainWindow3 import Ui_MainWindow3
from MainWindow7 import Ui_MainWindow7
from MainWindow4 import Ui_MainWindow4
from MainWindow6 import Ui_MainWindow6
from MainWindow8 import Ui_MainWindow8
from MainWindow9 import Ui_MainWindow9
from MainWindow10 import Ui_MainWindow10
from handler1 import AccountHandler
from PyQt6.QtWidgets import QTableWidgetItem
from menu import menu_items
from donhang import save_order
from MainWindowEx5 import MainWindowEx5
# Import MainWindowEx5
import json
import os
from datetime import datetime
from account import accounts


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
def get_current_timestamp():
        """Trả về thời gian hiện tại theo định dạng chuẩn ISO."""
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
class MainWindowEx6(QMainWindow, Ui_MainWindow6):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user  # Lưu thông tin người dùng đang đăng nhập

        self.pushButtonDat.clicked.connect(self.save_booking)  # Xử lý đặt bàn
        self.pushButtonTC.clicked.connect(self.go_to_mainwindow2)  # Quay về MainWindow2
        self.pushButtoDX.clicked.connect(self.logout)  # Đăng xuất

        self.load_bookings()



    def save_booking(self):
        """Lưu đặt bàn vào file `datban.json` và đảm bảo dữ liệu không bị lỗi."""
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
            datetime.strptime(date, "%Y-%m-%d")  # Định dạng YYYY-MM-DD
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Ngày đặt bàn không đúng định dạng (YYYY-MM-DD).")
            return

        file_path = "datban.json"

        # Đọc danh sách đặt bàn từ file nếu có
        if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
            bookings = []
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    bookings = json.load(file)
                    if not isinstance(bookings, list):  # Kiểm tra định dạng
                        bookings = []
            except json.JSONDecodeError:
                bookings = []

        # Tạo `reservation_id` duy nhất (dựa vào ID cuối cùng)
        if bookings:
            last_id = int(bookings[-1]["reservation_id"][3:])  # Lấy số từ "RES001"
            new_reservation_id = f"RES{last_id + 1:03d}"
        else:
            new_reservation_id = "RES001"

        # Thêm đặt bàn mới
        booking_data = {
            "reservation_id": new_reservation_id,
            "phone": self.user.phone_number,
            "date": date,
            "guest_count": guest_count,
            "decoration": decoration,
            "status": "Pending",  # Trạng thái mặc định
            "table_number": None,  # Chưa có số bàn
            "deposit_amount": 0,  # Đặt cọc ban đầu là 0
            "created_at": get_current_timestamp(),
            "updated_at": get_current_timestamp()
        }

        bookings.append(booking_data)

        # Ghi dữ liệu cập nhật vào file
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(bookings, file, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Thành công", "Đặt bàn thành công!")
            print(f"Đặt bàn thành công: {booking_data}")  # Log đặt bàn thành công
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi lưu đặt bàn: {e}")
            print(f"Lỗi khi lưu đặt bàn: {e}")  # Log lỗi

        self.load_bookings()  # Cập nhật giao diện

    def load_bookings(self):
        try:
            with open("datban.json", "r", encoding="utf-8") as file:
                bookings = json.load(file)
                filtered_bookings = [b for b in bookings if b["phone"] == self.user.phone_number]
        except (FileNotFoundError, json.JSONDecodeError):
            filtered_bookings = []

        self.tableWidget.setRowCount(len(filtered_bookings))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Ngày", "Số khách", "Trang trí", "Số bàn"])

        for row, booking in enumerate(filtered_bookings):
            table_number = booking.get("table_number", "Pending")  # Nếu chưa có số bàn, hiển thị Pending
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
        self.setupUi(self)  # Đảm bảo giao diện được thiết lập
        self.user = user  # Lưu thông tin người dùng

        # Gán sự kiện cho các nút
        #self.pushButtonKH.clicked.connect(self.go_to_mainwindow8)  # Chuyển đến giao diện đặt bàn
        self.pushButtonDB.clicked.connect(self.go_to_mainwindow8)  # Chuyển đến giao diện khách hàng
        self.pushButton_4.clicked.connect(self.logout)  # Đăng xuất
        self.pushButtonDH.clicked.connect(self.go_to_mainwindow9)
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
        self.user = user  # Lưu thông tin người dùng đang đăng nhập

        # Kết nối nút với chức năng
        self.pushButtonDX.clicked.connect(self.logout)  # Đăng xuất
        self.pushButtonTC.clicked.connect(self.go_to_mainwindow7)  # Quay về quản lý
        self.pushButtonXN1.clicked.connect(self.confirm_reservation)  # Xác nhận đặt bàn
        self.pushButtonXN2.clicked.connect(self.confirm_guest_arrival)  # Xác nhận khách đến

        self.load_reservations()  # Tải dữ liệu lên bảng

    def load_reservations(self):
        """Tải danh sách đặt bàn từ datban.json và hiển thị trên tableWidget."""
        try:
            with open("datban.json", "r", encoding="utf-8") as file:
                reservations = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            reservations = []

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
        """Admin xác nhận đặt bàn, cập nhật số bàn vào datban.json."""
        res_id = self.lineEditID1.text().strip()
        table_number = self.lineEditSoban.text().strip()

        if not res_id or not table_number:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID đặt bàn và số bàn.")
            return

        try:
            with open("datban.json", "r", encoding="utf-8") as file:
                reservations = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            reservations = []

        for res in reservations:
            if res["reservation_id"] == res_id:
                res["table_number"] = table_number
                res["status"] = "Confirmed"
                break
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy ID đặt bàn!")
            return

        with open("datban.json", "w", encoding="utf-8") as file:
            json.dump(reservations, file, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Thành công", "Đã xác nhận đặt bàn thành công!")
        self.load_reservations()  # Cập nhật giao diện

    def confirm_guest_arrival(self):
        """Admin xác nhận khách đã đến, cập nhật trạng thái thành 'Arrived'."""
        res_id = self.lineEditID2.text().strip()

        if not res_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID đặt bàn.")
            return

        try:
            with open("datban.json", "r", encoding="utf-8") as file:
                reservations = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            reservations = []

        for res in reservations:
            if res["reservation_id"] == res_id:
                res["status"] = "Arrived"
                break
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy ID đặt bàn!")
            return

        with open("datban.json", "w", encoding="utf-8") as file:
            json.dump(reservations, file, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Thành công", "Đã xác nhận khách đến!")
        self.load_reservations()  # Cập nhật giao diện

    def go_to_mainwindow7(self):
        """Quay về giao diện quản lý."""
        self.main_window7 = MainWindowEx7(self.user)
        self.main_window7.show()
        self.close()

    def logout(self):
        """Đăng xuất về màn hình chính."""
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()

class MainWindowEx9(QMainWindow, Ui_MainWindow9):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user  # Lưu thông tin người dùng đang đăng nhập

        # Kết nối nút với chức năng
        self.pushButtonDX.clicked.connect(self.logout)  # Đăng xuất
        self.pushButtonTC.clicked.connect(self.go_to_mainwindow7)  # Quay về quản lý
        self.pushButtonXN1.clicked.connect(self.cancel_order)  # Hủy đơn hàng
        self.pushButtonXN2.clicked.connect(self.confirm_delivery)  # Xác nhận giao hàng

        self.load_orders()  # Tải dữ liệu lên bảng

    def load_orders(self):
        """Tải danh sách đơn hàng từ donhang.json và hiển thị trên tableWidget."""
        try:
            with open("donhang.json", "r", encoding="utf-8") as file:
                orders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            orders = []

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
        """Admin hủy đơn hàng, cập nhật trạng thái thành 'Cancelled' và lưu lý do vào donhang.json."""
        order_id = self.lineEditID1.text().strip()
        reason = self.lineEditSoban.text().strip()

        if not order_id or not reason:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID đơn hàng và lý do hủy.")
            return

        try:
            with open("donhang.json", "r", encoding="utf-8") as file:
                orders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            orders = []

        for order in orders:
            if order["order_id"] == order_id:
                order["status"] = "Cancelled"
                order["cancel_reason"] = reason
                break
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy ID đơn hàng!")
            return

        with open("donhang.json", "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Thành công", "Đã hủy đơn hàng thành công!")
        self.load_orders()  # Cập nhật giao diện

    def confirm_delivery(self):
        """Admin xác nhận giao hàng, cập nhật trạng thái thành 'Delivered' trong donhang.json."""
        order_id = self.lineEditID2.text().strip()

        if not order_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID đơn hàng.")
            return

        try:
            with open("donhang.json", "r", encoding="utf-8") as file:
                orders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            orders = []

        for order in orders:
            if order["order_id"] == order_id:
                order["status"] = "Delivered"
                break
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy ID đơn hàng!")
            return

        with open("donhang.json", "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Thành công", "Đã xác nhận giao hàng thành công!")
        self.load_orders()  # Cập nhật giao diện

    def go_to_mainwindow7(self):
        """Quay về giao diện quản lý."""
        self.main_window7 = MainWindowEx7(self.user)
        self.main_window7.show()
        self.close()

    def logout(self):
        """Đăng xuất về màn hình chính."""
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()
class MainWindowEx10(QMainWindow, Ui_MainWindow10):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)  # Thiết lập giao diện
        self.user = user  # Lưu thông tin người dùng

        # Kết nối các nút với chức năng
        self.pushButtonThem.clicked.connect(self.add_money)  # Nút thêm tiền
        self.pushButton_2.clicked.connect(self.delete_account)  # Nút xóa tài khoản

        self.load_customers()  # Gọi hàm tải danh sách khách hàng

    def load_customers(self):
        """Load danh sách khách hàng từ `account.json` vào `tableWidget`."""
        try:
            with open("account.json", "r", encoding="utf-8") as file:
                accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            accounts = {}

        # Lọc danh sách khách hàng
        customers = [
            acc for acc in accounts.values()
            if acc.get("role") == "customer" and "customer_id" in acc  # Tránh KeyError
        ]

        # Định số lượng hàng và cột trong tableWidget
        self.tableWidget.setRowCount(len(customers))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID KH", "Họ và tên", "SĐT", "Email", "Số tiền"])

        for row, customer in enumerate(customers):
            full_name = f"{customer.get('first_name', 'N/A')} {customer.get('last_name', 'N/A')}".strip()
            customer_id = customer.get("customer_id", "N/A")  # Nếu thiếu, đặt "N/A"
            phone = customer.get("phone", "N/A")
            email = customer.get("email", "N/A")
            money = str(customer.get("money", 0.0))  # Nếu thiếu, mặc định là 0.0

            self.tableWidget.setItem(row, 0, QTableWidgetItem(customer_id))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(full_name))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(phone))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(email))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(money))

    def add_money(self):
        """Thêm tiền vào tài khoản khách hàng và lưu vào `account.json`."""
        customer_id = self.lineEditID.text().strip()
        amount = self.lineEditST.text().strip()

        if not customer_id or not amount.isdigit():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID khách hàng và số tiền hợp lệ!")
            return

        amount = float(amount)

        # Đọc file account.json
        try:
            with open("account.json", "r", encoding="utf-8") as file:
                accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            accounts = {}

        # Tìm khách hàng theo ID và cập nhật số tiền
        for acc in accounts.values():
            if acc.get("customer_id") == customer_id:
                acc["money"] = acc.get("money", 0.0) + amount
                break
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy khách hàng!")
            return

        # Lưu lại dữ liệu vào file account.json
        self.save_accounts(accounts)

        QMessageBox.information(self, "Thành công", f"Đã thêm {amount} VND vào tài khoản {customer_id}!")
        self.load_customers()  # Cập nhật lại danh sách khách hàng

    def delete_account(self):
        """Xóa tài khoản khách hàng và cập nhật `account.json`."""
        customer_id = self.lineEditID2.text().strip()

        if not customer_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID khách hàng cần xóa!")
            return

        # Đọc file account.json
        try:
            with open("account.json", "r", encoding="utf-8") as file:
                accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            accounts = {}

        # Xóa khách hàng khỏi danh sách
        for user_id in list(accounts.keys()):
            if accounts[user_id].get("customer_id") == customer_id:
                del accounts[user_id]
                break
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy khách hàng!")
            return

        # Lưu lại dữ liệu vào file account.json
        self.save_accounts(accounts)

        QMessageBox.information(self, "Thành công", f"Đã xóa tài khoản khách hàng {customer_id}!")
        self.load_customers()  # Cập nhật lại danh sách khách hàng

    def save_accounts(self, accounts):
        """Lưu danh sách tài khoản vào file `account.json`."""
        with open("account.json", "w", encoding="utf-8") as file:
            json.dump(accounts, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx1()
    window.show()
    sys.exit(app.exec())
