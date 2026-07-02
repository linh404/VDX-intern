# Week 4 - File + JSON Mini Project

## Kiến thức áp dụng
- Làm việc với File I/O (`open`, `read`, `write`)
- Sử dụng module `json` (`json.load`, `json.dump`)
- Xử lý ngoại lệ với File (`FileNotFoundError`, `json.JSONDecodeError`)
- Kiến trúc phần mềm cơ bản: Chia tách Layer (tách logic xử lý data vào `product_service.py` và UI vào `main.py`)
- Dữ liệu bền vững (Persistent Data) thông qua file hệ thống

## Bài thực hành: Ứng dụng Quản lý sản phẩm với Lưu trữ JSON & Kiến trúc Phân tầng
Xây dựng một Mini Project hoàn chỉnh với dữ liệu bền vững (Persistent Data) thông qua tệp tin `products.json`. Đồng thời, chia tách cấu trúc dự án thành các lớp (layers) rõ ràng và viết kiểm thử tự động với `unittest`.

### Cấu trúc dự án:
- [product.py](file:///home/linh/VDX-intern/first-month/week4_file_json_project/product.py): Định nghĩa lớp `Product`.
- [product_service.py](file:///home/linh/VDX-intern/first-month/week4_file_json_project/product_service.py): Tầng xử lý nghiệp vụ (Business Logic) và File I/O. Đọc và lưu dữ liệu trực tiếp từ/vào tệp tin `products.json`.
- [main.py](file:///home/linh/VDX-intern/first-month/week4_file_json_project/main.py): Tầng giao diện người dùng CLI (Presentation Layer). Chỉ chịu trách nhiệm tương tác nhập/xuất và gọi hàm từ `product_service`.
- [test_product.py](file:///home/linh/VDX-intern/first-month/week4_file_json_project/test_product.py): Các ca kiểm thử tự động (Unit Test) cho lớp `Product`.

### Các chức năng chính:
1. **Thêm sản phẩm**: Tạo đối tượng `Product`, lưu vào list và ghi đè đồng bộ xuống file JSON.
2. **Hiển thị danh sách sản phẩm**: Đọc dữ liệu từ file JSON ngay khi khởi chạy chương trình.
3. **Tìm kiếm sản phẩm**.
4. **Cập nhật số lượng**: Cập nhật số lượng của một sản phẩm và lưu lại file JSON.
5. **Xóa sản phẩm**: Xóa sản phẩm khỏi danh sách và cập nhật lại file JSON.
6. **Tính tổng giá trị kho**.
7. **Thoát**.
