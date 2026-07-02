# ==========================================
# Week 3 - OOP Product Manager
# ==========================================
from product import Product

class ProductManager:
    def __init__(self):
        self.products = []

    def add_product(self, name, price, quantity):
        product = Product(name, price, quantity)
        self.products.append(product)

    def list_products(self):
        print("\n--- DANH SÁCH SẢN PHẨM ---")
        if not self.products:
            print("Chưa có sản phẩm nào.")
        else:
            for product in self.products:
                print(product)

    def calculate_inventory_value(self):
        print("\n--- TỔNG GIÁ TRỊ KHO ---")
        total_value = sum(product.get_total_value() for product in self.products)
        print(f"Tổng giá trị kho là: {total_value} VNĐ")

    def find_product(self, keyword):
        print("\n--- KẾT QUẢ TÌM KIẾM ---")
        found = False
        for product in self.products:
            if keyword.lower() in product.name.lower():
                print(product)
                found = True
        
        if not found:
            print("Không tìm thấy sản phẩm phù hợp.")

    def update_quantity(self, name, new_quantity):
        for product in self.products:
            if product.name.lower() == name.lower():
                product.quantity = new_quantity
                print(f"Đã cập nhật số lượng của {product.name} thành {new_quantity}.")
                return
        print(f"Không tìm thấy sản phẩm nào có tên '{name}'.")

def main():
    manager = ProductManager()
    
    while True:
        print("\n=== OOP PRODUCT MANAGER (TUẦN 3) ===")
        print("1. Thêm sản phẩm")
        print("2. Hiển thị danh sách sản phẩm")
        print("3. Tính tổng giá trị kho")
        print("4. Tìm kiếm sản phẩm")
        print("5. Cập nhật số lượng")
        print("6. Thoát")
        
        choice = input("Chọn chức năng (1-6): ")
        
        if choice == '1':
            name = input("Nhập tên: ")
            price = float(input("Nhập giá: "))
            quantity = int(input("Nhập số lượng: "))
            manager.add_product(name, price, quantity)
            print("Đã thêm thành công!")
        elif choice == '2':
            manager.list_products()
        elif choice == '3':
            manager.calculate_inventory_value()
        elif choice == '4':
            keyword = input("Nhập từ khóa: ")
            manager.find_product(keyword)
        elif choice == '5':
            name = input("Nhập tên sản phẩm cần cập nhật: ")
            new_qty = int(input("Nhập số lượng mới: "))
            manager.update_quantity(name, new_qty)
        elif choice == '6':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
