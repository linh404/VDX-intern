# Glossary - Thuật ngữ Python cơ bản

Bảng tra cứu và định nghĩa chi tiết các thuật ngữ cốt lõi trong Python.

---

## 1. Nhóm Function (Hàm)

* **`parameter` (Tham số)**: Tên biến được khai báo trong phần định nghĩa của hàm.
  * *Ví dụ*: Trong `def greet(name):`, `name` là parameter.
* **`argument` (Đối số)**: Giá trị thực tế được truyền vào hàm khi gọi hàm.
  * *Ví dụ*: Trong `greet("An")`, `"An"` là argument.
* **`positional argument` (Đối số vị trí)**: Đối số được gán vào tham số dựa theo thứ tự xuất hiện của nó khi gọi hàm.
* **`keyword argument` (Đối số đặt tên)**: Đối số được truyền kèm theo tên tham số (ví dụ: `greet(name="An")`), giúp không phụ thuộc vào thứ tự truyền.
* **`*args`**: Cú pháp gom các đối số vị trí dư thừa truyền vào hàm thành một `tuple`.
* **`**kwargs`**: Cú pháp gom các đối số đặt tên dư thừa truyền vào hàm thành một `dict`.

---

## 2. Nhóm Collection (Tập hợp)

* **`iterable`**: Bất kỳ đối tượng nào hỗ trợ duyệt qua các phần tử của nó (ví dụ: list, tuple, dict, set, string). Đối tượng này chứa phương thức `__iter__()`.
* **`iterator`**: Đối tượng đại diện cho một luồng dữ liệu, trả về từng phần tử một khi gọi hàm `next()`. Đối tượng này chứa phương thức `__next__()` và `__iter__()`.
* **`sequence`**: Một dạng iterable hỗ trợ truy cập phần tử bằng chỉ số (index) nguyên và có độ dài cụ thể (ví dụ: list, tuple, string).
* **`mapping`**: Cấu trúc dữ liệu ánh xạ các khóa (key) sang các giá trị (value), ví dụ điển hình là `dict`.
* **`hashable`**: Một đối tượng là hashable nếu nó có giá trị hash không đổi trong suốt vòng đời (immutable) và có thể so sánh bằng. Chỉ có đối tượng hashable mới được làm key của `dict` hoặc phần tử của `set` (ví dụ: int, float, str, tuple).

---

## 3. Nhóm OOP (Hướng đối tượng)

* **`class`**: Bản thiết kế (blueprint) định nghĩa cấu trúc dữ liệu và hành vi cho các đối tượng được tạo ra từ nó.
* **`object` (Đối tượng)**: Một thực thể cụ thể (instance) được tạo ra từ một class.
* **`attribute` (Thuộc tính)**: Các biến gắn liền với đối tượng hoặc class dùng để lưu trữ dữ liệu trạng thái.
* **`method` (Phương thức)**: Các hàm được định nghĩa bên trong class để xử lý hành vi của đối tượng.
* **`class variable` (Biến class)**: Biến được khai báo trực tiếp trong class (ngoài các phương thức), dùng chung và chia sẻ bởi tất cả các instance của class đó.
* **`MRO` (Method Resolution Order)**: Thứ tự tìm kiếm thuộc tính và phương thức trong các lớp cha của Python (rất quan trọng khi đa kế thừa).
* **`descriptor`**: Một object định nghĩa các phương thức `__get__()`, `__set__()`, hoặc `__delete__()` để thay đổi hành vi truy cập thuộc tính của object khác.

---

## 4. Nhóm Python Style (Tư duy Python)

* **`duck-typing`**: Tư duy lập trình kiểu động: *"Nếu nó đi như một con vịt và kêu như một con vịt, thì nó là một con vịt"*. Ta quan tâm đến hành vi (phương thức) của đối tượng hơn là kiểu dữ liệu thực tế của nó.
* **`EAFP` (Easier to Ask for Forgiveness than Permission)**: Tư duy viết code *"Cứ làm đi rồi xin lỗi sau"*. Sử dụng khối `try-except` để bắt lỗi khi chạy, thay vì kiểm tra trước.
* **`LBYL` (Look Before You Leap)**: Tư duy viết code *"Nhìn kỹ trước khi nhảy"*. Sử dụng các câu lệnh `if` kiểm tra điều kiện trước khi thực thi hành động để tránh lỗi.
* **`Pythonic`**: Cách viết code ngắn gọn, rõ ràng, tối ưu và tận dụng tốt nhất các đặc tính đặc trưng của ngôn ngữ Python.

---

## 5. Nhóm Module & Package

* **`module`**: Một file Python đơn lẻ (ví dụ: `myfile.py`) chứa code có thể tái sử dụng.
* **`package`**: Một thư mục chứa một hoặc nhiều module Python khác.
* **`import path`**: Đường dẫn Python sử dụng để tìm kiếm và nạp các module/package khi chạy lệnh `import`.
* **`regular package`**: Package truyền thống có chứa file `__init__.py`.
* **`namespace package`**: Package được gộp từ nhiều thư mục khác nhau trên đĩa mà không cần file `__init__.py` (tính năng từ Python 3.3+).

---

## 6. Nhóm Nâng cao (Advanced)

* **`generator`**: Hàm trả về một iterator bằng cách sử dụng từ khóa `yield` thay vì `return`, giúp sinh dữ liệu lần lượt và tiết kiệm bộ nhớ.
* **`coroutine`**: Hàm có thể tạm dừng và tiếp tục thực thi tại nhiều thời điểm khác nhau (thường dùng trong lập trình bất đồng bộ `async/await`).
* **`GIL` (Global Interpreter Lock)**: Cơ chế khóa trong CPython giúp đảm bảo tại một thời điểm chỉ có một luồng (thread) thực thi bytecode của Python để tránh xung đột bộ nhớ.
* **`context manager`**: Đối tượng quản lý tài nguyên (ví dụ: đóng mở file, kết nối DB) thông qua cú pháp `with`, tự động giải phóng tài nguyên nhờ phương thức `__enter__()` và `__exit__()`.

---

Tài liệu tham khảo: [Python Glossary](https://docs.python.org/3/glossary.html)
