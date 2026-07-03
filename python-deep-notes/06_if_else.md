# If Else - Take Notes

Ghi chú về `if`, `elif`, `else`, cơ chế chọn nhánh và các trường hợp dễ gây lỗi logic khi viết khối điều kiện trong Python.

---

## 1. Khái niệm cơ bản

* **`if`**: Kiểm tra điều kiện đầu tiên.
* **`elif`**: Kiểm tra điều kiện tiếp theo nếu các điều kiện phía trên sai.
* **`else`**: Chạy khi tất cả điều kiện phía trên đều sai.

Ví dụ:

```python
score = 85

if score >= 90:
    print("Xuất sắc")
elif score >= 80:
    print("Giỏi")
else:
    print("Bình thường")
```

---

## 2. Cơ chế hoạt động

`if / elif / else` là **một khối điều kiện độc lập**, được kiểm tra **tuần tự từ trên xuống dưới**.

Trong cả khối này, chỉ có **một case duy nhất** được chạy.

```python
if condition_1:
    # case 1
elif condition_2:
    # case 2
elif condition_3:
    # case 3
else:
    # case mặc định
```

Cơ chế:

* Nếu `condition_1` đúng, chạy case 1 rồi thoát khỏi cả khối.
* Nếu `condition_1` sai, Python mới kiểm tra tiếp `condition_2`.
* Nếu gặp điều kiện đúng đầu tiên, Python chạy nhánh đó và bỏ qua toàn bộ nhánh phía sau.
* `else` chỉ chạy khi toàn bộ `if` và `elif` phía trên đều sai.

> [!NOTE]
> Hiểu nhanh: Check từ trên xuống, đúng nhánh nào đầu tiên thì vào nhánh đó, sau đó thoát khỏi cả khối.

---

## 3. Điều kiện hẹp phải đặt trước điều kiện rộng

Khi nhiều case có thể cùng đúng, phải đặt case cụ thể hơn lên trước.

Sai:

```python
age = 70

if age >= 18:
    print("Người lớn")
elif age >= 60:
    print("Người già")
```

Kết quả:

```python
Người lớn
```

Vì `age >= 18` đúng trước, nên Python không kiểm tra tiếp `age >= 60`.

Đúng:

```python
age = 70

if age >= 60:
    print("Người già")
elif age >= 18:
    print("Người lớn")
else:
    print("Trẻ em")
```

Quy tắc:

```text
Case hẹp / đặc biệt / cụ thể đặt trước.
Case rộng / tổng quát đặt sau.
```

---

## 4. `if / elif / else` khác nhiều `if` riêng

`if / elif / else` chỉ chạy **một nhánh đầu tiên đúng**.

```python
score = 95

if score >= 90:
    print("Xuất sắc")
elif score >= 80:
    print("Giỏi")
elif score >= 50:
    print("Đạt")
```

Kết quả:

```python
Xuất sắc
```

Còn nhiều `if` riêng thì mỗi `if` là một khối độc lập.

```python
score = 95

if score >= 90:
    print("Xuất sắc")

if score >= 80:
    print("Giỏi")

if score >= 50:
    print("Đạt")
```

Kết quả:

```python
Xuất sắc
Giỏi
Đạt
```

> [!TIP]
> Dùng `if / elif / else` khi chỉ muốn chọn một nhánh.
> Dùng nhiều `if` riêng khi nhiều nhánh có thể cùng chạy.

---

## 5. Trùng case làm nhánh phía sau chết

Ví dụ:

```python
choice = "3"

if choice == "3":
    print("Tính tổng kho")
elif choice == "3":
    print("Tìm sản phẩm")
```

Kết quả:

```python
Tính tổng kho
```

Nhánh `elif choice == "3"` phía sau không bao giờ chạy.

Case này hay gặp trong menu:

```python
if choice == "1":
    add_product(products)
elif choice == "2":
    list_products(products)
elif choice == "3":
    calculate_inventory_value(products)
elif choice == "3":
    find_product(products)
else:
    print("Lựa chọn không hợp lệ")
```

Ở đây option `"3"` thứ hai là lỗi logic.

Đúng hơn:

```python
if choice == "1":
    add_product(products)
elif choice == "2":
    list_products(products)
elif choice == "3":
    calculate_inventory_value(products)
elif choice == "4":
    find_product(products)
else:
    print("Lựa chọn không hợp lệ")
```

---

## 6. `else` thuộc về `if` gần nhất cùng cấp indent

Ví dụ:

```python
is_login = True
is_admin = False

if is_login:
    if is_admin:
        print("Admin")
    else:
        print("User thường")
else:
    print("Chưa đăng nhập")
```

Ở đây:

```python
else:
    print("User thường")
```

thuộc về:

```python
if is_admin:
```

Không phải thuộc về:

```python
if is_login:
```

Vì `else` sẽ ăn theo `if` gần nhất có cùng cấp thụt lề.

---

## 7. Các trường hợp dễ gây lỗi logic

### 7.1. Dùng nhiều `if` riêng khi đáng ra phải dùng `elif`

```python
score = 95

if score >= 90:
    print("Xuất sắc")
if score >= 80:
    print("Giỏi")
if score >= 50:
    print("Đạt")
```

Kết quả:

```python
Xuất sắc
Giỏi
Đạt
```

Nếu chỉ muốn in một kết quả, cách này sai logic.

Đúng hơn:

```python
score = 95

if score >= 90:
    print("Xuất sắc")
elif score >= 80:
    print("Giỏi")
elif score >= 50:
    print("Đạt")
```

---

### 7.2. Trùng case trong cùng một khối

```python
choice = "3"

if choice == "3":
    print("A")
elif choice == "3":
    print("B")
```

Không lỗi chương trình, nhưng nhánh `"B"` không bao giờ chạy.

---

### 7.3. Đặt `else` sai cấp thụt lề

```python
is_login = True
is_admin = False

if is_login:
    if is_admin:
        print("Admin")
    else:
        print("User thường")
else:
    print("Chưa đăng nhập")
```

Nếu không để ý indent, dễ hiểu nhầm `else: print("User thường")` là của `if is_login`.

Thực tế nó thuộc về:

```python
if is_admin:
```

Vì vậy khi có `if` lồng nhau, phải nhìn đúng cấp thụt lề.

---

### 7.4. Dùng `else` quá sớm làm mất các case cần kiểm tra tiếp

Sai:

```python
choice = "2"

if choice == "1":
    print("Thêm sản phẩm")
else:
    print("Lựa chọn không hợp lệ")
```

Nếu sau này có thêm option `"2"`, `"3"`, `"4"` mà vẫn để `else` ngay sau option `"1"` thì các option khác sẽ bị coi là không hợp lệ.

Đúng hơn:

```python
choice = "2"

if choice == "1":
    print("Thêm sản phẩm")
elif choice == "2":
    print("Danh sách sản phẩm")
elif choice == "3":
    print("Tính tổng kho")
else:
    print("Lựa chọn không hợp lệ")
```
