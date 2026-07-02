# ==========================================
# Week 1 - Basic Product CLI
# ==========================================

print("=== CHƯƠNG TRÌNH QUẢN LÝ SẢN PHẨM ===")

products = []

while True:
    print("\n1. Thêm sản phẩm")
    print("2. Hiển thị danh sách sản phẩm")
    print("3. Tính tổng giá trị kho")
    print("4. Tìm kiếm sản phẩm")
    print("5. Thoát")
    
    choice = input("Chọn chức năng (1-5): ")
    
    if choice == '1':
        print("\n--- THÊM SẢN PHẨM ---")
        name = input("Nhập tên sản phẩm: ")
        price = float(input("Nhập giá (VNĐ): "))
        quantity = int(input("Nhập số lượng: "))
        
        product = {
            "name": name,
            "price": price,
            "quantity": quantity
        }
        products.append(product)
        print("Đã thêm sản phẩm thành công!")

    elif choice == '2':
        print("\n--- DANH SÁCH SẢN PHẨM ---")
        if len(products) == 0:
            print("Chưa có sản phẩm nào.")
        else:
            for p in products:
                print(f"Tên: {p['name']} - Giá: {p['price']} - SL: {p['quantity']}")

    elif choice == '3':
        print("\n--- TỔNG GIÁ TRỊ KHO ---")
        total_value = 0
        for p in products:
            total_value += p['price'] * p['quantity']
        print(f"Tổng giá trị kho là: {total_value} VNĐ")

    elif choice == '4':
        print("\n--- TÌM KIẾM SẢN PHẨM ---")
        keyword = input("Nhập từ khóa tìm kiếm: ")
        found = False
        for p in products:
            if keyword.lower() in p['name'].lower():
                print(f"Tên: {p['name']} - Giá: {p['price']} - SL: {p['quantity']}")
                found = True
        
        if not found:
            print("Không tìm thấy sản phẩm phù hợp.")

    elif choice == '5':
        print("Tạm biệt!")
        break
        
    else:
        print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
