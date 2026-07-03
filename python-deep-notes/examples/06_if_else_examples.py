# =====================================================================
# 1. KHÁI NIỆM CƠ BẢN (Basic Concepts)
# =====================================================================
def demo_basic_if_else(score):
    print(f"--- demo_basic_if_else(score={score}) ---")
    if score >= 90:
        print("Xuất sắc")
    elif score >= 80:
        print("Giỏi")
    else:
        print("Bình thường")
    print()


# =====================================================================
# 2. CƠ CHẾ HOẠT ĐỘNG (Branch Execution Flow)
# =====================================================================
def demo_execution_flow():
    print("--- demo_execution_flow ---")
    # Ví dụ tuần tự từ trên xuống dưới
    condition_1 = False
    condition_2 = True
    condition_3 = True

    if condition_1:
        print("Case 1 chạy")
    elif condition_2:
        print("Case 2 chạy (nhánh đúng đầu tiên)")
    elif condition_3:
        print("Case 3 chạy (nhánh này đúng nhưng bị bỏ qua vì condition_2 đã đúng trước)")
    else:
        print("Case mặc định")
    print()


# =====================================================================
# 3. ĐIỀU KIỆN HẸP PHẢI ĐẶT TRƯỚC ĐIỀU KIỆN RỘNG (Specificity Order)
# =====================================================================
def demo_specificity_order():
    print("--- demo_specificity_order ---")
    age = 70

    print("Cách viết SAI (Điều kiện rộng đặt trước):")
    if age >= 18:
        print("Người lớn")
    elif age >= 60:
        print("Người già")

    print("Cách viết ĐÚNG (Điều kiện hẹp đặt trước):")
    if age >= 60:
        print("Người già")
    elif age >= 18:
        print("Người lớn")
    else:
        print("Trẻ em")
    print()


# =====================================================================
# 4. IF / ELIF / ELSE KHÁC NHIỀU IF RIÊNG (If-Elif-Else vs Multiple Ifs)
# =====================================================================
def demo_if_elif_vs_multiple_ifs(score):
    print(f"--- demo_if_elif_vs_multiple_ifs(score={score}) ---")
    print("Dùng if/elif/else (Chỉ chọn 1 nhánh):")
    if score >= 90:
        print("Xuất sắc")
    elif score >= 80:
        print("Giỏi")
    elif score >= 50:
        print("Đạt")

    print("Dùng nhiều if riêng (Các khối độc lập, có thể cùng chạy):")
    if score >= 90:
        print("Xuất sắc")
    if score >= 80:
        print("Giỏi")
    if score >= 50:
        print("Đạt")
    print()


# =====================================================================
# 5. TRÙNG CASE LÀM NHÁNH PHÍA SAU CHẾT (Duplicate Cases)
# =====================================================================
# Định nghĩa các hàm giả lập để minh họa menu
def add_product(products):
    print("Đã gọi add_product")

def list_products(products):
    print("Đã gọi list_products")

def calculate_inventory_value(products):
    print("Đã gọi calculate_inventory_value")

def find_product(products):
    print("Đã gọi find_product")

def demo_duplicate_cases(choice):
    print(f"--- demo_duplicate_cases(choice='{choice}') ---")
    products = []
    
    print("Cách viết SAI (Trùng case '3'):")
    if choice == "1":
        add_product(products)
    elif choice == "2":
        list_products(products)
    elif choice == "3":
        calculate_inventory_value(products)
    elif choice == "3":  # Nhánh này không bao giờ chạy được
        find_product(products)
    else:
        print("Lựa chọn không hợp lệ")

    print("Cách viết ĐÚNG (Sửa case trùng thành '4'):")
    if choice == "1":
        add_product(products)
    elif choice == "2":
        list_products(products)
    elif choice == "3":
        calculate_inventory_value(products)
    elif choice == "4":
        find_product(products)
    else:
        print("Lựa chọn không hợp lệ")
    print()


# =====================================================================
# 6. ELSE THUỘC VỀ IF GẦN NHẤT CÙNG CẤP INDENT (Indentation Scope)
# =====================================================================
def demo_indentation_scope(is_login, is_admin):
    print(f"--- demo_indentation_scope(is_login={is_login}, is_admin={is_admin}) ---")
    # else của is_admin thuộc về if is_admin vì cùng cấp thụt lề
    if is_login:
        if is_admin:
            print("Admin")
        else:
            print("User thường")  # Thuộc về 'if is_admin'
    else:
        print("Chưa đăng nhập")  # Thuộc về 'if is_login'
    print()


# =====================================================================
# 7. CÁC TRƯỜNG HỢP DỄ GÂY LỖI LOGIC (Common Logic Pitfalls)
# =====================================================================
def demo_logic_pitfalls():
    print("--- demo_logic_pitfalls ---")
    
    # 7.1. Dùng nhiều if riêng thay vì if-elif
    print("7.1. Dùng nhiều if riêng (Sai logic khi chỉ muốn chọn một phân loại):")
    score = 95
    if score >= 90:
        print("Xuất sắc")
    if score >= 80:
        print("Giỏi")
    if score >= 50:
        print("Đạt")
    print()
        
    # 7.2. Trùng case trong cùng một khối
    print("7.2. Trùng case (Không lỗi Syntax nhưng nhánh sau bị chết):")
    choice = "3"
    if choice == "3":
        print("Nhánh A")
    elif choice == "3":
        print("Nhánh B (Chết)")
    print()

    # 7.3. Đặt else sai cấp thụt lề
    # Đã minh họa trong demo_indentation_scope
    
    # 7.4. Dùng else quá sớm làm mất các case cần kiểm tra tiếp
    print("7.4. Dùng else quá sớm:")
    choice_val = "2"
    print("Sai (else đặt quá sớm chặn các case sau):")
    if choice_val == "1":
        print("Thêm sản phẩm")
    else:
        print("Lựa chọn không hợp lệ (Bị coi là không hợp lệ dù là option 2)")
        
    print("Đúng (Thêm các nhánh elif thích hợp rồi mới dùng else):")
    if choice_val == "1":
        print("Thêm sản phẩm")
    elif choice_val == "2":
        print("Danh sách sản phẩm")
    elif choice_val == "3":
        print("Tính tổng kho")
    else:
        print("Lựa chọn không hợp lệ")
    print()


# =====================================================================
# MAIN FUNCTION
# =====================================================================
def main():
    # 1. Khái niệm cơ bản
    demo_basic_if_else(85)
    
    # 2. Cơ chế hoạt động
    demo_execution_flow()
    
    # 3. Điều kiện hẹp đặt trước điều kiện rộng
    demo_specificity_order()
    
    # 4. if/elif/else khác nhiều if riêng
    demo_if_elif_vs_multiple_ifs(95)
    
    # 5. Trùng case làm nhánh phía sau chết
    demo_duplicate_cases("3")
    
    # 6. else thuộc về if gần nhất cùng cấp indent
    demo_indentation_scope(True, False)
    
    # 7. Các lỗi logic thường gặp
    demo_logic_pitfalls()


if __name__ == "__main__":
    main()
