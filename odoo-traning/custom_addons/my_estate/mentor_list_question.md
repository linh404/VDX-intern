# Mentor List Question

## Danh sách câu hỏi

1. Trùng external id ở hai module thì xử lý như thế nào? Khi nào cần viết đầy đủ `module.external_id`?
2. Coding convention trong Odoo.
3. ACLs/access rights và record rule khác nhau như thế nào?
4. Mối liên hệ giữa field của model `ir.model.access` và header file `security/ir.model.access.csv`.
5. Many2one và Many2many khác nhau như thế nào ở tầng database?
6. Vì sao compute method cần lặp qua `self`, còn onchange thường không cần?
7. Computed field có `store=True` để làm gì?
8. Ba loại model trong Odoo: regular model, transient model, abstract model.
9. Các decorator API phổ biến: `@api.depends`, `@api.onchange`, `@api.constrains`, `@api.model`, `@api.model_create_multi`, `@api.depends_context`, `@api.ondelete`, `@api.autovacuum`.
10. Compute field có `store=True` có chạy bỏ qua quyền ACL/record rule hay không?
11. Computed field `store=True` và `store=False` chạy khi nào?
12. Thứ tự xử lý domain và các toán tử logic trong domain.
13. Các key hệ thống phổ biến của context: `default_<field>`, `search_default_<name>`, `group_by`, `active_id`, `active_ids`, `lang`, `tz`, `uid`, `allowed_company_ids`, ...
14. Attribute phổ biến của view `list`, `form`, `search`.
15. Khai báo `domain`/attribute trên model field và trên XML view khác nhau như thế nào?
16. Widget và option của widget trong XML view.
17. Param phổ biến của relational field: `Many2one`, `One2many`, `Many2many`.
18. Action window và action server khác nhau như thế nào?
19. Search bar và search panel trong search view.
20. Trong search bar, group được là do context hay do thẻ `group`? Đặt group-by filter trong và ngoài thẻ `group` khác nhau như thế nào? Vì sao?
21. Relational field khai báo `domain` ở model và field đó trong XML view cũng khai báo `domain` thì áp dụng hoặc xung đột như thế nào?
22. Computed field `store=True` và `store=False` check quyền như thế nào? Liên quan gì đến `compute_sudo`?
23. Relational view: `Many2one` và `One2many` có phải luôn là một cặp không? Vì sao tạo record từ `One2many` tự liên kết record cha, còn `Many2many` thì không tự điền inverse giống vậy?
24. Action archive trong Odoo hoạt động như thế nào? Field `active` và context `active_test` liên quan gì đến việc ẩn/hiện record archived?
25. Action trong Odoo có bao nhiêu loại phổ biến? Khi nào dùng `ir.actions.act_window`, `ir.actions.server`, `ir.actions.report`, `ir.actions.act_url`, `ir.actions.client`?
26. `button type="action"` hoạt động như thế nào? Khi nào `name` cần dùng cú pháp `%(module.external_id)d`, và liên hệ với report action ra sao?
27. ID trong Odoo có mấy loại? Khác nhau giữa database id, external id/XML id và vì sao cần external id?
28. Attribute `related` của field dùng để làm gì? Khác gì với computed field thông thường?
29. Field `Many2oneReference` và `Reference` khác nhau như thế nào? Khi nào nên dùng, khi nào nên tránh?
30. Report action có behavior gì khi `binding_model_id` và `binding_type="report"`? Vì sao Odoo tự thêm nút/menu Print khi chọn một hoặc nhiều record trong list view?
31. `editable` của relational list view có option gì? `editable="top"` và `editable="bottom"` khác nhau thế nào, và nếu bỏ `editable` thì thao tác tạo/sửa record con thay đổi ra sao?
32. Có nên ẩn cột list view bằng `invisible` không? Khi dùng `invisible` trên field trong list view thì chuyện gì xảy ra, khác gì với `column_invisible`?
33. Button trong Odoo view có bao nhiêu loại `type` phổ biến? Khác nhau giữa `type="object"` và `type="action"` là gì?

## Kết quả đối chiếu code

