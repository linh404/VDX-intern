# ==========================================
# Week 4 - Business Logic & File I/O
# ==========================================
import json
import os
from product import Product

DATA_FILE = "products.json"

def load_products():
    """
    Đọc dữ liệu từ file JSON, trả về list các object Product.
    Nếu file không tồn tại hoặc lỗi định dạng, trả về list rỗng.
    """
    if not os.path.exists(DATA_FILE):
        return []
        
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Product(item['name'], item['price'], item['quantity']) for item in data]
    except json.JSONDecodeError:
        print("Lỗi: Dữ liệu JSON không hợp lệ.")
        return []


def save_products(products):
    """Lưu list object Product xuống file JSON."""
    data = [product.to_dict() for product in products]
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def add_product(products, name, price, quantity):
    """Tạo sản phẩm mới, thêm vào list và lưu file."""
    new_product = Product(name, price, quantity)
    products.append(new_product)
    save_products(products)


def find_product(products, keyword):
    """Tìm sản phẩm theo tên."""
    print("\n--- KẾT QUẢ TÌM KIẾM ---")
    found = False
    for p in products:
        if keyword.lower() in p.name.lower():
            print(p)
            found = True
    if not found:
        print("Không tìm thấy sản phẩm phù hợp.")


def update_quantity(products, name, new_quantity):
    """Cập nhật số lượng sản phẩm."""
    for p in products:
        if p.name.lower() == name.lower():
            p.quantity = new_quantity
            save_products(products)
            print(f"Đã cập nhật số lượng của {p.name} thành {new_quantity}.")
            return
    print(f"Không tìm thấy sản phẩm '{name}'.")


def delete_product(products, name):
    """Xóa sản phẩm theo tên."""
    for i, p in enumerate(products):
        if p.name.lower() == name.lower():
            del products[i]
            save_products(products)
            print(f"Đã xóa sản phẩm '{p.name}'.")
            return
    print(f"Không tìm thấy sản phẩm '{name}'.")


def calculate_total_value(products):
    """Tính tổng giá trị kho."""
    print("\n--- TỔNG GIÁ TRỊ KHO ---")
    total_value = sum(p.get_total_value() for p in products)
    print(f"Tổng giá trị kho là: {total_value} VNĐ")
