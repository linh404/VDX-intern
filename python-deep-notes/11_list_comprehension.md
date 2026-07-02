# List Comprehension - Take Notes

Ghi chú về cú pháp List Comprehension trong Python để tạo list mới ngắn gọn và tối ưu.

---

## 1. Khái niệm cơ bản

**List Comprehension** là một cú pháp ngắn gọn và trực quan của Python dùng để khởi tạo một list mới bằng cách duyệt, lọc hoặc biến đổi các phần tử từ một iterable nguồn (như `list`, `tuple`, `range`, `str`...).

> **Bản chất**: Đây là cách viết ngắn gọn của vòng lặp `for` thông thường dùng để tạo mới một list, giúp code sạch, dễ đọc và thường chạy nhanh hơn phương thức `append()` truyền thống.

---

## 2. Công thức cơ bản

```python
[new_value for item in iterable]
```

* `iterable`: Nguồn dữ liệu để duyệt (ví dụ: `range(5)`, `list`).
* `item`: Biến đại diện cho từng phần tử khi duyệt.
* `new_value`: Biến đổi hoặc biểu thức sẽ được đưa vào list mới làm phần tử.

---

## 3. Lọc dữ liệu bằng điều kiện `if`

Công thức:
```python
[new_value for item in iterable if condition]
```

* Logic: Duyệt từng phần tử, chỉ giữ lại phần tử thỏa mãn điều kiện `condition`.
* Ví dụ lọc số chẵn:
  ```python
  even_numbers = [n for n in [1, 2, 3, 4, 5] if n % 2 == 0] # [2, 4]
  ```

---

## 4. Biến đổi dữ liệu bằng điều kiện `if-else`

Khi cần thay đổi giá trị trả về dựa trên điều kiện, ta đặt `if-else` phía trước từ khóa `for`:
```python
[value_if_true if condition else value_if_false for item in iterable]
```

* Ví dụ phân loại chẵn lẻ:
  ```python
  result = ["even" if n % 2 == 0 else "odd" for n in [1, 2, 3, 4]]
  # Kết quả: ['odd', 'even', 'odd', 'even']
  ```

> [!IMPORTANT]
> **Phân biệt vị trí `if`**:
> * `if` ở cuối $\rightarrow$ Dùng để **lọc** (bỏ bớt phần tử).
> * `if else` ở trước `for` $\rightarrow$ Dùng để **biến đổi giá trị** (giữ nguyên số lượng phần tử nhưng thay đổi nội dung).

---

## 5. Khi nào nên và không nên dùng?

* **Nên dùng**:
  - Khi biểu thức logic ngắn gọn, rõ ràng (1-2 dòng).
  - Vừa lọc vừa biến đổi dữ liệu đơn giản.
* **Không nên dùng**:
  - Khi logic xử lý quá phức tạp hoặc có lồng ghép nhiều vòng lặp `for` lồng nhau (gây khó đọc).
  - Thay vào đó, hãy sử dụng vòng lặp `for` truyền thống.

---

## 6. Ví dụ cần xem

[11_list_comprehension_examples.py](file:///home/linh/VDX-intern/python-deep-notes/examples/11_list_comprehension_examples.py)
