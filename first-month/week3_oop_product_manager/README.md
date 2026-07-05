# Week 3 - OOP Product Manager

## Kiến thức áp dụng
- Lập trình hướng đối tượng (Classes and Objects)
- Phương thức khởi tạo (Constructor - `__init__`)
- Thuộc tính đối tượng (Instance Attributes)
- Phương thức đối tượng (Instance Methods)
- Class method (`@classmethod`)
- Static method (`@staticmethod`)
- Các phương thức đặc biệt (Dunder methods, tiêu biểu là `__str__`)
- Import module tự viết giữa các file trong cùng thư mục

## Python OOP: 3 loại method hay gặp

| Loại method | Nhận gì? | Dùng khi nào? |
|---|---|---|
| Instance method | `self` | Cần xử lý dữ liệu của object cụ thể |
| Class method | `cls` | Cần xử lý class đang gọi method |
| Static method | Không có `self`/`cls` | Chỉ là hàm tiện ích đặt trong class cho gọn |

### Instance method: dùng `self`

```python
def get_total_value(self):
    return self.price * self.quantity
```

Dùng khi mỗi object có dữ liệu riêng. Ví dụ mỗi `Product` có `price`, `quantity` khác nhau.

### Class method: dùng `cls`

```python
@classmethod
def create_default(cls, name):
    return cls(name, cls.default_role)
```

Trong [test_oop.py](file:///home/linh/VDX-intern/first-month/week3_oop_product_manager/test_oop.py):

```python
admin = Admin.create_default("Binh")
staff = Staff.create_default("Cuong")
```

`Admin` gọi thì `cls` là `Admin`. `Staff` gọi thì `cls` là `Staff`.

Vì vậy:

```python
return cls(name, cls.default_role)
```

sẽ tạo đúng class đang gọi:

```text
Admin -> tạo Admin, role admin
Staff -> tạo Staff, role staff
```

Nếu ghi cứng:

```python
return User(name, User.default_role)
```

thì dù `Staff` gọi vẫn tạo `User`, role `user`.

Mục đích chính của `cls`: viết logic một lần ở class cha, class con gọi vẫn chạy đúng theo class con. Code ít phụ thuộc cứng vào `User`, dễ dùng lại khi có kế thừa.

### Static method: không dùng `self` hoặc `cls`

```python
@staticmethod
def is_valid_quantity(quantity):
    return quantity >= 0
```

Dùng khi hàm không cần dữ liệu object, cũng không cần biết class nào đang gọi.

### Tóm tắt

```text
self -> object cụ thể
cls  -> class đang gọi method
static -> hàm tiện ích, không cần object/class
```

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
