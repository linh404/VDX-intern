# Week 3 - OOP Product Manager

## Kiến thức áp dụng
- Lập trình hướng đối tượng (Classes and Objects)
- Phương thức khởi tạo (Constructor - `__init__`)
- Thuộc tính đối tượng (Instance Attributes)
- Phương thức đối tượng (Instance Methods)
- Các phương thức đặc biệt (Dunder methods, tiêu biểu là `__str__`)
- Import module tự viết giữa các file trong cùng thư mục

## Bài thực hành: Quản lý sản phẩm theo Hướng đối tượng (OOP)
Tái cấu trúc hoàn chỉnh ứng dụng quản lý sản phẩm bằng mô hình Lập trình hướng đối tượng (OOP).

### Thiết kế các Lớp (Classes):
1. **Lớp `Product`** (trong [product.py](file:///home/linh/VDX-intern/first-month/week3_oop_product_manager/product.py)):
   - Đại diện cho thực thể sản phẩm.
   - Thuộc tính: `name`, `price`, `quantity`.
   - Phương thức:
     - `get_total_value()`: Trả về giá trị tồn kho của sản phẩm (`price * quantity`).
     - `to_dict()`: Trả về biểu diễn dictionary của sản phẩm.
     - `__str__()`: Định nghĩa chuỗi hiển thị tùy biến của đối tượng Product.
2. **Lớp `ProductManager`** (trong [main.py](file:///home/linh/VDX-intern/first-month/week3_oop_product_manager/main.py)):
   - Quản lý danh sách các đối tượng `Product`.
   - Chứa các phương thức xử lý danh sách: `add_product`, `list_products`, `calculate_inventory_value`, `find_product`, `update_quantity`.

### Chức năng chính:
1. **Thêm sản phẩm**: Khởi tạo thực thể `Product` và thêm vào danh sách quản lý.
2. **Hiển thị danh sách sản phẩm**: In thông tin bằng cách gọi trực tiếp hàm `print(product)` (tự động kích hoạt `__str__`).
3. **Tính tổng giá trị kho**: Gọi `get_total_value()` trên từng thực thể `Product`.
4. **Tìm kiếm sản phẩm**.
5. **Cập nhật số lượng**: Tìm kiếm sản phẩm theo tên và thay đổi thuộc tính `quantity`.
6. **Thoát**.
