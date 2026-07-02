# Python Collection Notes

Ghi chú ngắn gọn về lý thuyết và cách sử dụng 4 kiểu dữ liệu tập hợp cốt lõi trong Python.

---

## 1. Tổng quan 4 kiểu Collection

```text
+-------+----------+----------+-------------+----------------+--------------------------+
| Type  | Có thứ tự | Sửa được | Cho trùng   | Truy cập bằng  | Mục đích chính           |
+-------+----------+----------+-------------+----------------+--------------------------+
| list  | Có       | Có       | Có          | index          | Lưu danh sách thay đổi   |
| tuple | Có       | Không    | Có          | index          | Lưu hằng số, trả về nhiều|
| dict  | Có       | Có       | Key không   | key            | Lưu dạng Key-Value       |
| set   | Không    | Có       | Không       | membership     | Lọc trùng, check tồn tại |
+-------+----------+----------+-------------+----------------+--------------------------+
```

---

## 2. Lý thuyết chi tiết từng kiểu

### 2.1 List (Danh sách)
* **Khi nào dùng**: Cần lưu nhiều phần tử, cần giữ nguyên thứ tự, cho phép trùng lặp, cần thêm/sửa/xóa linh hoạt.
* **Thao tác cơ bản**:
  * **Duyệt**: `for item in lst:`
  * **Sửa**: `lst[index] = new_value`.
  * **Lọc**: Dùng List Comprehension `[x for x in lst if condition]` (Xem chi tiết tại [11_list_comprehension.md](file:///home/linh/VDX-intern/python-deep-notes/11_list_comprehension.md)).
* **Các phương thức (methods) hay dùng**:
  * `append(x)`: Thêm phần tử `x` vào cuối list.
  * `extend(iterable)`: Thêm các phần tử của `iterable` vào cuối list.
  * `insert(i, x)`: Chèn phần tử `x` vào index `i`.
  * `remove(x)`: Xóa phần tử đầu tiên có giá trị bằng `x` (gây lỗi `ValueError` nếu không tìm thấy).
  * `pop([i])`: Xóa và trả về phần tử tại index `i` (mặc định lấy ra phần tử cuối nếu không truyền `i`).
  * `clear()`: Xóa sạch toàn bộ phần tử trong list.
  * `index(x)`: Trả về index đầu tiên của phần tử bằng `x` (gây lỗi `ValueError` nếu không tìm thấy).
  * `count(x)`: Đếm số lần xuất hiện của phần tử `x` trong list.
  * `sort(key=None, reverse=False)`: Sắp xếp các phần tử của list tại chỗ (in-place).
  * `reverse()`: Đảo ngược các phần tử của list tại chỗ (in-place).

### 2.2 Tuple (Bộ dữ liệu cố định)
* **Khi nào dùng**: Dữ liệu cố định không muốn bị sửa đổi (đảm bảo tính toàn vẹn), trả về nhiều giá trị từ hàm.
* **Thao tác cơ bản**:
  * **Unpacking**: `a, b = (1, 2)`.
  * **Tuple 1 phần tử**: Bắt buộc phải có dấu phẩy đi kèm, ví dụ `x = (1,)` (nếu viết `x = (1)` thì Python sẽ coi là kiểu `int` đặt trong dấu ngoặc đơn).

### 2.3 Dict (Từ điển)
* **Khi nào dùng**: Lưu dữ liệu dưới dạng `key: value`, truy cập phần tử cực nhanh theo key.
* **Thao tác cơ bản**:
  * **Truy cập**: `d[key]` (báo lỗi `KeyError` nếu không có key) hoặc dùng `d.get(key, default_value)` (trả về `None` hoặc giá trị mặc định nếu key không tồn tại).
  * **Thêm/Sửa**: `d[key] = value` (chưa có thì thêm mới, đã có thì ghi đè).
  * **Xóa**: `d.pop(key)` hoặc `del d[key]`.
  * **Duyệt**: Duyệt keys (`for k in d:`), duyệt values (`for v in d.values():`), duyệt cả cặp (`for k, v in d.items():`).

### 2.4 Set (Tập hợp)
* **Khi nào dùng**: Loại bỏ phần tử trùng lặp (lọc trùng), kiểm tra sự tồn tại của phần tử nhanh chóng (`in`), thực hiện các phép toán tập hợp.
* **Thao tác cơ bản**:
  * **Lọc trùng**: `unique_set = set(lst)`.
  * **Kiểm tra tồn tại**: `if x in my_set:`.
  * **Các phép toán tập hợp (Set operations)**:
    * Phép trừ (hiệu): `set_a - set_b` (phần tử chỉ có ở A).
    * Phép và (giao): `set_a & set_b` (phần tử có ở cả A và B).
    * Phép hoặc (hợp): `set_a | set_b` (gộp chung cả hai).

---

## 3. Các cạm bẫy cần tránh (Gotchas)

### A. Mutable & Reference (Lỗi sao chép nông)
* `list`, `dict`, `set` là kiểu dữ liệu có thể thay đổi (mutable).
* Phép gán `b = a` chỉ tạo tham chiếu mới trỏ tới cùng một đối tượng.
* Muốn nhân bản độc lập, phải dùng `.copy()` (ví dụ `b = a.copy()`).

### B. Không sửa Collection khi đang duyệt trực tiếp
* Duyệt qua list/dict và dùng `remove()` hoặc `del` trực tiếp trên nó sẽ làm thay đổi độ dài, bỏ sót phần tử hoặc gây lỗi logic.
* **Cách khắc phục**: Tạo list/dict mới thông qua comprehension hoặc duyệt qua một bản sao của keys (`list(data.keys())`).

### C. Không dùng List/Dict làm Default Parameter cho hàm
* Giá trị mặc định của tham số (ví dụ: `def add(item, items=[])`) chỉ được khởi tạo **một lần duy nhất** khi định nghĩa hàm, dẫn đến việc dùng chung một list qua tất cả các cuộc gọi sau đó.
* **Cách khắc phục**: Dùng `items=None`, và khởi tạo `items = []` bên trong thân hàm.

---

[07_collection_examples.py](file:///home/linh/VDX-intern/python-deep-notes/examples/07_collection_examples.py)
