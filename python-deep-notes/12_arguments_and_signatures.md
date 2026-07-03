# Arguments Và Function Signatures

Ghi chú về cách Python truyền giá trị vào hàm, cách đọc function signature, và cách phân biệt đúng giữa `parameter`, `argument`, `*args`, `**kwargs`.

---

## 0. Parameter Và Argument

Trong Python cần tách rõ 2 khái niệm:

| Khái niệm | Nghĩa |
|---|---|
| Parameter | Tên biến nằm trong phần định nghĩa hàm |
| Argument | Giá trị thật sự được truyền vào khi gọi hàm |

Ví dụ:

```python
def greet(name, age):
    pass

greet("Linh", 20)
```

Trong đó:

```python
name, age       # parameters
"Linh", 20      # arguments
```

Nói ngắn gọn:

> Parameter là chỗ nhận. Argument là giá trị được đưa vào.

---

## 1. Argument Bình Thường

Argument bình thường là giá trị được truyền vào và khớp trực tiếp với parameter đã khai báo sẵn trong signature.

```python
def add(a, b):
    return a + b

add(2, 3)
```

Map ra:

```python
a = 2
b = 3
```

Có 2 cách truyền argument bình thường.

### 1.1 Positional Argument

Truyền theo vị trí.

```python
def create_user(name, age):
    print(name, age)

create_user("Linh", 20)
```

Map ra:

```python
name = "Linh"
age = 20
```

Với positional argument, thứ tự rất quan trọng.

### 1.2 Keyword Argument

Truyền theo tên parameter.

```python
def create_user(name, age):
    print(name, age)

create_user(age=20, name="Linh")
```

Map ra:

```python
name = "Linh"
age = 20
```

Keyword argument không phụ thuộc vào thứ tự, vì Python map theo tên.

---

## 2. `*args` Và `**kwargs`

`*args` và `**kwargs` không phải là một loại argument riêng.

Chính xác hơn:

- `*args` là một parameter đặc biệt dùng để gom các positional arguments còn dư.
- `**kwargs` là một parameter đặc biệt dùng để gom các keyword arguments còn dư.
- Tên `args` và `kwargs` chỉ là convention.
- Cái đặc biệt nằm ở dấu `*` và `**`.

---

## 3. `*args`

`*args` gom các positional arguments chưa được parameter cố định nào nhận vào một tuple.

```python
def demo(a, b, *args):
    print(a)
    print(b)
    print(args)

demo(1, 2, 3, 4)
```

Map ra:

```python
a = 1
b = 2
args = (3, 4)
```

Giải thích:

- `1` được gán cho `a`.
- `2` được gán cho `b`.
- `3`, `4` là positional arguments còn dư, nên bị gom vào `args`.

Lưu ý:

```python
def demo(*values):
    print(values)
```

Vẫn đúng. Vì tên `args` không bắt buộc. Nhưng trong Python người ta thường đặt là `args` cho dễ đọc.

---

## 4. `**kwargs`

`**kwargs` gom các keyword arguments chưa khớp với parameter cố định nào vào một dictionary.

```python
def demo(a, b, **kwargs):
    print(a)
    print(b)
    print(kwargs)

demo(a=1, b=2, name="Linh", age=20)
```

Map ra:

```python
a = 1
b = 2
kwargs = {
    "name": "Linh",
    "age": 20,
}
```

Keyword nào có parameter nhận riêng thì không rơi vào `kwargs`.

```python
def demo(a, b, **kwargs):
    print(a)
    print(b)
    print(kwargs)

demo(b=1, a=2)
```

Map ra:

```python
a = 2
b = 1
kwargs = {}
```

Vì `a` và `b` đã có chỗ nhận riêng trong signature, nên chúng không bị đẩy vào `kwargs`.

Chỉ keyword lạ mới rơi vào `kwargs`.

```python
demo(b=1, a=2, x=10, y=20)
```

Map ra:

```python
a = 2
b = 1
kwargs = {
    "x": 10,
    "y": 20,
}
```

---

## 5. Thứ Tự Parameter Trong Function Signature

Dạng dễ nhớ:

```python
def func(a, b=10, *args, c, d=20, **kwargs):
    pass
```

Thứ tự:

| Nhóm | Ví dụ | Ý nghĩa |
|---|---|---|
| Parameter cố định | `a`, `b=10` | Nhận argument bình thường |
| Positional còn dư | `*args` | Gom positional arguments còn lại |
| Keyword-only parameter | `c`, `d=20` | Bắt buộc truyền bằng tên |
| Keyword còn dư | `**kwargs` | Gom keyword arguments còn lại |

Ví dụ:

```python
def demo(a, b, *args, c, **kwargs):
    print(a)
    print(b)
    print(args)
    print(c)
    print(kwargs)

demo(1, 2, 3, 4, c=5, name="Linh")
```

Map ra:

```python
a = 1
b = 2
args = (3, 4)
c = 5
kwargs = {"name": "Linh"}
```

