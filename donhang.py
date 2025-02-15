import json

# Đọc danh sách đơn hàng từ file nếu có
try:
    with open("donhang.json", "r", encoding="utf-8") as file:
        donhang_list = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    donhang_list = []

def save_order(order_data):
    try:
        order_data["status"] = "Chưa giao"
        donhang_list.append(order_data)
        with open("donhang.json", "w", encoding="utf-8") as file:
            json.dump(donhang_list, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Lỗi khi lưu đơn hàng:", e)
