from account import accounts
from cautrucdulieu import Customer, Admin
import json
import hashlib

class AccountHandler:
    def __init__(self):
        # Sử dụng danh sách tài khoản từ file account.py
        self.accounts = {user_id: self.create_user_object(user_id, info) for user_id, info in accounts.items()}

    def create_user_object(self, user_id, info):
        if info["role"] == "admin":
            return Admin(user_id, info["first_name"], info["last_name"], info["phone"], info["email"],
                         info["admin_id"], info["role"])
        else:
            return Customer(user_id, info["first_name"], info["last_name"], info["phone"], info["email"],
                            info["customer_id"], info["address"], info["registration_date"], info["money"])

    def hash_password(self, password):
        """Mã hóa mật khẩu bằng SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_login(self, phone, password):
        """Kiểm tra đăng nhập với mật khẩu đã mã hóa"""
        hashed_password = self.hash_password(password)  # Mã hóa mật khẩu nhập vào để so sánh

        for user_id, user in self.accounts.items():
            if user.phone_number == phone and accounts[user_id]["password"] == hashed_password:
                if isinstance(user, Customer):
                    return True, user, "mainwindow2"
                elif isinstance(user, Admin):
                    return True, user, "mainwindow7"

        return False, None, None