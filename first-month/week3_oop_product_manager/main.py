# ==========================================
# Week 3 - OOP Product Manager
# ==========================================
from product import DigitalProduct, HybridProduct, PhysicalProduct, Product

class ProductManager:
    def __init__(self):
        self.products = []

    def add_product(self, product):
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


def input_basic_product_info():
    name = input("Nhập tên: ")
    price = float(input("Nhập giá: "))
    quantity = int(input("Nhập số lượng: "))
    return name, price, quantity


def create_product():
    print("\n--- CHỌN LOẠI SẢN PHẨM ---")
    print("1. Sản phẩm thường")
    print("2. Sản phẩm vật lý")
    print("3. Sản phẩm số")

    product_type = input("Chọn loại sản phẩm (1-3): ")
    name, price, quantity = input_basic_product_info()

    if product_type == '1':
        return Product(name, price, quantity)
    if product_type == '2':
        weight = float(input("Nhập cân nặng (kg): "))
        return PhysicalProduct(name, price, quantity, weight)
    if product_type == '3':
        file_size = float(input("Nhập dung lượng file (MB): "))
        return DigitalProduct(name, price, quantity, file_size)

    print("Loại sản phẩm không hợp lệ. Tạo sản phẩm thường.")
    return Product(name, price, quantity)


def demo_inheritance():
    print("\n--- DEMO KẾ THỪA ---")
    physical_product = PhysicalProduct("Laptop", 15000000, 2, 1.5)
    digital_product = DigitalProduct("Khóa học Python", 500000, 10, 2048)

    print("PhysicalProduct kế thừa từ Product:")
    print(physical_product)
    print("DigitalProduct kế thừa từ Product:")
    print(digital_product)

    print("\n--- DEMO ĐA KẾ THỪA ---")
    hybrid_product = HybridProduct("Sách kèm file PDF", 250000, 5, 0.4, 100)

    print("HybridProduct kế thừa từ PhysicalProduct và DigitalProduct:")
    print(hybrid_product)
    print(hybrid_product.shipping_info())
    print(hybrid_product.download_info())
    print(HybridProduct.__mro__)


def main():
    manager = ProductManager()
    
    while True:
        print("\n=== OOP PRODUCT MANAGER (TUẦN 3) ===")
        print("1. Thêm sản phẩm")
        print("2. Hiển thị danh sách sản phẩm")
        print("3. Tính tổng giá trị kho")
        print("4. Tìm kiếm sản phẩm")
        print("5. Cập nhật số lượng")
        print("6. Demo kế thừa và đa kế thừa")
        print("7. Thoát")
        
        choice = input("Chọn chức năng (1-7): ")
        
        if choice == '1':
            product = create_product()
            manager.add_product(product)
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
            demo_inheritance()
        elif choice == '7':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
