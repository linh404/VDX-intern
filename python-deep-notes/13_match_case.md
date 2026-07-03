# Match-Case (Structural Pattern Matching) - Take Notes

Ghi chú chuyên sâu về cú pháp `match-case` (Structural Pattern Matching) được giới thiệu từ Python 3.10, so sánh điểm khác biệt cực kỳ quan trọng so với `switch-case` truyền thống trong các ngôn ngữ khác.

---

## 1. Khái niệm cơ bản

**Structural Pattern Matching** (`match-case`) là một tính năng mạnh mẽ được giới thiệu trong Python 3.10 (PEP 634). Mặc dù trông giống cú pháp `switch-case` trong các ngôn ngữ C/C++, Java, C#, hay JavaScript, nhưng nó không chỉ đơn thuần là so khớp giá trị tĩnh mà là **so khớp cấu trúc và gán biến** (destructuring & binding).

---

## 2. Các điểm khác biệt cốt lõi so với `switch-case` ngôn ngữ khác

> [!IMPORTANT]
> Đây là những điểm cực kỳ quan trọng giúp phân biệt `match-case` của Python và tránh các lỗi logic tai hại khi chuyển từ ngôn ngữ khác sang.

### 2.1 Không có Fall-through (Không dùng `break`)
- **Trong C/Java/JS**: Nếu không thêm từ khóa `break` ở cuối mỗi `case`, luồng điều khiển sẽ "trôi" (fall-through) xuống và thực thi tiếp các case bên dưới.
- **Trong Python**: Chỉ có duy nhất `case` đầu tiên khớp cấu trúc được thực thi. Sau khi chạy xong block của case đó, Python sẽ lập tức thoát khỏi cấu trúc `match`.
  - **Không cần** viết `break`.
  - Nếu cố tình viết `break` ngoài một vòng lặp, Python sẽ báo lỗi `SyntaxError`.

### 2.2 Bẫy gán biến (Variable Capture Gotcha) - Điểm khác biệt nguy hiểm nhất!

#### Biến chụp (Capture Variable) là gì?
Trong Structural Pattern Matching, **Biến chụp** là một tên biến đơn lẻ (không chứa dấu chấm `.`) đóng vai trò làm mẫu hứng đại diện. Nó **luôn khớp thành công với mọi giá trị** và tự động **gán (bind)** giá trị của đối tượng đang so khớp vào tên biến đó để sử dụng bên trong case.

#### Tại sao Python biết để capture thay vì so sánh?
Khi phân tích cú pháp `case`, Python dựa trên các quy tắc sau:
- **Giá trị cụ thể (Literal Patterns)**: Như số (`10`, `20`), chuỗi (`"user"`), `True`, `False`, `None` $\rightarrow$ Python thực hiện phép **so sánh bằng (`==`)**.
- **Tên định danh thường (Identifier)**: Như `y`, `x`, `name` $\rightarrow$ Python coi đây là một chỗ trống cần điền giá trị. Nó **không so sánh** mà thực hiện **gán giá trị** vào tên biến này.

#### Ví dụ về lỗi logic:
```python
x = 10
y = 20  # Biến ở scope ngoài

match x:
    case y:  # CẢNH BÁO: Python hiểu đây là biến chụp "y" (luôn khớp) chứ không phải so sánh!
        print("Khớp thành công!")  # Khối code này SẼ ĐƯỢC CHẠY!
        print(f"y bị gán lại thành: {y}")  # In ra: 10
```
*Sau khi chạy qua khối lệnh trên, biến `y` ở scope ngoài đã bị ghi đè và thay đổi giá trị.*

#### Cách khắc phục để so sánh giá trị:
1. **Dùng Dotted Name (Tên chứa dấu chấm)**: Định nghĩa hằng số trong class, module hoặc dùng `Enum`. Các tên có chứa dấu chấm (như `Constants.y`) được Python nhận diện là hằng số để so sánh.
2. **Dùng Guard (Điều kiện `if` đi kèm)**:
   ```python
   case value if value == y:
   ```

### 2.3 Structural Pattern Matching (Khớp cấu trúc và Phân rã dữ liệu)
- Cú pháp `switch-case` thông thường chỉ so sánh bằng (`==`) các kiểu dữ liệu nguyên thủy (số, chuỗi).
- Python `match-case` có thể so khớp cấu trúc của kiểu dữ liệu phức tạp (list, tuple, dict, object) và trích xuất trực tiếp giá trị của các phần tử bên trong (destructuring).

