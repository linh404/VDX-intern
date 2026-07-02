# Inheritance - Take Notes

Ghi chú cá nhân về lập trình hướng đối tượng (OOP) trong Python.

---

## 1. Class & Object

* **Class**: Bản thiết kế, là khuôn để tạo ra đối tượng.
* **Đối tượng (Object / Instance)**: Một thể hiện (instance) cụ thể được tạo ra từ Class.
* **Cấu trúc đối tượng**: Gồm **thuộc tính** (thường được tạo trong hàm khởi tạo `__init__`) và **hành vi** (các hàm trong một Class).

---

## 2. Namespace

* **Định nghĩa**: Vùng không gian ánh xạ tên giúp Python không bị nhầm lẫn nếu như có trùng tên.
  * *Ví dụ*: Có 2 hàm `connect()` trùng tên, nhưng 1 hàm ở module `api.py` còn 1 hàm ở module `database.py`. Nhờ namespace, 2 module này không bị conflict với nhau. Ở đây nó thuộc về cấp global space. Với Python, 1 đối tượng có hành vi thì đều thuộc về 1 namespace.
* **4 cấp Scope (Quy tắc LEGB)** từ bé đến lớn:
  * `local`: Trong nội bộ 1 hàm.
  * `enclosing`: Hàm trong hàm.
  * `global`: Cả 1 module.
  * `built-in`: Có sẵn, không cần import, cứ gọi là có (Cấp cao nhất của Python).

> [!IMPORTANT]
> **Quy tắc gọi hàm trong Class**:
> Trong 1 class, có hàm `A` và hàm `B`. Nếu hàm `B` mà gọi hàm `A` thì cần phải dùng `self.A()`. 
> *Lý do*: Theo quy tắc namespace LEGB, hàm `B` sẽ gọi đến local trước (tức là tìm trong hàm `B` có hàm `A` nào không) $\rightarrow$ báo lỗi nếu không thấy. Bản chất của class **không có tính chất enclosing scope** đối với các hàm con bên trong nó, nên phải dùng `self.A()` để trỏ qua namespace của đối tượng.

---

## 3. Hàm `__init__`, `self` và Biến Private

* **Hàm `__init__()`**: Constructor của class, tự động gọi ngay khi tạo ra 1 đối tượng từ class đó.
* **Cách tạo nhanh constructor**: Sử dụng thư viện `dataclass`:
  ```python
  from dataclasses import dataclass 
  
  @dataclass 
  class Employee: 
      name: str 
      dept: str 
      salary: int 
  ```
* **Tham số `self`**: Tương tự như `this` trong các ngôn ngữ khác, là tham số bắt buộc truyền đầu tiên vào mỗi instance method của class.
  * Có thể không truyền với các hàm `@staticmethod`.
  * Thay bằng `cls` đối với các hàm `@classmethod`.
* **Biến Private & Protected (Quy ước)**:
  * `_protected_var` (1 dấu gạch dưới): Báo hiệu biến nội bộ (protected), không nên truy cập trực tiếp từ ngoài Class.
  * `__private_var` (2 dấu gạch dưới): Python kích hoạt cơ chế name mangling để đổi tên biến này $\rightarrow$ tránh bị ghi đè bởi class con (private).

---

## 4. Kế thừa

* **Định nghĩa**: Thừa hưởng các đặc điểm và hành vi của class Cha, đồng thời chuyên biệt hóa một vài đặc điểm/hành vi của class Con.

```python
class LopCha:
    # Các thuộc tính và phương thức của lớp cha
    pass

class LopCon(LopCha):
    # Lớp con kế thừa tất cả từ LopCha
    pass
```

---

## 5. Super, MRO và Arguments (`*args` và `**kwargs`)

### 5.1 Super & MRO (Method Resolution Order)
* **`super()`**: Như một object chuyển tiếp được áp dụng trong kế thừa, nó không xử lý trực tiếp mà đưa việc tìm các thuộc tính và hành vi cho MRO.
  * Bình thường khi sử dụng lệnh `super()` thì đó là cú pháp zero-argument đặc biệt của super do Python quy định, không phải default parameter.
  * Nếu truyền tham số cho super: `super(Class_mốc, self_hoặc_cls)` $\rightarrow$ Python bắt đầu tìm phương thức từ class đứng ngay sau `Class_mốc` đó trong chuỗi MRO.
* **MRO**: Thứ tự tìm thuộc tính và hành vi trong cây kế thừa.

*Ví dụ dễ hiểu:*
```python
class A:
    def run(self):
        print("A.run")

class B(A):
    def run(self):
        print("B.run")
        super().run()

class C(B):
    def run(self):
        print("C.run")
        super().run()

obj = C()
obj.run()
```
*Kết quả:*
```text
C.run
B.run
A.run
```
*Giải thích*: MRO của `C` là: `C -> B -> A -> object`.
* Để đứng ở `C` mà bỏ qua `B` để gọi thẳng `A`, ta viết: `super(B, self).run()` (vì nó tìm từ sau class `B`).
* Nếu gọi `super(A, self).run()` thì nó tìm sau `A` (là class `object`).

### 5.2 Đa kế thừa & Diamond Problem
* Thứ tự MRO trong đa kế thừa được áp dụng từ trái sang phải.

*Ví dụ:*
```python
class A:
    def run(self):
        print("A.run")

class B(A):
    def run(self):
        print("B.run")
        super().run()

class C(A):
    def run(self):
        print("C.run")
        super().run()

class D(B, C):
    def run(self):
        print("D.run")
        super().run()
```
*Giải thích*: Chuỗi MRO lúc này là: `D -> B -> C -> A -> object`.
* Vì `B` đứng trước `C` trong tham số kế thừa của `D`.
* Lúc này khi `B.run()` gọi `super().run()`, nó sẽ gọi đến `C.run()` chứ không gọi thẳng lên `A`.
* Đây là cơ chế **Đa kế thừa hợp tác (Cooperative Multiple Inheritance)** để đảm bảo duyệt qua tất cả các class cha đúng 1 lần từ thằng kế thừa cuối cùng.

### 5.3 Tham số `*args` và `**kwargs`
* Python có 2 cách truyền tham số: Cố định vị trí (positional argument) hoặc truyền theo tên (keyword argument).

*Ví dụ:*
```python
def func(a, b, *args, **kwargs):
    print("a =", a)
    print("b =", b)
    print("args =", args)
    print("kwargs =", kwargs)

func(1, 2, 3, 4, x=10, y=20)
```
* **`1, 2`**: Tương ứng với tham số vị trí `a, b`.
* **`3, 4`**: Các tham số vị trí dư thừa, tự động gom vào `args` dưới dạng **tuple**.
* **`x=10, y=20`**: Các tham số keyword truyền vào dưới dạng `key=value`, tự động gom vào `kwargs` dưới dạng **dict**.

---

[02_inheritance_examples.py](file:///home/linh/intern-training/python-deep-notes/examples/02_inheritance_examples.py)
