II. Bài tập Thực chiến: Quản lý Chiết khấu Duyệt cấp Quản lý (Sale Order Approval Discount)
Để thực hành Kế thừa mở rộng (Extension Inheritance) — loại kế thừa được dùng tới 80-90% trong thực tế, bạn hãy làm bài tập sau:
 1 Ngữ cảnh nghiệp vụ (Business Case)
Thông thường, nhân viên Sale được quyền tự cho khách hàng chiết khấu (Discount). Tuy nhiên, để tránh việc Sale giảm giá quá sâu làm mất lợi nhuận của công ty, Giám đốc quy định:
    • Nếu tổng phần trăm chiết khấu trung bình của đơn hàng $\le$ 10%, đơn hàng tiến hành bình thường.
    • Nếu chiết khấu > 10%, đơn hàng phải chuyển sang trạng thái "Chờ duyệt" (To Approve). Chỉ khi Quản lý nhấn nút "Duyệt chiết khấu" (Approve Discount) thì mới được phép Xác nhận đơn hàng (Confirm Sale).
2 Yêu cầu Kỹ thuật (Yêu cầu bài tập)
Bạn hãy tạo một custom module để thực hiện các bước sau bằng cách kế thừa model sale.order:
1. Kế thừa Model (sale.order)
    • Thêm một trường Boolean tên là requires_approval (Computed field): Tự động bật True nếu đơn hàng có dòng sản phẩm nào có discount > 10 (hoặc tính trung bình tùy bạn chọn).
    • Sửa đổi trường state (Trạng thái đơn hàng): Thêm một trạng thái mới tên là to_approve (Chờ duyệt).
    • Viết một hàm mới: action_approve_discount() để chuyển trạng thái từ to_approve về draft (hoặc một trạng thái bạn tự quy định) và đánh dấu là đã duyệt.
2. Ghi đè Logic (Override Method)
    • Kế thừa và ghi đè hàm action_confirm() của sale.order.
    • Logic: Trước khi gọi super(), hãy kiểm tra nếu requires_approval == True và trạng thái chưa được Quản lý duyệt, thì đưa ra thông báo lỗi (ValidationError) ngăn không cho confirm đơn hàng.
3. Kế thừa Giao diện (View Inheritance - sale.order.form)
    • Kế thừa view sale.view_order_form.
    • Thêm nút "Duyệt chiết khấu" (nút này gọi hàm action_approve_discount) vào thanh header. Nút này chỉ hiển thị khi đơn hàng ở trạng thái to_approve (Sử dụng thuộc tính modifiers hoặc invisible).
    • Hiển thị trường requires_approval lên form (chế độ chỉ đọc) để Sale nhận biết.

