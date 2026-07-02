# Iterable & Iterator - Take Notes

Ghi chú về Iterable, Iterator, cơ chế duyệt vòng lặp và các hàm `iter()`, `next()` trong Python.

---

## 1. Khái niệm cơ bản

* **Iterable**: Là bất kỳ đối tượng nào có thể duyệt qua được bằng vòng lặp `for` (ví dụ: `list`, `tuple`, `str`, `set`, `dict`, `range`, file object...).
* **Iterator**: Là đối tượng thực sự thực hiện việc duyệt, lưu giữ trạng thái hiện tại (biết mình đang ở đâu) và trả về phần tử tiếp theo khi được gọi qua hàm `next()`.

> **Phân biệt nhanh**: `list` là một **iterable**, nhưng bản thân nó không phải là một **iterator**. Không thể gọi trực tiếp `next(list)`.

---

## 2. Hàm `iter()` và `next()`

* **`iter(iterable)`**: Tạo ra một đối tượng `iterator` từ `iterable` truyền vào.
* **`next(iterator)`**: Trả về phần tử tiếp theo trong chuỗi phần tử của `iterator`.
* **Cơ chế StopIteration**: Khi `iterator` đã duyệt hết phần tử, cuộc gọi `next()` tiếp theo sẽ raise ngoại lệ `StopIteration` để báo hiệu dừng lại.

---

## 3. Cơ chế hoạt động của vòng lặp `for`

Khi ta viết:
```python
for item in iterable:
    # xử lý item
```

Dưới cấu trúc của Python, vòng lặp hoạt động tương tự như sau:
```python
# 1. Tạo iterator từ iterable
it = iter(iterable)

# 2. Vòng lặp vô hạn để lấy từng phần tử
while True:
    try:
        item = next(it)
        # xử lý item
    except StopIteration:
        # 3. Kết thúc khi hết phần tử
        break
```

---

## 4. Đặc điểm của Iterator

* **Có trạng thái (Stateful)**: Nhớ vị trí hiện tại của con trỏ duyệt.
* **Một chiều**: Iterator chỉ đi tiếp về phía trước, không thể đi lùi hay tự động quay lại từ đầu. Nếu muốn duyệt lại, bắt buộc phải tạo một iterator mới bằng hàm `iter()`.

---

## 5. Ví dụ cần xem

[10_iterable_examples.py](file:///home/linh/intern-training/python-deep-notes/examples/10_iterable_examples.py)
