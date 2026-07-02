# Python Core Semantics - Syntax Cheat Sheet

Cú pháp và ghi chú ngắn gọn về các đặc tính cốt lõi của Python.

---

## 1. Assignment & Binding (Gán & Tham chiếu)

```python
# Gán nhãn cho đối tượng (Binding)
x = [1, 2, 3]

# Tham chiếu chia sẻ (Shared Reference)
y = x  # y trỏ cùng đối tượng với x
y.append(4)  # Thay đổi qua y ảnh hưởng tới x (x lúc này là [1, 2, 3, 4])
```

---

## 2. Identity vs Equality (Đồng nhất vs Bằng nhau)

```python
# == : So sánh giá trị (Equality)
# is : So sánh địa chỉ vùng nhớ/ID (Identity)
a = [1, 2]
b = [1, 2]

a == b  # True
a is b  # False

# id() : Lấy địa chỉ vùng nhớ
id(a) == id(b)  # False
```

### Integer Caching (Small Int Caching)
```python
# Cache số nguyên từ -5 đến 256
x = 256
y = 256
x is y  # True

# Ngoài khoảng cache
m = 257
n = 257
m is n  # False (trên REPL) / True (nếu chạy cùng script do Compiler Optimization)
```

---

## 3. Mutability vs Immutability (Khả biến vs Bất biến)

```python
# Mutable (list, dict, set): Thay đổi không đổi id()
lst = [1, 2]
old_id = id(lst)
lst.append(3)
id(lst) == old_id  # True

# Immutable (int, float, str, tuple, bool): Thay đổi tạo id() mới
t = (1, 2)
old_id = id(t)
t += (3,)
id(t) == old_id  # False
```

---

## 4. Truthy & Falsy (Giá trị Chân lý)

```python
# Falsy: None, False, 0, 0.0, "", [], (), {}, set(), range(0)
# Truthy: Tất cả các giá trị khác

# Cú pháp định nghĩa Custom Truthiness:
class CustomObject:
    def __init__(self, is_valid):
        self.is_valid = is_valid
        
    def __bool__(self):
        return self.is_valid  # Trả về True/False

obj = CustomObject(False)
bool(obj)  # False
```

---

## 5. Scopes & Namespaces (Quy tắc LEGB)

```python
# Quy tắc tìm kiếm biến: Local -> Enclosing -> Global -> Built-in

glob_var = 10  # Global variable

def outer_func():
    outer_var = 20  # Enclosing variable
    
    def inner_func():
        # Sử dụng global để thay đổi biến toàn cục
        global glob_var
        glob_var = 15
        
        # Sử dụng nonlocal để thay đổi biến enclosing
        nonlocal outer_var
        outer_var = 25
        
        local_var = 5  # Local variable
        
    inner_func()
```

---

## 6. Tài liệu tham khảo ví dụ

[01_python_core_semantics_examples.py](file:///home/linh/intern-training/python-deep-notes/examples/01_python_core_semantics_examples.py)