### 2.4 Các quy tắc cú pháp nhỏ cần lưu ý (Syntax Guidelines)

> [!TIP]
> Ghi nhớ các đặc điểm biên dịch dưới đây để tránh gặp lỗi SyntaxError khi viết code.

- **Vị trí của `case _:` (Wildcard / Default)**:
  - Chỉ được chạy khi **không có bất kỳ case nào ở trên khớp**.
  - **Bắt buộc phải nằm ở cuối cùng** của khối `match`. Nếu đặt sai vị trí, Python sẽ báo lỗi cú pháp ngay khi quét qua.
  - Nếu không viết `case _:` và không có case nào khớp, Python sẽ bỏ qua toàn bộ khối lệnh `match` và chạy tiếp các dòng code bên dưới.
  - *Ví dụ về lỗi:*
    ```python
    match status:
        case _:  # LỖI BIÊN DỊCH: SyntaxError! Wildcard phải ở cuối cùng.
            print("Mặc định")
        case 200:
            print("Thành công")
    ```

- **Hạn chế của toán tử OR (`|`)**:
  - Chỉ được dùng để nhóm các mẫu **không liên kết biến** (như `"quit" | "exit"` hoặc `200 | 201`).
  - Không được phép trộn lẫn một biến chụp (muốn gán dữ liệu) và một giá trị cụ thể bằng dấu `|`.
  - *Ví dụ về lỗi:*
    ```python
    match command_parts:
        # LỖI BIÊN DỊCH: SyntaxError! Vì 'quit' không nháy (muốn gán biến) 
        # còn '"exit"' có nháy (so sánh giá trị).
        case [quit | "exit"]:  
            print("Thoát")
    ```
  - *Viết đúng:*
    ```python
    case ["quit" | "exit"]:  # Hợp lệ (cả hai đều so sánh giá trị cụ thể)
    ```

- **Vai trò của dấu ngoặc `[]` và `()`**:
  - Dùng `case ["quit"]:` để so khớp với **cấu trúc list/tuple có 1 phần tử** là `"quit"`.
  - Dùng `case "quit":` để so khớp trực tiếp với **giá trị chuỗi đơn lẻ** `"quit"`.
  - *Ví dụ minh họa:*
    ```python
    command_parts = ["quit"]  # Kiểu list
    
    match command_parts:
        case "quit":    # THẤT BẠI! Vì so sánh list ["quit"] với string "quit"
            print("Khớp chuỗi")
        case ["quit"]:  # THÀNH CÔNG!
            print("Khớp list")
    ```
  - Trong dòng `case`, ngoặc vuông `[]` và ngoặc đơn `()` có thể dùng thay thế cho nhau (đều đại diện cho Sequence Pattern để khớp cả list và tuple).
    ```python
    case ("quit", "exit"):  # Vẫn khớp bình thường nếu command_parts là list ["quit", "exit"]
    ```

---

## 3. Các dạng so khớp (Pattern Types) phổ biến

### 3.1 Khớp giá trị cụ thể (Literal Patterns)
So khớp trực tiếp giá trị chuỗi, số hoặc `None`.
```python
match response_code:
    case 200:
        return "OK"
    case 404:
        return "Not Found"
    case _:
        return "Unknown"
```
> `_` là wildcard pattern, khớp với bất kỳ giá trị nào (tương đương `default` trong switch-case).

### 3.2 Khớp nhiều giá trị bằng toán tử OR (`|`)
Dùng ký tự `|` để gom nhóm nhiều giá trị chung một cách xử lý.
```python
match status:
    case 200 | 201 | 204:
        return "Success"
    case 400 | 404:
        return "Client Error"
```

### 3.3 Khớp chuỗi/danh sách (Sequence Patterns)
Khớp cấu trúc list hoặc tuple, có thể dùng `*rest` để gom các phần tử còn lại.
```python
match command.split():
    case ["quit"]:
        exit()
    case ["go", direction]:
        print(f"Going {direction}")
    case ["drop", *items]:
        print(f"Dropping: {items}")
```

### 3.4 Khớp Dictionary (Mapping Patterns)

Khi khớp dictionary, Python vừa kiểm tra kiểu dữ liệu, sự tồn tại của key, so khớp giá trị cụ thể, vừa trích xuất và gán biến chụp cùng một lúc.

