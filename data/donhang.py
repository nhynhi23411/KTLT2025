import json
import os

def save_order(order_data):
    """Lưu đơn hàng vào file `donhang.json` và đảm bảo không mất dữ liệu."""
    file_path = "donhang.json"

    # Đọc dữ liệu từ file nếu có
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        donhang_list = []
    else:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                donhang_list = json.load(file)
                if not isinstance(donhang_list, list):  # Đảm bảo JSON là danh sách
                    donhang_list = []
        except json.JSONDecodeError:
            donhang_list = []

    # Tạo `order_id` duy nhất
    new_order_id = f"O{len(donhang_list) + 1:03d}"  # Định dạng O001, O002,...

    # Đảm bảo `total_price` là số nguyên
    order_data["total_price"] = int(order_data.get("total_price", 0))

    # Gán thông tin đơn hàng
    order_data["order_id"] = new_order_id
    order_data["status"] = "Chưa giao"  # Mặc định trạng thái

    # Thêm đơn hàng vào danh sách
    donhang_list.append(order_data)

    # Lưu lại dữ liệu vào file JSON
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(donhang_list, file, ensure_ascii=False, indent=4)
        print(f"Đơn hàng {new_order_id} đã được lưu thành công!")
    except Exception as e:
        print("Lỗi khi lưu đơn hàng:", e)
