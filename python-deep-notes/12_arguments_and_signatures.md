# Arguments & Function Signatures

Ghi chú chi tiết về cách truyền tham số (Arguments) và Chữ ký hàm (Signature) trong Python.

---

## 1. Tham số `*args` và `**kwargs`

Python cung cấp 2 cách truyền tham số linh hoạt khi số lượng đối số truyền vào không cố định:

### 1.1 `*args` (Positional Arguments)
* **Định nghĩa**: Gom tất cả các tham số vị trí dư thừa truyền vào hàm thành một **tuple**.
* **Ví dụ**:
  ```python
  def sum_numbers(*args):
      print(args)  # (1, 2, 3)
      return sum(args)

  sum_numbers(1, 2, 3)
  ```

### 1.2 `**kwargs` (Keyword Arguments)
* **Định nghĩa**: Gom tất cả các tham số truyền theo cặp `key=value` dư thừa thành một **dictionary**.
* **Ví dụ**:
  ```python
  def print_info(**kwargs):
      print(kwargs)  # {'name': 'Linh', 'age': 20}

  print_info(name="Linh", age=20)
  ```

---

## 2. Kiểm soát cách truyền đối số (Argument Control)

Từ Python 3.8+, ta có thể kiểm soát nghiêm ngặt cách truyền đối số vào hàm thông qua ký tự `/` và `*`.

```
def func(positional_only, /, positional_or_keyword, *, keyword_only):
    pass
```

### 2.1 Positional-only parameters (Dùng `/`)
* Các tham số đứng **trước dấu `/`** bắt buộc phải truyền dưới dạng tham số vị trí (positional argument), không được phép truyền bằng tên (keyword).
* **Mục đích**: Giúp ta có thể đổi tên tham số ở lớp cha mà không làm hỏng code của các lớp con/caller đang dùng.
* **Ví dụ**:
  ```python
  def greet(name, /, greeting="Hello"):
      return f"{greeting}, {name}"

  greet("Linh")            # Hợp lệ
  # greet(name="Linh")     # TypeError: greet() got some positional-only arguments passed as keyword arguments
  ```

### 2.2 Keyword-only parameters (Dùng `*`)
* Các tham số đứng **sau dấu `*`** bắt buộc phải truyền dưới dạng tên (`key=value`), không được phép truyền theo vị trí.
* **Mục đích**: Bắt buộc caller phải tường minh khi truyền các tham số cấu hình quan trọng, tránh nhầm lẫn thứ tự.
* **Ví dụ**:
  ```python
  def calculate_tax(price, *, tax_rate):
      return price * tax_rate

  calculate_tax(100, tax_rate=0.1) # Hợp lệ
  # calculate_tax(100, 0.1)        # TypeError: calculate_tax() takes 1 positional argument but 2 were given
  ```

---

## 3. Signature của Hàm (Function Signature)

### 3.1 Signature là gì?
Signature (chữ ký) của một hàm/phương thức trong Python bao gồm:
1. **Tên hàm** (Function Name).
2. **Các tham số** (Parameters): Số lượng, thứ tự, tên tham số, giá trị mặc định (default values) của chúng.
3. **Kiểu dữ liệu** (Type hints) của tham số đầu vào và giá trị trả về (nếu có).

*Ví dụ:*
```python
def process_data(user_id: int, status: str = "active") -> bool:
    pass
```
Chữ ký của hàm trên là: `process_data(user_id: int, status: str = 'active') -> bool`.

### 3.2 Tại sao cần phải quan tâm đến Signature?

#### A. Là một bản hợp đồng thiết kế (Interface Contract)
Signature định nghĩa cách mà bên ngoài giao tiếp với hàm của bạn. Nó quy định chính xác caller cần truyền vào những gì và nhận lại kết quả dạng nào.

#### B. Hỗ trợ IDE, Static Analyzer & Tự động hoàn thành (Autocomplete)
Python là ngôn ngữ kiểu động (dynamically typed). Việc cung cấp signature rõ ràng cùng với Type Hint giúp các công cụ như VS Code, PyCharm, MyPy:
* Cảnh báo lỗi sai kiểu dữ liệu ngay khi viết code (trước khi chạy chương trình).
* Gợi ý tự động (autocomplete) chính xác tên thuộc tính/hành vi.

#### C. Phục vụ Meta-programming (Lập trình siêu dữ liệu) và Tự động hóa
Nhiều thư viện hiện đại của Python (FastAPI, Pydantic, Click, Typer, v.v.) dựa vào việc đọc và phân tích signature ở runtime (thông qua module `inspect` của Python) để tự động hóa nhiều tác vụ phức tạp:
* **FastAPI/Pydantic**: Đọc signature của hàm xử lý request để tự động kiểm tra tính hợp lệ của dữ liệu (validation), tự động parse kiểu dữ liệu, và sinh ra tài liệu API (Swagger UI).
* **Dependency Injection (DI)**: Đọc tham số trong signature để tự động truyền đúng đối tượng cần thiết.

*Ví dụ phân tích signature bằng thư viện `inspect`:*
```python
import inspect

def greet(name: str, age: int = 20) -> str:
    return f"Hello {name}, you are {age}."

sig = inspect.signature(greet)
print(sig)  # Output: (name: str, age: int = 20) -> str

for param in sig.parameters.values():
    print(f"Name: {param.name}, Type: {param.annotation}, Default: {param.default}")
```

#### D. Tương thích Signature trong Ghi đè phương thức (Override)
Khi lớp con ghi đè một phương thức của lớp cha, nó nên tuân thủ **Nguyên lý thay thế Liskov (Liskov Substitution Principle - LSP)**: 
> Chữ ký phương thức của lớp con phải **tương thích** hoặc **rộng hơn** chữ ký của lớp cha để đảm bảo bất kỳ nơi nào chạy được lớp cha thì cũng chạy được lớp con mà không bị lỗi.

---

## Tài liệu tham khảo chính thức (Official Documentation)
* [Python Tutorial - More on Defining Functions (Arguments, /, *)](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)
* [Python Language Reference - Function Definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
* [Python Standard Library - `inspect` Module (Signature Introspection)](https://docs.python.org/3/library/inspect.html#introspecting-callables-with-the-signature-object)
* [PEP 570 - Python Positional-Only Parameters](https://peps.python.org/pep-0570/)
* [PEP 3102 - Keyword-Only Arguments](https://peps.python.org/pep-3102/)

---

[12_arguments_and_signatures_examples.py](file:///home/linh/VDX-intern/python-deep-notes/examples/12_arguments_and_signatures_examples.py)
