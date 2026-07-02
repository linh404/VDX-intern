# ==========================================
# Week 2 - Function + Validation
# ==========================================

def input_product():
    """Hàm nhập thông tin sản phẩm và validate."""
    print("\n--- THÊM SẢN PHẨM ---")
    
    while True:
        name = input("Nhập tên sản phẩm: ").strip()
        if name:
            break
        print("Tên không được để trống!")
    
    while True:
        try:
            price = float(input("Nhập giá (VNĐ): "))
            if price > 0:
                break
            print("Giá phải lớn hơn 0!")
        except ValueError:
            print("Giá trị nhập không hợp lệ, vui lòng nhập số!")
    
    while True:
        try:
            quantity = int(input("Nhập số lượng: "))
            if quantity >= 0:
                break
            print("Số lượng phải lớn hơn hoặc bằng 0!")
        except ValueError:
            print("Giá trị nhập không hợp lệ, vui lòng nhập số nguyên!")
    
    return {"name": name, "price": price, "quantity": quantity}


def add_product(products):
    """Thêm sản phẩm vào danh sách."""
    product = input_product()
    products.append(product)
    print("Đã thêm sản phẩm thành công!")


def list_products(products):
    """Hiển thị danh sách sản phẩm."""
    print("\n--- DANH SÁCH SẢN PHẨM ---")
    if not products:
        print("Chưa có sản phẩm nào.")
    else:
        for p in products:
            print(f"Tên: {p['name']} - Giá: {p['price']} - SL: {p['quantity']}")


def calculate_inventory_value(products):
    """Tính và in ra tổng giá trị kho."""
    print("\n--- TỔNG GIÁ TRỊ KHO ---")
    total_value = sum(p['price'] * p['quantity'] for p in products)
    print(f"Tổng giá trị kho là: {total_value} VNĐ")


def find_product(products, keyword):
    """Tìm kiếm sản phẩm theo tên."""
    print("\n--- KẾT QUẢ TÌM KIẾM ---")
    found = False
    for p in products:
        if keyword.lower() in p['name'].lower():
            print(f"Tên: {p['name']} - Giá: {p['price']} - SL: {p['quantity']}")
            found = True
    
    if not found:
        print("Không tìm thấy sản phẩm phù hợp.")


def show_menu():
    """Hiển thị menu chính."""
    print("\n=== CHƯƠNG TRÌNH QUẢN LÝ SẢN PHẨM (TUẦN 2) ===")
    print("1. Thêm sản phẩm")
    print("2. Hiển thị danh sách sản phẩm")
    print("3. Tính tổng giá trị kho")
    print("4. Tìm kiếm sản phẩm")
    print("5. Thoát")


def main():
    products = []
    
    while True:
        show_menu()
        choice = input("Chọn chức năng (1-5): ")
        
        if choice == '1':
            add_product(products)
        elif choice == '2':
            list_products(products)
        elif choice == '3':
            calculate_inventory_value(products)
        elif choice == '4':
            keyword = input("Nhập tên sản phẩm cần tìm: ")
            find_product(products, keyword)
        elif choice == '5':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
