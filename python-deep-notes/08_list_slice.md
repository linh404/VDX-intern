# List Slicing (Cắt lát danh sách)

Ghi chú chi tiết về cơ chế hoạt động, các mẹo sử dụng và những lưu ý quan trọng khi sử dụng tính năng List Slicing trong Python.

---

## 1. Bản chất của List Slicing

* **Định nghĩa**: Slicing là cơ chế trích xuất một phần của chuỗi (sequence) như list, tuple, string trong Python bằng cách sử dụng cú pháp:
  ```python
  sequence[start:stop:step]
  ```
* **Cơ chế sao chép**: Slicing trả về một **bản sao nông (shallow copy)** mới của sequence đó. Các thay đổi trên list con được cắt ra sẽ không ảnh hưởng trực tiếp đến list gốc (ngoại trừ trường hợp list chứa các object tham chiếu thay đổi được - mutable objects).
* **Các tham số mặc định**:
  * `start`: Vị trí bắt đầu cắt (mặc định là `0` nếu `step > 0`, hoặc `-1` nếu `step < 0`).
  * `stop`: Vị trí kết thúc cắt (không bao gồm phần tử ở chỉ số này). Mặc định là độ dài của list (`len(sequence)`) nếu `step > 0`, hoặc chỉ số trước phần tử đầu tiên (`-len(sequence)-1`) nếu `step < 0`.
  * `step`: Bước nhảy (mặc định là `1`). Không bao giờ được phép bằng `0` (sẽ gây ra `ValueError: slice step cannot be zero`).

### 1.1 Hoạt động với chỉ số âm (Negative Indexing)
Chỉ số âm cho phép đếm ngược từ cuối danh sách. Công thức chuyển đổi: `index_âm = index_dương - len(sequence)`.
*Ví dụ:*
```python
a = [10, 20, 30, 40, 50]
# Cắt từ phần tử thứ 2 từ cuối lên đến trước phần tử cuối cùng
print(a[-3:-1])  # [30, 40]
```

### 1.2 Không ném ra lỗi `IndexError` (Out-of-bounds slicing)
Khác với việc truy cập trực tiếp bằng một index (`a[i]`), slicing trong Python rất linh hoạt và tự động giới hạn chỉ số về trong phạm vi của danh sách mà không ném ra lỗi `IndexError`.
*Ví dụ:*
```python
a = [1, 2, 3]
print(a[0:100])  # [1, 2, 3] (Không báo lỗi)
print(a[10:20])   # [] (Trả về list rỗng)
```

---

## 2. Các vấn đề List Slicing giải quyết

### 2.1 Trích xuất danh sách con nhanh gọn
Thay vì phải dùng vòng lặp để duyệt qua các phần tử, slicing thực hiện tối ưu ở tầng C giúp lấy ra các phần tử nhanh hơn.

### 2.2 Đảo ngược danh sách (Reverse)
Sử dụng bước nhảy `-1`:
```python
a = [1, 2, 3, 4]
print(a[::-1])  # [4, 3, 2, 1]
```

### 2.3 Gán lát cắt (Slice Assignment)
Ta có thể thay đổi, chèn hoặc xóa các phần tử của list gốc trực tiếp thông qua gán giá trị cho một slice:

* **Thay thế một khoảng**:
  ```python
  a = [1, 2, 3, 4, 5]
  a[1:3] = [99, 100]
  print(a)  # [1, 99, 100, 4, 5]
  ```

* **Chèn thêm phần tử**:
  ```python
  a = [1, 2, 3]
  a[1:1] = [99, 100]  # Cắt rỗng tại index 1
  print(a)  # [1, 99, 100, 2, 3]
  ```

* **Xóa phần tử**:
  ```python
  a = [1, 2, 3, 4]
  a[1:3] = []
  # Hoặc dùng: del a[1:3]
  print(a)  # [1, 4]
  ```

---

## 3. Luồng xử lý và Đối tượng `slice` trong Python

### 3.1 Hàm khởi tạo `slice()`
Bản chất của cú pháp ngoặc vuông `a[start:stop:step]` là Python tự động tạo ra một đối tượng `slice` và truyền nó vào phương thức ma thuật của lớp.
* **Cú pháp**: `slice(stop)` hoặc `slice(start, stop, step)`
* **Ví dụ tương đương**:
  ```python
  a = [10, 20, 30, 40, 50]
  
  # Cách viết ngoặc vuông thông thường
  sub1 = a[1:4:2]
  
  # Cách viết dùng đối tượng slice tường minh
  my_slice = slice(1, 4, 2)
  sub2 = a[my_slice]
  
  print(sub1 == sub2)  # True
  ```

Khi ta chạy mã trên, Python sẽ chuyển đổi lời gọi thành:
* Lấy giá trị: `a.__getitem__(slice(1, 4, 2))`
* Gán giá trị: `a.__setitem__(slice(1, 4, 2), values)`
* Xóa giá trị: `a.__delitem__(slice(1, 4, 2))`

### 3.2 Lỗi gán lát cắt mở rộng (Extended Slice Assignment Error)
Khi sử dụng bước nhảy `step` khác `1` (Extended Slicing), Python đòi hỏi danh sách thay thế phải có **độ dài khớp chính xác** với số lượng phần tử bị thay thế bởi slice. Nếu không khớp sẽ báo lỗi `ValueError`.
*Ví dụ:*
```python
a = [1, 2, 3, 4, 5]
# Lát cắt này chọn ra 2 phần tử: index 0 (giá trị 1) và index 2 (giá trị 3)
# a[0:4:2] tương ứng với [1, 3]

# Thử gán list có 3 phần tử vào slice kích thước 2:
# a[0:4:2] = [10, 20, 30] 
# -> Lỗi: ValueError: attempt to assign sequence of size 3 to extended slice of size 2

# Gán đúng số lượng:
a[0:4:2] = [10, 20]  # Hợp lệ!
print(a)  # [10, 2, 20, 4, 5]
```

---

## Tài liệu tham khảo chính thức (Official Documentation)
* [Python Built-in Functions - `slice()`](https://docs.python.org/3/library/functions.html#slice)
* [Python Tutorial - Common Sequence Operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)

---

[13_list_slice_examples.py](file:///home/linh/VDX-intern/python-deep-notes/examples/13_list_slice_examples.py)
