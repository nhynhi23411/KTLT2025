from account import accounts
from cautrucdulieu import Customer, Admin
import hashlib

class AccountHandler:
    def __init__(self):
        # Sử dụng danh sách tài khoản từ account.py
        self.accounts = {user_id: self.create_user_object(user_id, info) for user_id, info in accounts.items()}

    def create_user_object(self, user_id, info):
        """Tạo đối tượng User (Admin hoặc Customer) từ dữ liệu account.py"""
        if info["role"] == "admin":
            return Admin(
                user_id,
                info["first_name"],
                info["last_name"],
                info["phone"],
                info["email"],
                info["admin_id"],
                info["role"]
            )
        else:
            return Customer(
                user_id,
                info["first_name"],
                info["last_name"],
                info["phone"],
                info["email"],
                info.get("customer_id", f"C{int(user_id.replace('customer', '')):03}"),  # Nếu thiếu, tự động tạo
                info.get("address", "Unknown"),  # Nếu thiếu, gán mặc định
                info.get("registration_date", "0000-00-00"),  # Nếu thiếu, gán ngày mặc định
                info.get("money", 0.0)  # Nếu thiếu, gán mặc định 0.0
            )

    def hash_password(self, password):
        """Mã hóa mật khẩu bằng SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_login(self, phone, password):
        """Kiểm tra đăng nhập với mật khẩu đã mã hóa"""
        hashed_password = self.hash_password(password)  # Mã hóa mật khẩu nhập vào

        for user_id, user in self.accounts.items():
            stored_password = accounts[user_id].get("password", "")

            # Kiểm tra số điện thoại và mật khẩu đã mã hóa
            if user.phone_number == phone and stored_password == hashed_password:
                if isinstance(user, Customer):
                    return True, user, "mainwindow2"
                elif isinstance(user, Admin):
                    return True, user, "mainwindow7"

        return False, None, None
