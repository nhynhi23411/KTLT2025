from account import accounts
from cautrucdulieu import Customer, Admin
import json

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

    def verify_login(self, phone, password):
        for user_id, user in self.accounts.items():
            if user.phone_number == phone and accounts[user_id]["password"] == password:
                if isinstance(user, Customer):
                    return True, user, "mainwindow2"
                elif isinstance(user, Admin):
                    return True, user, "mainwindow7"
        return False, None, None