Vì sao phải là `c=5` mà không phải `5`?

Vì `c` đứng sau `*args`, nên `c` là keyword-only parameter. Sau khi gặp `*args`, Python sẽ gom hết positional arguments còn dư vào `args`.

Nếu gọi:

```python
demo(1, 2, 3, 4, 5, name="Linh")
```

Python sẽ hiểu:

```python
a = 1
b = 2
args = (3, 4, 5)
```

Và `c` vẫn chưa có giá trị, nên sẽ lỗi.

---

## 6. Vì Sao `**kwargs` Phải Đứng Cuối?

`**kwargs` có nghĩa là gom tất cả keyword arguments còn lại.

Vì nó đã gom phần còn lại, nên sau `**kwargs` không thể còn parameter nào nữa.

Sai:

```python
def demo(**kwargs, a):
    pass
```

Đúng:

```python
def demo(a, **kwargs):
    pass
```

Chốt:

> `*args` đứng trước `**kwargs`. `**kwargs` phải đứng cuối.

---

## 7. Dấu `/` Và `*` Trong Signature

Khi kết hợp cả `/` và `*` trong cùng một function signature, Python sẽ phân chia các parameter làm 3 vùng rõ rệt (dấu `/` phải luôn đứng trước `*`):

```python
def func(positional_only, /, positional_or_keyword, *, keyword_only):
    pass
```

| Vị trí parameter | Phân loại | Quy tắc truyền argument |
|---|---|---|
| Đứng **trước** dấu `/` | **Positional-only** | Bắt buộc truyền theo đúng vị trí, cấm truyền bằng tên. |
| Đứng **giữa** `/` và `*` | **Positional-or-Keyword** | Tự do, truyền theo vị trí hay bằng tên đều được. |
| Đứng **sau** dấu `*` | **Keyword-only** | Bắt buộc truyền bằng tên, cấm truyền theo vị trí. |

### Ví dụ minh họa:

```python
def mix_demo(a, /, b, *, c):
    print(f"a={a}, b={b}, c={c}")
```

- **Các cách gọi ĐÚNG:**
  ```python
  mix_demo(1, 2, c=3)      # a vị trí (1), b vị trí (2), c tên (c=3)
  mix_demo(1, b=2, c=3)    # a vị trí (1), b tên (b=2), c tên (c=3)
  ```

- **Các cách gọi SAI (Gây lỗi TypeError):**
  ```python
  mix_demo(a=1, b=2, c=3)  # Lỗi! 'a' đứng trước / nên không được truyền bằng tên.
  mix_demo(1, 2, 3)        # Lỗi! 'c' đứng sau * nên không được truyền bằng vị trí.
  ```

---

## 8. Positional-only Parameter

Parameter đứng trước dấu `/` chỉ được truyền bằng vị trí, không được truyền bằng tên.

```python
def greet(name, /, greeting="Hello"):
    return f"{greeting}, {name}"

greet("Linh")
greet("Linh", greeting="Hi")
```

Sai:

```python
greet(name="Linh")
```

Mục đích:

- Caller không phụ thuộc vào tên parameter.
- Người viết hàm có thể đổi tên parameter mà ít làm hỏng code bên ngoài.
- Hay gặp trong built-in functions hoặc thư viện cần giữ API chặt.

---

## 9. Keyword-only Parameter

Parameter đứng sau `*args` hoặc sau dấu `*` bắt buộc phải truyền bằng tên.

```python
def calculate_tax(price, *, tax_rate):
    return price * tax_rate

calculate_tax(100, tax_rate=0.1)
```

Sai:

```python
calculate_tax(100, 0.1)
```

Mục đích:

- Ép caller viết rõ ý nghĩa argument.
- Tránh nhầm thứ tự với các tham số cấu hình quan trọng.
- Code dễ đọc hơn.

---

## 10. Function Signature Là Gì?

Function signature là phần mô tả cách một hàm được gọi.

Nó là phần "mặt ngoài" của hàm:

- Tên hàm.
- Danh sách parameters.
- Thứ tự parameters.
- Parameter nào bắt buộc.
- Parameter nào có default value.
- Parameter nào là positional-only.
- Parameter nào là keyword-only.
- Hàm có nhận `*args` hay `**kwargs` không.
- Type hints và return annotation nếu có.

Ví dụ:

```python
def process_data(user_id: int, status: str = "active") -> bool:
    pass
```

Có thể đọc signature là:

```python
process_data(user_id: int, status: str = "active") -> bool
```

Lưu ý:

> Type hints chỉ là gợi ý kiểu. Python không tự ép kiểu ở runtime nếu không có tool hoặc thư viện xử lý thêm.

---

## 11. Vì Sao Signature Quan Trọng?

### 11.1 Signature Là Hợp Đồng Gọi Hàm

```python
def add(a, b):
    return a + b
```

Signature cho biết hàm `add` cần 2 argument.

Đúng:

```python
add(1, 2)
```

