import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from MainWindow3 import Ui_MainWindow3
from handler1 import AccountHandler
from PyQt6.QtWidgets import QTableWidgetItem
from MainWindowEx2 import MainWindowEx2
from MainWindowEx import MainWindowEx1
from MainWindowEx2 import MainWindowEx2
from MainWindowEx3 import MainWindowEx3
from MainWindowEx5 import MainWindowEx5
from MainWindowEx4 import MainWindowEx4
from MainWindow6 import Ui_MainWindow6
import json
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
        booking_data = {
            "phone": self.user.phone_number,
            "date": self.lineEditNgay.text().strip(),
            "guest_count": self.lineEditSL.text().strip(),
            "decoration": self.lineEdit_3.text().strip()
        }

        if not booking_data["date"] or not booking_data["guest_count"].isdigit():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin đặt bàn hợp lệ.")
            return

        try:
            with open("datban.json", "r", encoding="utf-8") as file:
                bookings = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            bookings = []

        bookings.append(booking_data)
        with open("datban.json", "w", encoding="utf-8") as file:
            json.dump(bookings, file, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Thành công", "Đặt bàn thành công!")
        self.load_bookings()

    def load_bookings(self):
        try:
            with open("datban.json", "r", encoding="utf-8") as file:
                bookings = json.load(file)
                filtered_bookings = [b for b in bookings if b["phone"] == self.user.phone_number]
        except (FileNotFoundError, json.JSONDecodeError):
            filtered_bookings = []

        self.tableWidget.setRowCount(len(filtered_bookings))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Ngày", "Số khách", "Trang trí"])

        for row, booking in enumerate(filtered_bookings):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(booking["date"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(booking["guest_count"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(booking["decoration"]))

    def go_to_mainwindow2(self):
        self.main_window2 = MainWindowEx2(self.user)
        self.main_window2.show()
        self.close()

    def logout(self):
        QMessageBox.information(self, "Đăng xuất", "Bạn đã đăng xuất thành công.")
        self.main_window1 = MainWindowEx1()
        self.main_window1.show()
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx6()
    window.show()
    sys.exit(app.exec())
