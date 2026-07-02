# Decorator - Take Notes

Ghi chú cá nhân về Decorator trong Python - Hàm bọc hàm và các ứng dụng thực tế.

---

## 1. Bản chất

* **Định nghĩa**:
  * Decorator là một hàm đặc biệt dùng để bọc một hàm (hoặc class) khác nhằm mở rộng hoặc thay đổi hành vi của hàm đó mà không cần sửa trực tiếp code bên trong hàm gốc.
  * Sử dụng cú pháp `@decorator_name` đặt ngay phía trên khai báo hàm.
* **Cơ chế hoạt động**:
  * Khi dùng `@decorator` trước hàm `my_func`, bản chất Python sẽ truyền `my_func` làm tham số đầu vào cho decorator.
  * Cú pháp:
    ```python
    @my_decorator
    def my_func():
        pass
    ```
    Tương đương với:
    ```python
    my_func = my_decorator(my_func)
    ```
  * Decorator nhận hàm gốc, định nghĩa một hàm `wrapper` bên trong để xử lý thêm chức năng (bọc trước/sau hàm gốc), sau đó trả về hàm `wrapper` đã nâng cấp đó.

* **Class Decorator (Ví dụ `@dataclass`)**:
  * Không chỉ bọc hàm, decorator còn có thể bọc cả class (Class Decorator).
  * *Ví dụ*: `@dataclass` giúp tự động sinh các constructor `__init__`, hàm hiển thị `__repr__`... giúp viết code class cực kỳ nhanh.
    ```python
    from dataclasses import dataclass

    @dataclass
    class Employee:
        name: str
        dept: str
        salary: int
    ```

---

## 2. Nó giải quyết vấn đề gì?

* **Tránh lặp code (DRY - Don't Repeat Yourself)**: Gom các đoạn code lặp đi lặp lại ở đầu và cuối nhiều hàm khác nhau (như ghi log, đo thời gian chạy, kiểm tra quyền truy cập) vào một nơi duy nhất.
* **Tách biệt logic (Separation of Concerns)**: Hàm chính chỉ tập trung xử lý logic nghiệp vụ chính (business logic), còn các tác vụ bổ trợ (logging, caching, authentication) được tách riêng ra ngoài decorator.
* **Dễ dàng bật/tắt tính năng**: Chỉ cần thêm hoặc xóa dòng `@decorator_name` trên đầu hàm.

---

## 3. Luồng xử lý trong Python

### 3.1 Luồng chạy của Decorator cơ bản
*Ví dụ ghi log hành động rút tiền:*
```python
def ghi_log(func):
    def wrapper():
        print("[LOG]: Hành động này bắt đầu được thực thi...") # Thêm chức năng trước
        func()                                                # Chạy hàm gốc
        print("[LOG]: Hành động đã hoàn thành.")             # Thêm chức năng sau
    return wrapper                                            # Trả về hàm đã nâng cấp

@ghi_log
def rut_tien():
    print("-> Đang xử lý rút tiền: Đếm tiền... Nhả tiền...")

rut_tien()
```

*Kết quả khi chạy:*
```text
1. [LOG]: Hành động này bắt đầu được thực thi...
2. -> Đang xử lý rút tiền: Đếm tiền... Nhả tiền...
3. [LOG]: Hành động đã hoàn thành.
```

### 3.2 Luồng xử lý hàm có tham số (`*args` và `**kwargs`)
* Nếu hàm gốc nhận các tham số (ví dụ: `def add(a, b)`), thì hàm `wrapper` bên trong decorator cũng phải nhận các tham số tương tự. Giải pháp tốt nhất là dùng `*args` và `**kwargs` để bọc được mọi loại hàm bất kể số lượng tham số.
```python
def decorator_with_args(func):
    def wrapper(*args, **kwargs):
        print("Tham số truyền vào:", args, kwargs)
        result = func(*args, **kwargs)
        return result
    return wrapper
```

### 3.3 Bảo toàn thông tin của hàm gốc (`@functools.wraps`)
* Khi bị bọc bởi decorator, các thuộc tính metadata của hàm gốc (như tên hàm `__name__`, docstring `__doc__`) sẽ bị ghi đè bởi thông tin của hàm `wrapper`.
* Khắc phục bằng cách dùng `@functools.wraps(func)` của thư viện built-in `functools` đặt trên đầu hàm `wrapper`.

---

## 4. Ví dụ cần xem

Các ví dụ chi tiết từ cơ bản đến nâng cao (bao gồm cả decorator nhận tham số dạng `@repeat(num_times=3)`) nằm tại:
* [04_decorator_examples.py](file:///home/linh/intern-training/python-deep-notes/examples/04_decorator_examples.py)
