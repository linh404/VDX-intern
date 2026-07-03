from enum import Enum

# =====================================================================
# 1. KHÔNG CÓ FALL-THROUGH (Không cần/Không dùng break)
# =====================================================================
def demo_no_fall_through(value):
    print(f"--- demo_no_fall_through({value}) ---")
    match value:
        case 1:
            print("Xử lý cho case 1")
            # Không cần break ở đây. Luồng xử lý tự động dừng và thoát match.
        case 2:
            print("Xử lý cho case 2")
        case _:
            print("Xử lý mặc định (wildcard)")
    print("Đã thoát khỏi match-case\n")


# =====================================================================
# 2. BẪY GÁN BIẾN (Variable Capture Gotcha)
# =====================================================================
# Ví dụ về việc sử dụng x = 10, y = 20 để thấy lỗi logic khi dùng biến thường làm case:
def demo_variable_capture_bug():
    print("--- demo_variable_capture_bug ---")
    x = 10
    y = 20

    print(f"Trước match: x = {x}, y = {y}")
    
    match x:
        case y:  
            # LỖI LOGIC: Python hiểu 'y' ở đây là một biến chụp (capture variable).
            # Nó sẽ khớp với BẤT KỲ giá trị nào của x và gán ngược giá trị đó vào 'y'.
            print("-> [BUG] Khớp case y thành công! (Dù x là 10 chứ không phải 20)")
            print(f"-> Trong case: y bị gán lại thành = {y}")
            
    print(f"Sau match: y = {y} (Giá trị của y đã bị thay đổi trong scope này!)\n")


# CÁCH GIẢI QUYẾT 1: Dùng Dotted Name (Tên chứa dấu chấm)
class Constants:
    y = 20

def demo_dotted_name_solution(x_val):
    print(f"--- demo_dotted_name_solution(x = {x_val}) ---")
    
    # Python nhận diện tên chứa dấu chấm (Constants.y) là giá trị hằng số để so khớp
    match x_val:
        case Constants.y:
            print("Khớp với Constants.y (20)")
        case _:
            print("Không khớp với Constants.y")
    print()


# CÁCH GIẢI QUYẾT 2: Dùng Guard (Điều kiện if)
def demo_guard_solution():
    print("--- demo_guard_solution ---")
    x = 10
    y = 20
    
    match x:
        # Sử dụng guard 'if' để so sánh bằng một cách tường minh
        case value if value == y:
            print("Khớp với y (20)")
        case value:
            # 'value' ở đây là capture variable hứng mọi giá trị không khớp ở trên
            print(f"Không khớp với y. Giá trị thực tế nhận được: {value}")
    print()


# =====================================================================
# 3. KHỚP CẤU TRÚC PHỨC TẠP (Structural Matching & Destructuring)
# =====================================================================
# Khớp Sequence (List/Tuple)
def demo_sequence_matching(command_str):
    print(f"--- demo_sequence_matching('{command_str}') ---")
    command_parts = command_str.split()
    
    match command_parts:
        case ["quit" | "exit"]:
            print("Thoát chương trình.")
        case ["go", ("north" | "south" | "east" | "west") as direction]:
            print(f"Di chuyển theo hướng: {direction}")
        case ["go", unknown_direction]:
            print(f"Hướng đi '{unknown_direction}' không hợp lệ!")
        case ["teleport", x, y]:
            print(f"Dịch chuyển tức thời đến tọa độ ({x}, {y})")
        case ["drop", *items]:
            # Dùng *items để gom tất cả các phần tử còn lại vào một list
            print(f"Vứt bỏ các món đồ sau: {items}")
        case _:
            print("Lệnh không hợp lệ!")
    print()


# Khớp Dictionary (Mapping)
def demo_dict_matching(data):
    print(f"--- demo_dict_matching with data: {data} ---")
    
    # 1. Cách viết bằng match-case (Vừa kiểm tra cấu trúc vừa capture và bind 'name')
    print("[match-case] Đang xử lý...")
    match data:
        case {"type": "user", "info": {"name": name}}:
            print(f"-> Thành công! Tìm thấy user có name: '{name}'")
        case _:
            print("-> Không khớp cấu trúc user mong muốn.")
            
    # 2. Cách viết bằng if-else truyền thống để đạt độ an toàn tương đương
    print("[if-else] Đang xử lý...")
    if (isinstance(data, dict) 
        and data.get("type") == "user" 
        and isinstance(data.get("info"), dict) 
        and "name" in data["info"]):
        
        name = data["info"]["name"]  # Trích xuất thủ công
        print(f"-> Thành công! Tìm thấy user có name: '{name}'")
    else:
        print("-> Không khớp cấu trúc user mong muốn.")
    print()


# Khớp Class Instance
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def demo_class_matching(point):
    print(f"--- demo_class_matching (Point({point.x}, {point.y})) ---")
    match point:
        case Point(x=0, y=0):
            print("Điểm nằm ngay Gốc tọa độ")
        case Point(x=x, y=y) if x == y:
            print(f"Điểm nằm trên đường phân giác y = x tại ({x}, {y})")
        case Point(x=x, y=y):
            # x, y ở đây tự động được trích xuất từ thuộc tính của đối tượng Point
            print(f"Điểm bất kỳ có tọa độ X={x}, Y={y}")
    print()


# Khớp kèm Guard và Kiểm tra kiểu (Class Pattern với Guard)
def demo_guard_with_type_check(number):
    print(f"--- demo_guard_with_type_check({repr(number)}) ---")
    match number:
        case int() as n if n % 2 == 0:
            print(f"{n} là số chẵn")
        case int() as n:
            print(f"{n} là số lẻ")
        case _:
            print(f"Không phải số nguyên! Nhận được kiểu: {type(number).__name__}")
    print()


# =====================================================================
# MAIN FUNCTION
# =====================================================================
def main():
    # 1. Minh họa không fall-through
    demo_no_fall_through(1)
    
    # 2. Minh họa bẫy gán biến và cách sửa
    demo_variable_capture_bug()
    demo_dotted_name_solution(10)
    demo_guard_solution()
    
    print("-" * 50)
    
    # 3. Minh họa khớp cấu trúc nâng cao
    demo_sequence_matching("go south")
    demo_sequence_matching("go nowhere")
    demo_sequence_matching("teleport 10 20")
    demo_sequence_matching("drop sword shield potion")
    
    print("-" * 50)
    
    # Thử nghiệm với các trường hợp dữ liệu khác nhau
    # Trường hợp 1: Đúng cấu trúc hoàn toàn
    demo_dict_matching({
        "type": "user",
        "info": {"name": "Linh", "age": 20}
    })
    # Trường hợp 2: Sai giá trị của type (là admin chứ không phải user)
    demo_dict_matching({
        "type": "admin",
        "info": {"name": "Linh"}
    })
    # Trường hợp 3: Sai cấu trúc (info không phải dict mà là string)
    demo_dict_matching({
        "type": "user",
        "info": "Thông tin trống"
    })
    
    print("-" * 50)
    
    demo_class_matching(Point(0, 0))
    demo_class_matching(Point(5, 5))
    demo_class_matching(Point(3, 8))
    
    print("-" * 50)
    print("Minh họa Khớp kèm Guard và Kiểm tra kiểu:")
    demo_guard_with_type_check(10)
    demo_guard_with_type_check(7)
    demo_guard_with_type_check("hello")



if __name__ == "__main__":
    main()