Sai:

```python
add(1)
add(1, 2, 3)
```

---

### 11.2 Signature Quyết Định Cách Python Map Argument Vào Parameter

```python
def demo(a, b, **kwargs):
    pass

demo(b=1, a=2)
```

Python map theo tên:

```python
a = 2
b = 1
kwargs = {}
```

Chỉ keyword lạ mới rơi vào `kwargs`:

```python
demo(b=1, a=2, x=3)
```

Map ra:

```python
a = 2
b = 1
kwargs = {"x": 3}
```

---

### 11.3 Signature Quan Trọng Khi Override Method

Khi class con override method của class cha, signature nên tương thích với method gốc.

```python
class Parent:
    def write(self, vals):
        pass


class Child(Parent):
    def write(self, vals):
        return super().write(vals)
```

Nếu override sai:

```python
class Child(Parent):
    def write(self):
        pass
```

Khi code bên ngoài gọi:

```python
obj.write({"name": "Linh"})
```

Sẽ lỗi vì method con không nhận `vals`.

Trong Odoo, điều này rất quan trọng vì override method xảy ra liên tục.

---

## 12. Dùng `*args`, `**kwargs` Khi Override

Khi muốn giữ method con linh hoạt với method cha, có thể dùng:

```python
class Child(Parent):
    def some_method(self, *args, **kwargs):
        result = super().some_method(*args, **kwargs)
        return result
```

Ý nghĩa:

- `*args` nhận positional arguments còn dư.
- `**kwargs` nhận keyword arguments còn dư.
- Khi gọi `super()`, `*args` bung tuple thành positional arguments.
- Khi gọi `super()`, `**kwargs` bung dict thành keyword arguments.

Cần phân biệt:

```python
def some_method(self, *args, **kwargs):
    pass
```

Trong định nghĩa hàm:

- `*args` gom positional arguments.
- `**kwargs` gom keyword arguments.

Còn khi gọi hàm:

```python
super().some_method(*args, **kwargs)
```

Thì:

- `*args` bung tuple ra.
- `**kwargs` bung dict ra.

---

## 13. Dạng Signature Đầy Đủ

Dạng đầy đủ nhất:

```python
def func(pos_only, /, pos_or_kw, *args, kw_only, **kwargs):
    pass
```

Có thể đọc như sau:

| Vị trí | Loại parameter |
|---|---|
| Trước `/` | Chỉ truyền bằng vị trí |
| Giữa `/` và `*args` hoặc `*` | Truyền bằng vị trí hoặc bằng tên |
| `*args` | Gom positional arguments còn dư |
| Sau `*args` hoặc sau `*` | Chỉ truyền bằng keyword |
| `**kwargs` | Gom keyword arguments còn dư |

Dạng thực tế hay gặp:

```python
def func(a, b=1, *args, c, d=2, **kwargs):
    pass
```

Đọc là:

```python
a, b        # parameter cố định, nhận argument bình thường
*args       # gom positional arguments còn dư
c, d        # keyword-only parameters
**kwargs    # gom keyword arguments còn dư
```

---

## 14. Các Lỗi Hay Gặp

### 14.1 Gán Một Parameter Hai Lần

```python
def demo(a, b):
    pass

demo(1, a=2)
```

Lỗi vì Python đã map:

```python
a = 1
a = 2
```

---

### 14.2 Keyword Lạ Khi Không Có `**kwargs`

```python
def demo(a, b):
    pass

demo(a=1, b=2, c=3)
```

Lỗi vì `c` không có parameter nhận riêng và hàm cũng không có `**kwargs`.

---

### 14.3 Truyền Positional Cho Keyword-only Parameter

```python
def demo(a, *, b):
    pass

demo(1, 2)
```

Lỗi vì `b` đứng sau `*`, nên phải truyền bằng tên:

```python
demo(1, b=2)
```

---

## 15. Chốt Để Nói Với Leader

Nếu cần giải thích ngắn gọn:

> Argument là giá trị truyền vào khi gọi hàm. Parameter là tên biến trong định nghĩa hàm. `*args` và `**kwargs` không phải là argument riêng, mà là parameter đặc biệt. `*args` gom positional arguments còn dư thành tuple. `**kwargs` gom keyword arguments còn dư thành dict. Keyword argument nào khớp với parameter cố định thì được map vào parameter đó trước, không rơi vào `kwargs`. Chỉ keyword lạ mới vào `kwargs`. Sau `*args`, các parameter phía sau là keyword-only, nên phải truyền bằng tên.

---

## Tài Liệu Tham Khảo

- [Python Tutorial - More on Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)
- [Python Language Reference - Function Definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)
- [Python Standard Library - inspect.Signature](https://docs.python.org/3/library/inspect.html#inspect.Signature)
- [PEP 570 - Python Positional-Only Parameters](https://peps.python.org/pep-0570/)
- [PEP 3102 - Keyword-Only Arguments](https://peps.python.org/pep-3102/)
