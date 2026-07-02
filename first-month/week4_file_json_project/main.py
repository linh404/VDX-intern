# ==========================================
# Week 4 - File + JSON Mini Project
# ==========================================
import product_service

def main():
    # Load dữ liệu từ file ngay khi khởi động
    products = product_service.load_products()
    
    while True:
        print("\n=== FINAL MINI PROJECT (TUẦN 4) ===")
        print("1. Thêm sản phẩm")
        print("2. Hiển thị danh sách sản phẩm")
        print("3. Tìm kiếm sản phẩm")
        print("4. Cập nhật số lượng")
        print("5. Xóa sản phẩm")
        print("6. Tính tổng giá trị kho")
        print("7. Thoát")
        
        choice = input("Chọn chức năng (1-7): ")
        
        if choice == '1':
            name = input("Nhập tên: ")
            price = float(input("Nhập giá: "))
            quantity = int(input("Nhập số lượng: "))
            product_service.add_product(products, name, price, quantity)
            print("Thêm thành công!")
            
        elif choice == '2':
            print("\n--- DANH SÁCH ---")
            for p in products:
                print(p)
                
        elif choice == '3':
            keyword = input("Nhập từ khóa tìm kiếm: ")
            product_service.find_product(products, keyword)
                
        elif choice == '4':
            name = input("Nhập tên sản phẩm cần cập nhật: ")
            new_qty = int(input("Nhập số lượng mới: "))
            product_service.update_quantity(products, name, new_qty)
            
        elif choice == '5':
            name = input("Nhập tên sản phẩm cần xóa: ")
            product_service.delete_product(products, name)
            
        elif choice == '6':
            product_service.calculate_total_value(products)
            
        elif choice == '7':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