| Câu | Trạng thái | Vị trí / ghi chú |
| --- | --- | --- |
| Q1 | Có áp dụng | `views/estate_property_views.xml` dùng `%(my_estate.estate_property_offer_action)d`; `security/security.xml` dùng external id module khác như `base.group_user`. |
| Q2 | Lý thuyết / tổng quát | Coding convention áp dụng ở mức toàn project, nên không gắn comment trực tiếp vào code để tránh khó hiểu. |
| Q3 | Có áp dụng | ACL nằm trong `security/ir.model.access.csv`; record rule nằm trong `security/security.xml` và dùng `domain_force`. |
| Q4 | Có áp dụng | `security/ir.model.access.csv` có header map với field của model `ir.model.access`. Không chèn comment vào CSV để tránh làm hỏng quá trình import của Odoo. |
| Q5 | Có áp dụng | `models/estate_property.py` có `Many2one`, `Many2many`, `One2many`; `models/estate_property_offer.py` có `Many2one(..., ondelete="cascade")`. |
| Q6 | Có áp dụng | `models/estate_property.py` có `_compute_total_area`, `_compute_best_price` lặp qua `self`; `_onchange_garden` xử lý record trên form. |
| Q7 | Có áp dụng | `best_price` trong `models/estate_property.py` là computed field có `store=True`, nên giá trị được lưu xuống DB. |
| Q8 | Có áp dụng | `models.Model` cho model nghiệp vụ; `models.TransientModel` cho cancel wizard. Chưa có abstract model. |
| Q9 | Có áp dụng | Đang dùng `@api.depends`, `@api.onchange`, `@api.constrains`, `@api.model_create_multi`. |
| Q10 | Có áp dụng | `best_price` dùng `compute_sudo=True` để compute không bị lệch do ACL/record rule trên offer. |
| Q11 | Có áp dụng | `total_area` minh họa computed field non-stored; `best_price` minh họa computed field `store=True`. |
| Q12 | Có áp dụng | Domain xuất hiện ở model field, XML view, search filter và record rule. |
| Q13 | Có áp dụng | `action_open_cancel_wizard` dùng `default_property_id`; search view dùng `context="{'group_by': ...}"`. |
| Q14 | Có áp dụng | `views/estate_property_views.xml` có `list`, `form`, `search`, `limit`, `editable`, `readonly`, `invisible`. |
| Q15 | Có áp dụng | `tag_ids` có domain trên model và domain khác trong form view, minh họa sự khác nhau giữa model-level và view-level attribute. |
| Q16 | Có áp dụng | Dùng widget `statusbar`, `many2many_tags`, `handle`. |
| Q17 | Có áp dụng | Relational fields được khai báo trong property/offer/wizard models, gồm `domain`, `ondelete`, inverse field của `One2many`. |
| Q18 | Có áp dụng | Có `ir.actions.act_window` để mở view/model và `ir.actions.server` để chạy `records.action_cancel_draft()`. |
| Q19 | Có áp dụng | Search view có search fields, filter, group-by filters và `searchpanel`. |
| Q20 | Có áp dụng | Search view dùng `context="{'group_by': ...}"` trong các filter nằm dưới thẻ `group`. |
| Q21 | Có áp dụng | `tag_ids` có `domain` ở model field và có `domain` khác tại field trong form view. |
| Q22 | Có áp dụng | `best_price` là computed field `store=True, compute_sudo=True`; `total_area` là computed field non-stored. |
| Q23 | Có áp dụng | `offer_ids` là `One2many` qua inverse `property_id`; `property_id` là `Many2one`; `tag_ids` là `Many2many` dùng bảng trung gian. |
| Q24 | Có áp dụng | `models/estate_property.py` có field `active`; `views/estate_property_views.xml` có filter Archived và action context `{'active_test': False}`. |
| Q25 | Có áp dụng | `views/estate_property_views.xml` có `ir.actions.act_window` và `ir.actions.server`; `models/estate_property.py` trả về action dict `ir.actions.act_window`; `report/estate_property_report.xml` có `ir.actions.report`. Chưa có ví dụ `act_url` và `act_client`. |
| Q26 | Có áp dụng | `views/estate_property_views.xml` có button `Open Offers` dùng `type="action"` với `name="%(my_estate.estate_property_offer_action)d"`; `report/estate_property_report.xml` có report action `action_report_estate_property`. |
| Q27 | Có áp dụng | Các XML file dùng nhiều external id qua `<record id="...">`, `<menuitem id="...">`, `ref="..."`, và cú pháp `%(my_estate.estate_property_offer_action)d`; database id là id số runtime của record. |
| Q28 | Chưa áp dụng | Chưa có field nào khai báo `related="..."` trong module; nếu cần minh họa có thể thêm field related đọc từ `property_type_id` hoặc partner/user. |
| Q29 | Chưa áp dụng | `models/estate_property.py` chỉ có comment placeholder `Many2oneReference`; chưa có field `fields.Reference` hoặc `fields.Many2oneReference` thật để minh họa. |
| Q30 | Có áp dụng | `report/estate_property_report.xml` khai báo `binding_model_id` trỏ tới `model_estate_property` và `binding_type` là `report`, nên report được bind vào model và xuất hiện trong menu/nút Print cho record được chọn. |
| Q31 | Có áp dụng | `views/estate_property_views.xml` có relational list của `offer_ids` dùng `<list editable="bottom">`; nếu bỏ `editable`, list không inline-edit trực tiếp theo dòng như hiện tại mà chuyển sang mở form/dialog record con tùy view. |
| Q32 | Có áp dụng | `views/estate_property_views.xml` có `<field name="best_price" invisible="1"/>` trong list view; đây là điểm để hỏi sự khác nhau giữa ẩn field/cell bằng `invisible` và ẩn cả cột bằng `column_invisible`. |
| Q33 | Có áp dụng | `views/estate_property_views.xml` có button `type="object"` cho method Python và button `type="action"` để mở action; wizard view cũng có `type="object"` và `special="cancel"`. |
