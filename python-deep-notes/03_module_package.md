# Module & Package - Take Notes

Ghi chú cá nhân về cấu trúc mã nguồn, cơ chế import và quản lý namespace trong Python.

---

## 1. Bản chất

* **Module**: 
  * Là 1 file Python đơn lẻ (file `.py`).
  * Chứa các khai báo biến, hàm, class hoặc code chạy trực tiếp.
  * Tên file chính là tên module (ví dụ: `models.py` ứng với module `models`).
* **Package**:
  * Là 1 folder chứa nhiều module hoặc package con (subpackage).
  * Package và subpackage khác nhau ở cấp thư mục phân cấp, bản chất hoạt động là như nhau.
* **Cơ chế tìm kiếm module (`sys.path`)**:
  * Khi gọi lệnh `import`, Python tìm kiếm theo thứ tự trong danh sách `sys.path`:
    1. Thư mục hiện tại (chứa script đang chạy).
    2. Biến môi trường `PYTHONPATH` (nếu có).
    3. Standard Library (thư viện có sẵn của Python).
    4. Thư mục `site-packages` (thư viện bên thứ ba cài qua `pip`).
* **Regular Package vs Namespace Package**:
  * **Regular Package**: Thư mục chứa file `__init__.py`. Khi import package, `__init__.py` tự động chạy trước tiên để khởi tạo namespace cho package đó. Có thể để trống đối với python thuần.
  * **Namespace Package** (từ Python 3.3+): Không cần `__init__.py`. Dùng khi muốn phân chia các subpackage nằm ở nhiều folder vật lý/repo khác nhau nhưng chung 1 namespace gốc.

---

## 2. Nó giải quyết vấn đề gì?

* **Tránh xung đột tên (Namespace Isolation)**: Gom nhóm code giúp các hàm trùng tên ở các module khác nhau không đè lên nhau (ví dụ: `auth.services.login` và `crm.services.login`).
* **Khả năng tái sử dụng (Code Reusability)**: Đóng gói logic dùng chung vào module/package để dễ import sử dụng lại, tránh copy-paste code.
* **Tổ chức cấu trúc backend chuẩn**: Giúp chia nhỏ dự án thành nhiều tầng logic rõ ràng (Model, Service, Controller...) làm base để học các framework lớn như FastAPI, Odoo, Django...

---

## 3. Luồng xử lý & Cơ chế Import

### 3.1 Hai kiểu Import cơ bản
* **`import module`**:
  * *Cách dùng*: `import math` $\rightarrow$ gọi qua namespace: `math.sqrt(4)`.
  * *Đặc điểm*: An toàn, tránh trùng tên, rõ ràng nguồn gốc hàm.
* **`from module import name`**:
  * *Cách dùng*: `from math import sqrt` $\rightarrow$ gọi trực tiếp: `sqrt(4)`.
  * *Đặc điểm*: Ngắn gọn nhưng dễ gây conflict tên trong file hiện tại. Có thể khắc phục bằng alias: `from math import sqrt as math_sqrt`.

### 3.2 Absolute Imports vs Relative Imports
* **Absolute Import (Import tuyệt đối)**: Dùng đường dẫn đầy đủ tính từ thư mục gốc của dự án.
  * *Ví dụ*: `from examples.module_package_demo.models import User`.
  * *Đặc điểm*: Rõ ràng, chạy ở bất kỳ file nào cũng hoạt động.
* **Relative Import (Import tương đối)**: Dùng dấu chấm (`.`) để trỏ tương đối từ vị trí module hiện tại.
  * `.` là thư mục hiện tại, `..` là thư mục cha.
  * *Ví dụ*: `from .models import User` hoặc `from ..utils import helper`.
  * *Lưu ý*: **Chỉ hoạt động khi nằm trong 1 Package**.

> [!WARNING]
> **Lỗi: `ImportError: attempted relative import with no known parent package`**
>
> * **Nguyên nhân**: Khi chạy trực tiếp file bằng `python3 path/to/file.py`, Python coi file đó là script độc lập (chạy với `__name__ = "__main__"`) nên không xác định được package cha của nó. Do đó các relative import bị lỗi.
> * **Cách khắc phục**:
>   1. Chạy từ thư mục gốc của dự án dưới dạng module bằng flag `-m`:
>      ```bash
>      # Đứng ở root folder (/home/linh/intern-training)
>      python3 -m python-deep-notes.examples.module_package_demo.main
>      ```
>   2. Thay relative import thành absolute import nếu file đó được thiết kế để chạy độc lập như script độc lập.

---

## 4. Các tính năng đặc biệt

### 4.1 Khối lệnh `if __name__ == "__main__"`
* **Cơ chế**:
  * Mỗi module khi chạy đều có một biến ẩn `__name__`.
  * Nếu chạy trực tiếp script: `__name__` được gán giá trị `"__main__"`.
  * Nếu bị import từ file khác: `__name__` được gán bằng tên module (ví dụ: `"main"`).
* **Ứng dụng**:
  ```python
  def main():
      # logic chạy thử/test
      pass
  
  if __name__ == "__main__":
      main()
  ```
  Giúp thiết kế 1 file vừa làm script chạy độc lập, vừa làm module để import mà không bị tự động chạy các đoạn code test khi import.

### 4.2 Sử dụng nâng cao với `__init__.py` & Biến `__all__`
* **Exposing (Phơi bày API)**:
  * Cho phép import trước các class/hàm quan trọng lên cấp package trong file `__init__.py`.
  * *Ví dụ*: Trong `__init__.py` của package `demo` viết:
    ```python
    from .models import User
    from .services import UserService
    ```
    Bên ngoài chỉ cần dùng: `from demo import User, UserService` (không cần đi sâu vào `from demo.models import User`).
* **Biến `__all__`**:
  * Là 1 list các chuỗi quy định những gì được export ra ngoài khi dùng wildcard import `from module import *`.
  * *Ví dụ*:
    ```python
    # file models.py
    __all__ = ['User']  # Chỉ export User khi dùng import *
    class User: pass
    class Admin: pass
    ```
  * *Lời khuyên*: Hạn chế dùng `from module import *` để tránh ô nhiễm namespace.

---

## 5. Ví dụ cần xem

* [Thư mục demo: module_package_demo](file:///home/linh/intern-training/python-deep-notes/examples/module_package_demo)
* [main.py](file:///home/linh/intern-training/python-deep-notes/examples/module_package_demo/main.py)
