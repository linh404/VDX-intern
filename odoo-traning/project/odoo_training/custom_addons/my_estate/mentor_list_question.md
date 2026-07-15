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
