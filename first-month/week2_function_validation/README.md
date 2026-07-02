# Week 2 - Function + Validation

## Kiến thức áp dụng
- Hàm (Functions, Parameters, Return values)
- Docstrings
- Xử lý ngoại lệ (`try/except/ValueError`)
- Vòng lặp `while True` kết hợp `break` để lặp lại việc kiểm tra dữ liệu đầu vào (Validation)

## Bài thực hành: Quản lý sản phẩm với Hàm và Kiểm chuẩn dữ liệu (Validation)
Cải tiến ứng dụng quản lý sản phẩm bằng cách cấu trúc mã nguồn thành các hàm đơn nhiệm, rõ ràng và thêm tầng xử lý/kiểm tra tính hợp lệ của dữ liệu đầu vào (validation).

### Các chức năng chính:
1. **Thêm sản phẩm (Có kiểm chuẩn dữ liệu)**:
   - Tên sản phẩm không được để trống hoặc chỉ có khoảng trắng.
   - Đơn giá phải là số lớn hơn 0 (bắt lỗi nhập chữ/ký tự đặc biệt bằng `try/except ValueError`).
   - Số lượng phải là số nguyên lớn hơn hoặc bằng 0.
2. **Hiển thị danh sách sản phẩm**: Sử dụng hàm riêng để xuất thông tin sản phẩm.
3. **Tính tổng giá trị kho**: Gọi hàm tính toán tổng giá trị tồn kho.
4. **Tìm kiếm sản phẩm**: Tìm kiếm sản phẩm theo từ khóa bằng hàm chuyên trách.
5. **Thoát**: Thoát khỏi chương trình.
