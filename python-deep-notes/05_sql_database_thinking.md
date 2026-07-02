# SQL Database Thinking - Take Notes

Ghi chú cá nhân về tư duy thiết kế cơ sở dữ liệu quan hệ (RDBMS), các mối quan hệ (1-N, N-1, N-N) và cơ chế truy vấn hai chiều trong SQL.

---

## 1. Bản chất các mối quan hệ (Relationship Types)

* **Quan hệ 1 - N (One-to-Many)**:
  * *Bản chất*: Một bản ghi ở bảng A liên kết với nhiều bản ghi ở bảng B, nhưng một bản ghi ở bảng B chỉ thuộc về duy nhất một bản ghi ở bảng A.
  * *Ví dụ*: Bảng `GiangVien` (GVM) và bảng `HopDong` (HopDongGVM). Một giảng viên có thể ký nhiều hợp đồng.
* **Quan hệ N - 1 (Many-to-One)**:
  * *Bản chất*: Nhiều bản ghi ở bảng B liên kết với một bản ghi ở bảng A. Đây thực chất là chiều nhìn ngược lại của quan hệ 1-N.
  * *Ví dụ*: Bảng `HopDong` và bảng `GiangVien`. Nhiều hợp đồng khác nhau có thể cùng thuộc về một giảng viên.
* **Quan hệ N - N (Many-to-Many)**:
  * *Bản chất*: Một bản ghi ở bảng A liên kết với nhiều bản ghi ở bảng B, và ngược lại.
  * *Ví dụ*: Bảng `GiangVien` và bảng `LopHoc`. Một giảng viên dạy nhiều lớp, một lớp học có nhiều giảng viên cùng dạy.
  * *Cách hiện thực*: SQL không hỗ trợ trực tiếp quan hệ N-N trong cấu trúc vật lý của bảng. Bắt buộc phải dùng một **bảng trung gian (Junction Table / Relation Table)** chứa hai khóa ngoại (FK) trỏ tới hai bảng chính.
    * *Ví dụ*: Bảng trung gian `day_hoc` chứa cặp khóa ngoại `giang_vien_id` và `lop_hoc_id`.

---

## 2. Tại sao thiết kế vật lý chỉ có N-1 nhưng logic vẫn cần cả 1-N và N-1?

### 2.1 Cấu trúc vật lý dưới Database (Physical DB Level)
* Dưới góc độ lưu trữ vật lý của SQL, **chỉ có mối quan hệ N-1 thực sự tồn tại**.
* Khóa ngoại (Foreign Key - FK) bắt buộc phải nằm ở bảng phía "Nhiều" (phía N).
  * *Ví dụ*: Bảng `HopDong` chứa cột `giang_vien_id` làm khóa ngoại.
* Bảng phía "Một" (phía 1 - bảng `GiangVien`) **không có bất kỳ cột nào** lưu danh sách ID của các hợp đồng. Trong SQL, một ô chỉ được phép chứa một giá trị nguyên tố (dạng chuẩn 1NF), do đó bảng `GiangVien` không thể lưu một danh sách/mảng các ID hợp đồng.

### 2.2 Nhu cầu tư duy truy vấn hai chiều (Bidirectional Query Logic)
Mặc dù chỉ có một khóa ngoại vật lý được lưu ở bảng con, nhưng trong thiết kế phần mềm và truy vấn dữ liệu, ta bắt buộc phải hiểu và xử lý cả hai chiều quan hệ vì các lý do sau:

#### A. Chiều xuôi (N-1): Từ "Nhiều" tìm về "Một"
* Từ một thực thể con, muốn biết nó thuộc về thực thể cha nào.
* *Cách làm*: Truy vấn trực tiếp bằng cách so khớp khóa ngoại.
* *Ví dụ*: Từ một hợp đồng, tìm xem hợp đồng đó thuộc về giảng viên nào.
  ```sql
  SELECT * FROM GiangVien WHERE id = (SELECT giang_vien_id FROM HopDong WHERE id = 10);
  ```

#### B. Chiều ngược (1-N): Từ "Một" gom nhóm "Nhiều"
* Từ một thực thể cha, muốn thống kê, hiển thị hoặc tính toán trên tất cả các thực thể con.
* *Cách làm*: Lọc ngược lại bằng cách quét khóa ngoại của bảng con.
* *Ví dụ*: Từ một giảng viên, lấy danh sách tất cả các hợp đồng đã ký của giảng viên đó.
  ```sql
  SELECT * FROM HopDong WHERE giang_vien_id = 1;
  ```

---

## 3. Ví dụ cần xem

*(Đây là tài liệu lý thuyết tư duy DB cốt lõi, được áp dụng trực tiếp khi thiết kế cấu trúc bảng và viết các câu truy vấn SQL).*
