import json
import os
import hashlib
from datetime import datetime


class AccountHandler:
    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        """Tải danh sách tài khoản từ account.json"""
        try:
            with open("account.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_accounts(self, accounts=None):
        """Lưu danh sách tài khoản vào account.json"""
        if accounts is None:
            accounts = self.accounts
        with open("account.json", "w", encoding="utf-8") as file:
            json.dump(accounts, file, indent=4, ensure_ascii=False)

    def verify_login(self, phone, password):
        """Xác thực đăng nhập"""
        if not phone or not password:
            return False, None, None

        for user_id, account in self.accounts.items():
            if account.get("phone") == phone:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if account.get("password") == hashed_password:
                    user = User(account)
                    next_window = "mainwindow7" if account.get("role") == "admin" else "mainwindow2"
                    return True, user, next_window

        return False, None, None

    def add_money(self, customer_id, amount):
        """Thêm tiền vào tài khoản khách hàng"""
        accounts = self.load_accounts()
        for acc in accounts.values():
            if acc.get("customer_id") == customer_id:
                acc["money"] = acc.get("money", 0.0) + amount
                self.save_accounts(accounts)
                return True
        return False

    def add_customer(self, first_name, last_name, address, email, phone):
        """Thêm khách hàng mới"""
        accounts = self.load_accounts()

        # Kiểm tra trùng lặp email hoặc số điện thoại
        for acc in accounts.values():
            if acc["email"] == email or acc["phone"] == phone:
                return False

        user_id = f"customer{len(accounts) + 1}"
        customer_id = f"C{len(accounts) + 1:03}"
        hashed_password = hashlib.sha256("123456".encode()).hexdigest()

        new_customer = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "password": hashed_password,
            "role": "customer",
            "customer_id": customer_id,
            "address": address,
            "registration_date": datetime.now().strftime("%Y-%m-%d"),
            "money": 0.0
        }

        accounts[user_id] = new_customer
        self.save_accounts(accounts)
        return True

    def delete_account(self, customer_id):
        """Xóa tài khoản khách hàng"""
        accounts = self.load_accounts()
        user_id_to_delete = None

        for user_id, acc in accounts.items():
            if acc.get("customer_id") == customer_id:
                user_id_to_delete = user_id
                break

        if user_id_to_delete:
            del accounts[user_id_to_delete]
            self.save_accounts(accounts)
            return True
        return False

    @staticmethod
    def load_accounts():
        """Phương thức tĩnh để tải danh sách tài khoản (sử dụng trong MainWindowEx10)"""
        try:
            with open("account.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def add_money(customer_id, amount):
        """Phương thức tĩnh để thêm tiền vào tài khoản khách hàng (sử dụng trong MainWindowEx10)"""
        accounts = AccountHandler.load_accounts()
        for acc in accounts.values():
            if acc.get("customer_id") == customer_id:
                acc["money"] = acc.get("money", 0.0) + amount
                with open("account.json", "w", encoding="utf-8") as file:
                    json.dump(accounts, file, indent=4, ensure_ascii=False)
                return True
        return False

    @staticmethod
    def delete_account(customer_id):
        """Phương thức tĩnh để xóa tài khoản khách hàng (sử dụng trong MainWindowEx10)"""
        accounts = AccountHandler.load_accounts()
        user_id_to_delete = None

        for user_id, acc in accounts.items():
            if acc.get("customer_id") == customer_id:
                user_id_to_delete = user_id
                break

        if user_id_to_delete:
            del accounts[user_id_to_delete]
            with open("account.json", "w", encoding="utf-8") as file:
                json.dump(accounts, file, indent=4, ensure_ascii=False)
            return True
        return False

    @staticmethod
    def add_customer(first_name, last_name, address, email, phone):
        """Phương thức tĩnh để thêm khách hàng mới (sử dụng trong MainWindowEx11)"""
        accounts = AccountHandler.load_accounts()

        # Kiểm tra trùng lặp email hoặc số điện thoại
        for acc in accounts.values():
            if acc.get("email") == email or acc.get("phone") == phone:
                return False

        user_id = f"customer{len(accounts) + 1}"
        customer_id = f"C{len(accounts) + 1:03}"
        hashed_password = hashlib.sha256("123456".encode()).hexdigest()

        new_customer = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "password": hashed_password,
            "role": "customer",
            "customer_id": customer_id,
            "address": address,
            "registration_date": datetime.now().strftime("%Y-%m-%d"),
            "money": 0.0
        }

        accounts[user_id] = new_customer
        with open("account.json", "w", encoding="utf-8") as file:
            json.dump(accounts, file, indent=4, ensure_ascii=False)
        return True