#### Ví dụ cụ thể:
```python
match data:
    case {"type": "user", "info": {"name": name}}:
        print(f"User name: {name}")
```

#### Cơ chế hoạt động của dòng `case` trên:
Python thực hiện kiểm tra từ ngoài vào trong:
1. Kiểm tra `data` có phải là một **dictionary** không? (Nếu không, loại ngay).
2. Kiểm tra `data` có key `"type"` có giá trị bằng `"user"` (Literal Pattern) hay không?
3. Kiểm tra `data` có key `"info"` có giá trị là một **dictionary** hay không?
4. Kiểm tra trong dictionary `"info"` đó có key `"name"` hay không?
5. Nếu có, Python coi `name` là một **biến chụp** nên lập tức lấy giá trị của key `"name"` đó gán vào biến `name` để sử dụng ở khối code dưới.

#### So sánh với cách viết bằng `if-else` truyền thống:
Để đạt được độ an toàn tương đương (tránh lỗi crash `KeyError`, `AttributeError` khi data không đúng cấu trúc), cách viết `if-else` sẽ vô cùng cồng kềnh:
```python
if (isinstance(data, dict) 
    and data.get("type") == "user" 
    and isinstance(data.get("info"), dict) 
    and "name" in data["info"]):
    
    name = data["info"]["name"]  # Trích xuất thủ công
    print(f"User name: {name}")
```
*`match-case` giúp biểu diễn hình dáng (shape) dữ liệu mong muốn một cách trực quan hơn rất nhiều.*

### 3.5 Khớp Object/Class Instances
So khớp kiểu dữ liệu đối tượng và thuộc tính của đối tượng đó.
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

match point:
    case Point(x=0, y=0):
        print("Gốc tọa độ")
    case Point(x=x, y=y) if x == y:
        print(f"Nằm trên đường phân giác y=x tại ({x}, {y})")
    case Point(x=x, y=y):
        print(f"Điểm ({x}, {y})")
```

### 3.6 Khớp kèm Guard (Điều kiện phụ `if`)
Thêm điều kiện bổ sung sau mẫu khớp sử dụng từ khóa `if`.
```python
match number:
    case int() as n if n % 2 == 0:
        print(f"{n} là số chẵn")
    case int() as n:
        print(f"{n} là số lẻ")
```

#### Giải thích cú pháp `int() as n`:
Cú pháp này kết hợp hai tính năng của Pattern Matching: **Class Pattern** (`int()`) và **As Pattern** (`as n`).
1. **`int()` (So khớp kiểu/Class Pattern):**
   - Đóng vai trò như một bộ lọc kiểm tra kiểu dữ liệu (tương đương với `isinstance(number, int)`).
   - Nếu `number` không phải là số nguyên (ví dụ: chuỗi `"hello"`, danh sách `[1, 2]`), case này sẽ lập tức bị bỏ qua mà không chạy phần điều kiện `if` phía sau. Điều này giúp ngăn chặn lỗi runtime `TypeError` khi thực hiện phép chia lấy dư `n % 2`.
2. **`as n` (Gán giá trị/As Pattern):**
   - Nếu bước kiểm tra `int()` thành công (giá trị thực sự là số nguyên), Python sẽ gán giá trị đó vào biến `n`.
   - Biến `n` này sau đó được dùng trong biểu thức điều kiện phụ (guard) `if n % 2 == 0` và bên trong khối lệnh thực thi của `case`.

> [!NOTE]
> Nếu chỉ viết `case n:` thay vì `case int() as n:`, Python sẽ coi `n` là một **biến chụp (capture variable)** luôn khớp với mọi kiểu dữ liệu. Khi đó, nếu truyền vào một chuỗi `"hello"`, Python sẽ gán `"hello"` vào `n` rồi cố gắng thực thi guard `"hello" % 2 == 0`, gây ra lỗi crash chương trình (`TypeError: not all arguments converted during string formatting`).


## Tài Liệu Tham Khảo

- [PEP 634 – Structural Pattern Matching: Specification](https://peps.python.org/pep-0634/)
- [PEP 636 – Structural Pattern Matching: Tutorial](https://peps.python.org/pep-0636/)
- [Python Documentation - Match Statements](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)

---

## Ví dụ thực hành
Chi tiết các ví dụ chạy thực tế xem tại [13_match_case_examples.py](file:///home/linh/VDX-intern/python-deep-notes/examples/13_match_case_examples.py).
