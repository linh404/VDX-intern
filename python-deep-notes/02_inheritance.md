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

## 4. Kế thừa (Inheritance) & Ghi đè (Override)

* **Định nghĩa**: Thừa hưởng các đặc điểm và hành vi của class Cha, đồng thời chuyên biệt hóa một vài đặc điểm/hành vi của class Con.

```python
class LopCha:
    # Các thuộc tính và phương thức của lớp cha
    pass

class LopCon(LopCha):
    # Lớp con kế thừa tất cả từ LopCha
    pass
```

### 4.1 Ghi đè phương thức (Method Overriding)
Ghi đè phương thức xảy ra khi lớp con định nghĩa lại một phương thức đã có ở lớp cha (cùng tên). Khi ta gọi phương thức đó trên đối tượng của lớp con, Python sẽ thực thi phiên bản của lớp con.

Có hai kiểu ghi đè logic chính:

#### A. Ghi đè hoàn toàn logic (Complete Overriding)
Lớp con thay thế hoàn toàn hành vi của lớp cha và **không** gọi lại phương thức của lớp cha.
* **Sử dụng khi**: Lớp con muốn định nghĩa lại hoàn toàn cách hoạt động vì logic của lớp cha không còn phù hợp.
* **Ví dụ**:
  ```python
  class Animal:
      def make_sound(self):
          return "Some generic sound"

  class Dog(Animal):
      def make_sound(self):
          return "Woof woof"  # Thay thế hoàn toàn, không gọi Animal.make_sound
  ```

#### B. Kế thừa và mở rộng logic (Extending/Cooperative Logic)
Lớp con ghi đè phương thức của lớp cha nhưng vẫn muốn sử dụng lại (kế thừa) logic cũ, sau đó bổ sung thêm logic riêng của lớp con.
* **Cách thực hiện**: Dùng `super().tên_phương_thức()` để gọi logic của lớp cha.
* **Sử dụng khi**: Muốn tái sử dụng code của cha để tránh trùng lặp (DRY principle), chỉ viết thêm phần logic chuyên biệt của con.
* **Ví dụ với hàm khởi tạo `__init__` (Trường hợp phổ biến nhất)**:
  ```python
  class Employee:
      def __init__(self, name, salary):
          self.name = name
          self.salary = salary

  class Manager(Employee):
      def __init__(self, name, salary, department):
          # Gọi constructor lớp cha để khởi tạo name và salary (kế thừa logic)
          super().__init__(name, salary)
          # Khởi tạo thuộc tính riêng của Manager (mở rộng logic)
          self.department = department
  ```
* **Ví dụ với phương thức thông thường**:
  ```python
  class Order:
      def process(self):
          print("Checking inventory...")
          print("Calculating total...")

  class PromotionalOrder(Order):
      def process(self):
          # Chạy logic xử lý đơn hàng cơ bản của lớp cha trước
          super().process()
          # Thêm logic áp dụng mã giảm giá riêng của đơn hàng khuyến mãi
          print("Applying discount code...")
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

### 5.3 Nỗi đau Đa Kế thừa & Vấn đề truyền tham số (The Pain of Multiple Inheritance)
Đa kế thừa trong Python rất mạnh mẽ nhờ MRO, nhưng nó cũng mang lại một "nỗi đau" lớn liên quan đến việc truyền tham số (Arguments) và sự tương thích của chữ ký hàm (Signature).

* **Vấn đề**: Trong chuỗi MRO của đa kế thừa hợp tác (Cooperative Multiple Inheritance), một lớp con gọi `super().__init__(...)` không gọi trực tiếp cha của nó, mà gọi lớp tiếp theo trong chuỗi MRO (có thể là một lớp anh em/lớp khác cùng cấp).
* **Hậu quả**: Nếu các lớp trong chuỗi MRO đòi hỏi các tham số khởi tạo khác nhau (khác Signature), việc truyền tham số sẽ bị lỗi (ví dụ: `TypeError: __init__() got an unexpected keyword argument...`) vì lớp tiếp theo không nhận các tham số đó.

*Ví dụ về lỗi:*
```python
class Base:
    def __init__(self):
        print("Base __init__")

class A(Base):
    def __init__(self, a):
        print(f"A __init__ with a={a}")
        super().__init__()

class B(Base):
    def __init__(self, b):
        print(f"B __init__ with b={b}")
        super().__init__()

class C(A, B):
    def __init__(self, a, b):
        print("C __init__")
        # Gọi super() của C (là A) và truyền cả a và b?
        # A chỉ nhận `a`, nếu truyền `b` vào super() thì A sẽ báo lỗi hoặc nếu A chuyển tiếp `b` sang B thông qua super() thì cách viết sẽ cực kỳ rắc rối.
        super().__init__(a) # B sẽ không bao giờ nhận được b!
```

* **Giải pháp**:
  1. Sử dụng `*args` và `**kwargs` ở tất cả các lớp trong cây kế thừa để gom và chuyển tiếp các tham số dư thừa (tuy nhiên cách này làm signature của hàm bị mất đi tính rõ ràng).
  2. Hạn chế tối đa đa kế thừa có trạng thái (stateful multiple inheritance). Ưu tiên sử dụng **Mixin** (lớp bổ trợ chỉ chứa hành vi, không chứa trạng thái/thuộc tính) hoặc **Composition (Thành phần)** thay cho Đa kế thừa.

> [!TIP]
> Để hiểu rõ hơn về cách Python định nghĩa chữ ký hàm (Signature), các loại đối số (`*args`, `**kwargs`, positional-only `/`, keyword-only `*`) và cách thiết kế signature an toàn để giải quyết vấn đề truyền tham số này, hãy đọc tiếp tại:
> 👉 **[12_arguments_and_signatures.md](file:///home/linh/VDX-intern/python-deep-notes/12_arguments_and_signatures.md)**

---

## Tài liệu tham khảo chính thức (Official Documentation)
* [Python Tutorial - Inheritance & Multiple Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)
* [Python Built-in Functions - `super()`](https://docs.python.org/3/library/functions.html#super)
* [Python Method Resolution Order (MRO) - C3 Linearization](https://www.python.org/download/releases/2.3/mro/)

---

[02_inheritance_examples.py](file:///home/linh/VDX-intern/python-deep-notes/examples/02_inheritance_examples.py)