class OrderHandler:
    @staticmethod
    def load_orders():
        """Tải danh sách đơn hàng"""
        try:
            with open("donhang.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_orders(orders):
        """Lưu danh sách đơn hàng"""
        with open("donhang.json", "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4, ensure_ascii=False)

    @staticmethod
    def cancel_order(order_id, reason):
        """Hủy đơn hàng"""
        orders = OrderHandler.load_orders()
        for order in orders:
            if order["order_id"] == order_id:
                order["status"] = "Cancelled"
                order["cancel_reason"] = reason
                OrderHandler.save_orders(orders)
                return True
        return False

    @staticmethod
    def confirm_delivery(order_id):
        """Xác nhận giao hàng"""
        orders = OrderHandler.load_orders()
        for order in orders:
            if order["order_id"] == order_id:
                order["status"] = "Delivered"
                OrderHandler.save_orders(orders)
                return True
        return False

    @staticmethod
    def place_order(order_data):
        """Đặt đơn hàng mới"""
        orders = OrderHandler.load_orders()

        # Tạo ID đơn hàng mới
        order_id = f"ORD{len(orders) + 1:03}"

        # Tạo đơn hàng mới
        new_order = {
            "order_id": order_id,
            "phone": order_data["phone"],
            "items": order_data["items"],
            "total_price": float(order_data["total_price"]),
            "status": "Pending",
            "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Thêm đơn hàng vào danh sách
        orders.append(new_order)
        OrderHandler.save_orders(orders)

        return order_id


class ReservationHandler:
    @staticmethod
    def load_reservations():
        """Tải danh sách đặt bàn"""
        try:
            with open("datban.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_reservations(reservations):
        """Lưu danh sách đặt bàn"""
        with open("datban.json", "w", encoding="utf-8") as file:
            json.dump(reservations, file, indent=4, ensure_ascii=False)

    @staticmethod
    def update_reservation_status(reservation_id, status, table_number=None):
        """Cập nhật trạng thái đặt bàn"""
        reservations = ReservationHandler.load_reservations()
        for res in reservations:
            if res["reservation_id"] == reservation_id:
                res["status"] = status
                if table_number:
                    res["table_number"] = table_number
                res["updated_at"] = get_current_timestamp()
                ReservationHandler.save_reservations(reservations)
                return True
        return False

    @staticmethod
    def create_reservation(phone, date, guest_count, decoration):
        """Tạo đặt bàn mới"""
        reservations = ReservationHandler.load_reservations()

        # Tạo ID đặt bàn mới
        reservation_id = f"RES{len(reservations) + 1:03}"

        # Tạo đặt bàn mới
        new_reservation = {
            "reservation_id": reservation_id,
            "phone": phone,
            "date": date,
            "guest_count": guest_count,
            "decoration": decoration,
            "status": "Pending",
            "created_at": get_current_timestamp(),
            "updated_at": get_current_timestamp()
        }

        # Thêm đặt bàn vào danh sách
        reservations.append(new_reservation)
        ReservationHandler.save_reservations(reservations)

        return reservation_id

    @staticmethod
    def get_user_reservations(phone):
        """Lấy danh sách đặt bàn của người dùng"""
        reservations = ReservationHandler.load_reservations()
        user_reservations = []

        for res in reservations:
            if res.get("phone") == phone:
                user_reservations.append(res)

        return user_reservations


class MenuHandler:
    @staticmethod
    def load_menu():
        """Tải danh sách món ăn"""
        try:
            with open("menu.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def update_menu(menu_items):
        """Cập nhật menu"""
        with open("menu.json", "w", encoding="utf-8") as file:
            json.dump(menu_items, file, indent=4, ensure_ascii=False)


class User:
    """Mô hình người dùng"""

    def __init__(self, user_data):
        self.user_id = user_data.get("user_id")
        self.first_name = user_data.get("first_name")
        self.last_name = user_data.get("last_name")
        self.phone_number = user_data.get("phone")
        self.email = user_data.get("email")
        self.role = user_data.get("role")
        self.address = user_data.get("address")
        self.money = user_data.get("money", 0.0)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


def get_current_timestamp():
    """Trả về timestamp hiện tại"""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")