# Mentor Answers

## Q1. Trùng external id ở hai module thì xử lý như thế nào? Khi nào cần viết đầy đủ `module.external_id`?

External id đầy đủ có dạng:

```text
module.external_id
```

Nếu chỉ viết mỗi `external_id`, Odoo sẽ hiểu theo ngữ cảnh module hiện tại. Khi tham chiếu record ở module khác, hoặc khi muốn tránh nhầm vì nhiều module có id giống nhau, nên viết đầy đủ `module.external_id`.

Ví dụ:

```xml
ref="base.group_user"
```

Ở đây phải ghi rõ `base.group_user` vì group này nằm trong module `base`.

## Q2. Coding convention trong Odoo

Một số convention hay dùng:

- Tên model dùng dạng dot: `estate.property`, `estate.property.offer`.
- Tên class dùng PascalCase: `EstateProperty`, `EstatePropertyOffer`.
- Tên field và method dùng snake_case: `expected_price`, `action_sold`.
- Method compute đặt theo field: `_compute_total_area`.
- Method onchange đặt theo field: `_onchange_garden`.
- Method constraint thường đặt dạng `_check_<rule>`.
- XML id nên rõ nghĩa, có liên quan tới module hoặc chức năng.

Mục đích chính là để code dễ đọc, dễ tìm, và thống nhất với style của Odoo.

## Q3. ACLs/access rights và record rule khác nhau như thế nào?

ACL/access rights là quyền ở mức model. Nó quyết định user hoặc group có được quyền `read`, `write`, `create`, `unlink` trên một model hay không.

Record rule là quyền ở mức record. Nó quyết định trong model đó, user được nhìn hoặc thao tác với những record nào.

Điểm khác nhau:

| Phần | ACL / Access Rights | Record Rule |
| --- | --- | --- |
| Phạm vi | Model | Record |
| Quyền xử lý | CRUD | Lọc record được phép thao tác |
| Cú pháp chính | CSV `ir.model.access.csv` | Domain trong XML |
| Ví dụ | User được đọc model `estate.property` | User chỉ thấy property của mình |

Record rule không viết SQL trực tiếp mà viết bằng Odoo domain. Domain có tư duy giống `WHERE` trong SQL, nhưng chạy qua ORM.

ACL có tính cộng dồn giữa nhiều group. Nếu user không thuộc group nào cấp quyền phù hợp thì mặc định không có quyền thao tác model đó.

## Q4. Mối liên hệ giữa field của model `ir.model.access` và header file `security/ir.model.access.csv`

`ir.model.access.csv` là file dữ liệu để tạo record cho model `ir.model.access`.

Khi load CSV, Odoo lấy dòng header để map vào field của model `ir.model.access`.

Ví dụ header thường gặp:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

Ý nghĩa:

- `id`: external id của record ACL.
- `name`: tên ACL.
- `model_id:id`: model được phân quyền, trỏ tới `ir.model`.
- `group_id:id`: group được cấp quyền.
- `perm_read`, `perm_write`, `perm_create`, `perm_unlink`: quyền CRUD.

Mỗi dòng CSV là một record ACL, và mỗi record ACL phân quyền cho một model cụ thể.

## Q5. Many2one và Many2many khác nhau như thế nào ở tầng database?

`Many2one` tạo một cột khóa ngoại trên bảng hiện tại.

Ví dụ `property_type_id = fields.Many2one("estate.property.type")` thì bảng property sẽ có một cột kiểu như:

```text
property_type_id
```

Cột này trỏ tới id của bảng `estate_property_type`.

`Many2many` không lưu trực tiếp bằng một cột khóa ngoại. Nó tạo một bảng trung gian để lưu cặp id của hai bảng.

Ví dụ property và tag:

```text
estate_property_tag_rel
- property_id
- tag_id
```

Vì vậy, với Many2many, muốn xóa liên kết giữa property và tag thì chỉ cần xóa dòng tương ứng trong bảng trung gian.

## Q6. Vì sao compute method cần lặp qua `self`, còn onchange thường không cần?

Compute method chạy ở tầng ORM. `self` trong compute thường là một recordset, có thể chứa nhiều record, nên phải lặp:

```python
for record in self:
    record.total_area = record.living_area + record.garden_area
```

Nếu không lặp, code dễ chỉ xử lý đúng cho một record hoặc bị lỗi khi Odoo compute nhiều record cùng lúc.

Onchange chạy theo thao tác trên form view. Form thường đang mở một record cụ thể, nên `self` thường là một record đang được edit trên form. Vì vậy onchange thường không cần `for`.

Khác nhau về mục đích:

- Compute dùng để tính giá trị field dựa trên dependency.
- Onchange dùng để phản ứng khi user thay đổi field trên form, ví dụ tự fill field khác, đổi domain, hoặc cảnh báo.

`store=False` của compute không thay thế hoàn toàn onchange. Compute là logic tính field, còn onchange là logic hỗ trợ trải nghiệm nhập liệu trên form.

## Q7. Computed field có `store=True` để làm gì?

`store=True` dùng để lưu giá trị computed field xuống database.

Lợi ích:

- Không phải tính lại mỗi lần đọc field.
- Có thể search, sort, group theo field đó dễ hơn.
- Phù hợp với field tính toán nặng hoặc cần dùng trong filter/report.

Khi field trong `@api.depends` thay đổi, Odoo sẽ đánh dấu field computed cần tính lại, recompute và lưu giá trị mới xuống DB.

## Q8. Ba loại model trong Odoo: regular model, transient model, abstract model

`models.Model` là model nghiệp vụ bình thường. Nó dùng cho dữ liệu thật của hệ thống, mặc định `_auto=True`, nên Odoo tạo bảng DB tương ứng.

`models.TransientModel` dùng cho dữ liệu tạm, thường là wizard hoặc popup. Nó cũng có bảng DB vì mặc định `_auto=True`, nhưng dữ liệu có thể bị dọn tự động. Một số cấu hình liên quan:

- `_transient_max_hours`: mặc định khoảng 1 giờ.
- `_transient_max_count`: mặc định `0`, nghĩa là không giới hạn số record theo count.

`models.AbstractModel` là model trừu tượng. Nó dùng để gom logic chung cho model khác kế thừa. Mặc định `_auto=False`, nên không tạo bảng DB riêng.

## Q9. Các decorator API phổ biến

Các decorator hay gặp:

| Decorator | Mục đích |
| --- | --- |
| `@api.depends` | Khai báo field phụ thuộc cho computed field. |
| `@api.onchange` | Chạy khi field thay đổi trên form view. |
| `@api.constrains` | Kiểm tra ràng buộc dữ liệu khi create/write. |
| `@api.model` | Method làm việc ở mức model, không phụ thuộc record cụ thể. |
| `@api.model_create_multi` | Dùng khi override `create` để xử lý nhiều record. |
| `@api.depends_context` | Khai báo computed field phụ thuộc vào context. |
| `@api.ondelete` | Xử lý logic khi xóa record. |
| `@api.autovacuum` | Khai báo tác vụ dọn dẹp tự động. |

## Q10. Compute field có `store=True` có chạy bỏ qua quyền ACL/record rule hay không?

Với computed field stored, Odoo thường recompute bằng superuser mode thông qua `compute_sudo`. Vì vậy khi tính toán, nó có thể bỏ qua ACL/record rule.

Nói chính xác hơn:

- `store=True` làm field được lưu xuống DB.
- `compute_sudo` quyết định compute có chạy bằng quyền superuser hay không.
- Với stored computed field, `compute_sudo` thường mặc định là `True`.

Ví dụ `best_price` phụ thuộc vào các offer. Nếu salesperson chỉ được thấy offer của chính mình do record rule, mà compute không sudo, thì `best_price` có thể bị sai vì user không thấy hết offer. Dùng `compute_sudo=True` giúp tính trên toàn bộ dữ liệu cần thiết.

## Q11. Computed field `store=True` và `store=False` chạy khi nào?

`store=True`:

- Giá trị được lưu xuống DB.
- Khi `create`, `write`, hoặc `unlink` làm thay đổi field trong `@api.depends`, Odoo đánh dấu field cần recompute.
- Sau đó Odoo tính lại và lưu giá trị mới.

`store=False`:

- Giá trị không lưu xuống DB.
- Odoo thường chỉ invalidate cache khi dependency thay đổi.
- Field được compute khi cần đọc, ví dụ mở form/list view, gọi `read()`, export dữ liệu.

Tóm lại: `store=True` thiên về lưu và tái sử dụng giá trị; `store=False` thiên về tính động khi đọc.

## Q12. Thứ tự xử lý domain và các toán tử logic trong domain

Domain là cú pháp lọc record của ORM, gần giống phần `WHERE` trong SQL.

Điều kiện cơ bản:

```python
[("state", "=", "new")]
[("expected_price", ">", 1000000)]
[("name", "ilike", "villa")]
```

Nếu không ghi toán tử logic, Odoo mặc định nối các điều kiện bằng AND:

```python
[A, B]
# A AND B
```

Các toán tử logic:

- `|`: OR, lấy 2 biểu thức ngay sau nó.
- `&`: AND, lấy 2 biểu thức ngay sau nó.
- `!`: NOT, lấy 1 biểu thức ngay sau nó.

Odoo dùng cú pháp prefix, toán tử đứng trước biểu thức:

```python
["|", A, B]
# A OR B

["&", A, B]
# A AND B

["!", A]
# NOT A

["|", "&", A, B, C]
# (A AND B) OR C
```

## Q13. Các key hệ thống phổ biến của context

Context là dict truyền thêm thông tin cho ORM, view, action hoặc method.

Các key hay gặp:

| Context key | Công dụng |
| --- | --- |
| `default_<field>` | Gán giá trị mặc định khi tạo record. |
| `search_default_<name>` | Bật sẵn field search hoặc filter trong search view. |
| `group_by` | Nhóm record mặc định theo field. |
| `active_model` | Model hiện tại đang thao tác. |
| `active_id` | ID của record hiện tại. |
| `active_ids` | Danh sách record đang được chọn. |
| `lang` | Ngôn ngữ hiện tại. |
| `tz` | Múi giờ của user. |
| `uid` | ID của user hiện tại. |
| `allowed_company_ids` | Danh sách company đang được phép dùng. |
| `active_test` | Có tự động loại record `active=False` hay không. |

Ví dụ truyền default cho wizard:

```python
context = {
    "default_property_id": self.id,
}
```

## Q14. Attribute phổ biến của view `list`, `form`, `search`

Một số attribute hay gặp:

| View | Attribute phổ biến |
| --- | --- |
| `list` | `create`, `edit`, `delete`, `editable`, `multi_edit`, `default_order`, `default_group_by`, `limit`, `decoration-*` |
| `form` | `create`, `edit`, `delete`, `duplicate`, `readonly`, `invisible` |
| `search` | Chủ yếu dùng các thẻ con như `field`, `filter`, `group`, `separator`, `searchpanel` |

Ví dụ list:

```xml
<list editable="bottom" default_order="create_date desc" limit="40">
    <field name="name"/>
    <field name="state"/>
</list>
```

Ví dụ search:

```xml
<search>
    <field name="name"/>
    <filter name="available" string="Available" domain="[('state', '=', 'new')]"/>
    <filter name="group_by_type" string="Type" context="{'group_by': 'property_type_id'}"/>
</search>
```

## Q15. Khai báo `domain`/attribute trên model field và trên XML view khác nhau như thế nào?

Khai báo trên model field là cấu hình mặc định của field đó.

Ví dụ:

```python
buyer_id = fields.Many2one(
    "res.partner",
    domain=[("is_company", "=", False)],
)
```

Các view dùng field này có thể nhận domain mặc định đó.

Khai báo trong XML view chỉ áp dụng cho field ở đúng vị trí view đó:

```xml
<field name="buyer_id" domain="[('customer_rank', '>', 0)]"/>
```

So sánh nhanh:

| Vị trí khai báo | Phạm vi |
| --- | --- |
| Model field | Mặc định, dùng lại ở nhiều view |
| XML view | Chỉ áp dụng cho lần field xuất hiện trong view đó |

Nếu model đã khai báo domain/readonly rồi mà XML view khai báo lại y hệt thì thường là thừa.

## Q16. Widget và option của widget trong XML view

Model field định nghĩa dữ liệu. View quyết định cách record được hiển thị. Field trong view tham chiếu tới field trong model. Widget quyết định field đó hiển thị bằng UI nào.

Luồng hiểu đơn giản:

```text
Model field -> View -> <field> trong view -> widget
```

Ví dụ:

```xml
<field name="state" widget="statusbar"/>
<field name="tag_ids" widget="many2many_tags"/>
<field name="expected_price" widget="monetary"/>
<field name="active" widget="boolean_toggle"/>
```

`options` dùng để cấu hình thêm cho widget:

```xml
<field name="tag_ids"
       widget="many2many_tags"
       options="{'no_create': True}"/>
```

Một số widget phổ biến:

- `statusbar`: hiển thị trạng thái theo luồng.
- `many2many_tags`: hiển thị Many2many thành tag.
- `monetary`: hiển thị số tiền.
- `image`: hiển thị ảnh từ Binary.
- `boolean_toggle`: hiển thị Boolean dạng công tắc.
- `handle`: dùng kéo thả sắp xếp trong list.

## Q17. Param phổ biến của relational field: `Many2one`, `One2many`, `Many2many`

`Many2one`:

- `comodel_name`: model được liên kết.
- `domain`: lọc record có thể chọn.
- `context`: truyền context khi mở/tạo record liên kết.
- `ondelete`: xử lý khi record được trỏ tới bị xóa, ví dụ `set null`, `restrict`, `cascade`.
- `check_company`: kiểm tra multi-company.
- `index`: tạo index DB.
- `auto_join`: tối ưu search xuyên quan hệ.
- `delegate`: dùng cho delegation inheritance.

`One2many`:

- `comodel_name`: model chứa record con.
- `inverse_name`: field Many2one ở model con.
- `domain`: lọc record con.
- `context`: truyền default/context khi tạo record con.
- `copy`: có copy record con khi duplicate record cha hay không.

`One2many` không giữ khóa ngoại trực tiếp trong DB. Khóa ngoại nằm ở field Many2one bên model con, nên One2many không có `ondelete`.

`Many2many`:

- `comodel_name`: model được liên kết.
- `relation`: tên bảng trung gian.
- `column1`: cột trỏ tới model hiện tại.
- `column2`: cột trỏ tới model bên kia.
- `domain`: lọc record có thể chọn.
- `context`: truyền context.
- `check_company`: kiểm tra multi-company nếu cần.

## Q18. Action window và action server khác nhau như thế nào?

Action window dùng để mở một model với các view như list, form, kanban.

Luồng thường gặp:

```text
Menu -> Window Action -> View
```

Server action dùng để chạy logic phía server, ví dụ gọi một method trên record.

So sánh:

| Loại action | Mục đích |
| --- | --- |
| Window action | Điều hướng, mở view/model |
| Server action | Chạy logic server |

Khi bind server action vào action menu, user có thể chọn record, bấm menu Action, rồi Odoo chạy method hoặc code đã cấu hình.

## Q19. Search bar và search panel trong search view

Search bar là vùng tìm kiếm/filter/group by phía trên view. Nó được cấu hình trong search view bằng các thẻ như `field`, `filter`, `group`, `separator`.

Các phần hay dùng:

- `field`: tạo ô tìm kiếm theo field.
- `filter`: tạo bộ lọc có sẵn bằng domain.
- `filter` có `context="{'group_by': 'field_name'}"`: tạo group by.
- `separator`: tách nhóm filter.

Ví dụ:

```xml
<search>
    <field name="name"/>
    <filter name="available"
            string="Available"
            domain="[('state', '=', 'new')]"/>
    <separator/>
    <filter name="group_by_type"
            string="Type"
            context="{'group_by': 'property_type_id'}"/>
</search>
```

Các filter đứng liền nhau thường được hiểu là cùng một nhóm và có thể OR với nhau. Khi tách nhóm bằng `separator`, các nhóm filter sẽ kết hợp theo hướng AND.

Search panel là panel lọc bên trái. Nó cũng tạo domain lọc dữ liệu, nhưng UI cố định hơn và phù hợp để lọc nhanh theo category, selection, many2one hoặc many2many.

## Q20. Trong search bar, group được là do context hay do thẻ `group`?

Group by chạy được là do context có key `group_by`.

Ví dụ:

```xml
<filter name="property_type"
        string="Property Type"
        context="{'group_by': 'property_type_id'}"/>
```

Thẻ `group` trong search view chủ yếu là thẻ tổ chức UI. Nó gom các filter group-by vào khu vực Group By của search bar và có thể cấu hình thêm như `string`, `expand`.

Nếu một filter có `context="{'group_by': ...}"` được đặt ngoài thẻ `group`, bản chất group-by vẫn đến từ context. Tuy nhiên UI/ý nghĩa cấu trúc sẽ không rõ bằng đặt trong `group`. Vì vậy convention là các filter dùng để group record nên đặt trong:

```xml
<group expand="1" string="Group By">
    <filter name="postcode"
            string="Postcode"
            context="{'group_by': 'postcode'}"/>
</group>
```

Tóm lại: group-by do context quyết định; thẻ `group` giúp Odoo hiểu và hiển thị nhóm filter đó đúng vai trò trong search bar.

## Q21. Relational field có `domain` ở model và trong XML view cũng có `domain` thì xung đột như thế nào?

Model field domain là domain nền của relational field.

Ví dụ trong model:

```python
tag_ids = fields.Many2many(
    "estate.property.tag",
    domain=[("id", "in", [1, 2, 3])],
)
```

Domain trong XML view áp dụng cho lần field xuất hiện trong view đó, chủ yếu ở phần UI chọn/search record:

```xml
<field name="tag_ids"
       widget="many2many_tags"
       domain="[('id', 'in', [4, 5, 6])]"/>
```

Trong case test này, DB có 5 tag với id `1, 2, 3, 4, 5`.

Khi mở form property, UI của `many2many_tags` dùng domain trong view, nên chỉ show được tag `4` và `5`. Tag `6` không show vì không tồn tại trong DB.

Nhưng khi bấm Save thì không lưu được các tag `4, 5` vào field `tag_ids`, vì field ở model vẫn có domain nền:

```python
domain=[("id", "in", [1, 2, 3])]
```

Nói cách khác, view domain không ghi đè hoàn toàn field domain. Nó tạo xung đột:

```text
View cho chọn: id in [4, 5, 6]
Field chỉ nhận: id in [1, 2, 3]
Kết quả: UI thấy/chọn được 4,5 nhưng save không persist được vào DB
```

Vì vậy nếu muốn vừa show được trên view vừa lưu được vào field, domain ở view không nên mâu thuẫn với domain ở model. Có thể để view domain là tập con của model domain:

```xml
<field name="tag_ids"
       domain="[('id', 'in', [1, 2])]"/>
```

Tóm lại:

| Vị trí domain | Phạm vi |
| --- | --- |
| Model field | Domain nền của relational field, ảnh hưởng khi field xử lý/lưu/đọc dữ liệu |
| XML view | Domain cho UI tại đúng vị trí field trong view, ảnh hưởng record được search/chọn |

## Q22. Computed field `store=True` và `store=False` check quyền như thế nào?

Quyền khi compute phụ thuộc vào `compute_sudo`.

Với computed field `store=True`, mặc định `compute_sudo=True`. Khi đó compute chạy bằng superuser mode để bypass access rights/record rules. Tức là lúc tính toán, nó không bị giới hạn bởi quyền đọc record của user hiện tại.

Ví dụ:

```python
best_price = fields.Float(
    compute="_compute_best_price",
    store=True,
    compute_sudo=True,
)
```

Trường hợp này phù hợp vì `best_price` cần đọc toàn bộ `offer_ids`. Nếu user bị record rule che mất một số offer, compute không sudo có thể ra kết quả sai.

Với computed field không store, tức không khai báo `store` hoặc `store=False`, mặc định `compute_sudo=False`. Khi field được đọc và compute theo user hiện tại, nó có thể bị ảnh hưởng bởi ACL/record rule.

Tóm lại:

| Computed field | Mặc định `compute_sudo` | Check quyền khi compute |
| --- | --- | --- |
| `store=True` | `True` | Thường bypass ACL/record rule |
| `store=False` | `False` | Chịu ảnh hưởng ACL/record rule của user hiện tại |

## Q23. Recommend thêm về relational view

Nói "`Many2one` và `One2many` là một cặp luôn đi với nhau" là chưa đúng.

Đúng hơn:

- `One2many` bắt buộc phải có inverse field là một `Many2one` ở model bên kia.
- `Many2one` có thể đứng một mình, không bắt buộc phải có `One2many` tương ứng.

Trong module này:

```python
offer_ids = fields.One2many(
    "estate.property.offer",
    "property_id",
)
```

`offer_ids` hoạt động được vì model `estate.property.offer` có:

```python
property_id = fields.Many2one(
    "estate.property",
    required=True,
    ondelete="cascade",
)
```

Khi đứng ở form bất động sản và thêm offer trong tab `offer_ids`, Odoo biết record cha là bất động sản hiện tại và biết inverse field là `property_id`. Vì vậy offer mới sẽ tự được gán `property_id` về bất động sản đó.

Với `Many2many`, quan hệ nằm trong bảng trung gian, không nằm ở một field inverse bắt buộc trên record bên kia. Vì vậy khi tạo record liên quan từ một field `Many2many`, Odoo có thể tạo dòng liên kết trong bảng trung gian, nhưng không tự điền một field kiểu `property_id` trên record mới nếu field đó không tồn tại hoặc không được truyền qua context.

Nếu muốn tự điền field cha khi mở popup tạo record liên quan, có thể truyền context dạng:

```xml
<field name="offer_ids"
       context="{'default_property_id': id}"/>
```

Nhưng với `One2many`, việc này thường đã được xử lý qua inverse field. Với `Many2many`, phải hiểu là nó link qua bảng trung gian, không phải qua một khóa ngoại nằm trên record con.

## Q24. Action archive trong Odoo

`active` là một field có ý nghĩa đặc biệt trong Odoo. Khi model có field Boolean tên `active`, Odoo dùng field này như cơ chế archive/unarchive mềm cho record.

Quy ước thường dùng:

```python
active = fields.Boolean(default=True)
```

`active=True` nghĩa là record đang hoạt động. `active=False` nghĩa là record đã được archive. Archive không xóa record khỏi database, mà chỉ làm record bị ẩn khỏi phần lớn search/list mặc định.

Khi model có field `active`, Odoo có sẵn các method sau trên recordset:

```python
# active=True -> active=False
record.action_archive()

# active=False -> active=True
record.action_unarchive()

# Đảo giá trị active
record.toggle_active()
```

Trên view, khi model có field `active`, Odoo có thể hiển thị action Archive/Unarchive trong menu Action để thao tác với record mà không cần tự viết server action riêng.

Mặc định ORM dùng context:

```python
{"active_test": True}
```

Vì vậy các record có `active=False` thường bị loại khỏi kết quả search/list. Muốn tìm record đã archive trong search view thì thêm filter explicit:

```xml
<filter name="archived"
        string="Archived"
        domain="[('active', '=', False)]"/>
```

Nếu muốn mở list và thấy cả record active lẫn archived, có thể tắt cơ chế lọc mặc định bằng context trên window action:

```xml
<field name="context">
    {'active_test': False}
</field>
```

Trong module này, `estate.property` đã có field `active = fields.Boolean(default=True)`, search view có filter `Archived`, và action mở list có context `{'active_test': False}` để không tự loại record archived khỏi danh sách.

## Q25. Action trong Odoo có bao nhiêu loại phổ biến?

Các loại action phổ biến trong Odoo backend:

| Action type | Model / type | Mục đích |
| --- | --- | --- |
| Window action | `ir.actions.act_window` | Mở model bằng list, form, kanban, search view. |
| Server action | `ir.actions.server` | Chạy logic server, ví dụ gọi Python code/method trên records. |
| Report action | `ir.actions.report` | Render report QWeb/PDF/HTML. |
| URL action | `ir.actions.act_url` | Mở URL nội bộ hoặc bên ngoài. |
| Client action | `ir.actions.client` | Gọi client-side action/web client component. |

Ngoài ra còn có action dict đặc biệt như:

```python
{"type": "ir.actions.act_window_close"}
```

Nó thường dùng để đóng wizard/popup.

Áp dụng trong source code:

- Có áp dụng `ir.actions.act_window`: `views/estate_property_views.xml`, `views/estate_property_offer_views.xml`, `views/estate_property_tag_views.xml`, `views/estate_property_type_views.xml`.
- Có áp dụng action dict `ir.actions.act_window`: method `action_open_cancel_wizard()` trong `models/estate_property.py`.
- Có áp dụng `ir.actions.server`: record `estate_property_action_cancel` trong `views/estate_property_views.xml`.
- Có áp dụng `ir.actions.report`: record `action_report_estate_property` trong `report/estate_property_report.xml`.
- Có áp dụng `ir.actions.act_window_close`: wizard `estate_property_cancel_wizard.py`.
- Chưa thấy ví dụ `ir.actions.act_url` và `ir.actions.client` trong module `my_estate`.

## Q26. `button type="action"` hoạt động như thế nào?

`button type="action"` không gọi Python method trực tiếp. Nó yêu cầu web client load và chạy một action đã được khai báo sẵn.

Ví dụ trong form property:

```xml
<button name="%(my_estate.estate_property_offer_action)d"
        type="action"
        string="Open Offers"/>
```

Ở đây `name` dùng cú pháp:

```xml
%(module.external_id)d
```

Odoo sẽ resolve XML id `my_estate.estate_property_offer_action` thành database id thật của action rồi truyền cho web client.

Nếu chỉ ghi tên method Python thì phải dùng `type="object"`, không phải `type="action"`.

Với report, có thể tạo button `type="action"` trỏ tới một `ir.actions.report`. Khi bấm, Odoo chạy report action đó. Tuy nhiên trong module này chưa có backend button report dạng:

```xml
<button name="%(my_estate.action_report_estate_property)d"
        type="action"
        string="Print"/>
```

Module hiện tại expose report qua binding Print menu, không qua button form. Nút `Report` trong `estate_website_templates.xml` là HTML button submit của website route, không phải Odoo backend button `type="action"`.

Áp dụng trong source code:

- Có áp dụng `button type="action"`: button `Open Offers` trong `views/estate_property_views.xml`.
- Có report action liên quan: `report/estate_property_report.xml`.
- Chưa có backend button `type="action"` gọi trực tiếp report action.

## Q27. ID trong Odoo có mấy loại, tại sao cần external ID?

Trong thực tế hay gặp 2 loại ID chính:

| Loại ID | Ví dụ | Ý nghĩa |
| --- | --- | --- |
| Database ID | `42` | Primary key số nguyên trong bảng database. Có thể khác nhau giữa các database. |
| External ID / XML ID | `my_estate.estate_property_action` | ID ổn định ở tầng module/data, được lưu trong `ir.model.data`. |

Trong XML, khi khai báo:

```xml
<record id="estate_property_action" model="ir.actions.act_window">
```

thì external id đầy đủ là:

```text
my_estate.estate_property_action
```

Cần external ID vì:

- Tham chiếu record giữa các file XML/CSV.
- Tham chiếu record từ module khác bằng `module.external_id`.
- Giúp Odoo update đúng record khi upgrade module, thay vì tạo record trùng.
- Database ID không ổn định giữa local, staging, production.

Ví dụ:

```xml
<field name="binding_model_id" ref="model_estate_property"/>
```

`ref` dùng external id để tìm đúng record. Nếu record ở module khác thì phải ghi đầy đủ:

```xml
ref="base.group_user"
```

Áp dụng trong source code:

- Có áp dụng `<record id="...">` trong data, security, views, report.
- Có áp dụng `<menuitem id="...">` trong `views/estate_menus.xml` và các menu view khác.
- Có áp dụng `ref="..."` trong security/view/report XML.
- Có áp dụng cú pháp `%(my_estate.estate_property_offer_action)d` ở button `type="action"`.

## Q28. Attribute `related` của field dùng để làm gì?

`related` dùng để tạo field lấy giá trị thông qua một chain field khác.

Ví dụ:

```python
property_type_name = fields.Char(
    related="property_type_id.name",
    store=True,
)
```

Field này không tự tính bằng method riêng. Nó đọc giá trị từ:

```text
record.property_type_id.name
```

Khác với computed field thông thường:

| Phần | `related` | computed field |
| --- | --- | --- |
| Cách tính | Đi theo field chain có sẵn | Tự viết method compute |
| Logic phức tạp | Không phù hợp | Phù hợp |
| Ví dụ | Lấy tên type, country của partner | Tính tổng diện tích, best price |
| `store=True` | Có thể dùng | Có thể dùng |

`related` phù hợp khi chỉ muốn expose lại một field từ record liên quan. Nếu logic có điều kiện, tổng hợp nhiều record, hoặc cần xử lý đặc biệt thì dùng computed field.

Áp dụng trong source code:

- Chưa áp dụng. Rà trong `my_estate` chưa thấy field nào khai báo `related="..."`.
- Module đang có computed field thật là `total_area` và `best_price` trong `models/estate_property.py`.

## Q29. Field `Many2oneReference` và `Reference` khác nhau như thế nào?

`Reference` và `Many2oneReference` là pseudo-relational field. Chúng dùng cho quan hệ đa hình, tức một field có thể trỏ tới record thuộc nhiều model khác nhau.

`fields.Reference` lưu cả model và id trong cùng một giá trị dạng:

```text
model_name,record_id
```

Ví dụ ý tưởng:

```python
target_ref = fields.Reference(
    selection=[
        ("estate.property", "Property"),
        ("estate.property.offer", "Offer"),
    ],
)
```

`fields.Many2oneReference` lưu record id như một integer field, còn tên model nằm ở một field khác được chỉ định bằng `model_field`.

Ví dụ ý tưởng:

```python
target_model = fields.Char()
target_id = fields.Many2oneReference(model_field="target_model")
```

Khác nhau:

| Field | Cách lưu model | Cách lưu id |
| --- | --- | --- |
| `Reference` | Trong chính giá trị reference | Trong chính giá trị reference |
| `Many2oneReference` | Trong field khác, ví dụ `target_model` | Trong field hiện tại |

Cả hai đều không mạnh như `Many2one` bình thường ở tầng database vì không có foreign key thật tới một bảng cố định. Vì vậy nên tránh dùng nếu quan hệ có thể biểu diễn bằng `Many2one`, `One2many`, hoặc `Many2many` rõ ràng.

Áp dụng trong source code:

- Chưa áp dụng thật. `models/estate_property.py` chỉ có comment placeholder:

```python
# test = fields.Many2oneReference(model_field=)
```

- Chưa thấy field `fields.Reference(...)` hoặc `fields.Many2oneReference(...)` được khai báo thật trong module.

## Q30. Report action tự thêm nút/menu Print khi chọn nhiều record như thế nào?

Report action được khai báo bằng `ir.actions.report`.

Trong module này:

```xml
<record id="action_report_estate_property" model="ir.actions.report">
    <field name="name">Report Estate Property</field>
    <field name="model">estate.property</field>
    <field name="report_type">qweb-html</field>
    <field name="report_name">my_estate.report_estate_property</field>
    <field name="report_file">my_estate.report_estate_property</field>
    <field name="print_report_name">'Estate Property - %s' % (object.name)</field>
    <field name="binding_model_id" ref="model_estate_property"/>
    <field name="binding_type">report</field>
</record>
```

Hai field quan trọng:

- `binding_model_id`: bind report vào model `estate.property`.
- `binding_type="report"`: báo cho Odoo đây là report action của model đó.

Khi report được bind như vậy, Odoo tự đưa report vào menu/nút Print của model tương ứng. Ở list view, khi user chọn một hoặc nhiều property, web client có thể gọi report action với các record được chọn.

Template report cũng đang support nhiều record vì dùng:

```xml
<t t-foreach="docs" t-as="doc">
    <t t-call="my_estate.report_estate_property_document"/>
</t>
```

Tức là nếu chọn nhiều property, report render lặp qua nhiều `doc`.

Áp dụng trong source code:

- Có áp dụng trong `report/estate_property_report.xml`.
- Có `binding_model_id` và `binding_type="report"`.
- Có `t-foreach="docs"` nên report phù hợp với behavior in nhiều record.

## Q31. `editable` của relational list view có option gì?

Trong list view, `editable` thường có 2 giá trị:

| Giá trị | Ý nghĩa |
| --- | --- |
| `editable="top"` | Dòng tạo mới/inline edit nằm phía trên list. |
| `editable="bottom"` | Dòng tạo mới/inline edit nằm phía dưới list. |

Trong module này, tab Offers dùng relational list view:

```xml
<field name="offer_ids">
    <list editable="bottom">
        <field name="price"/>
        <field name="partner_id"/>
        ...
    </list>
</field>
```

Vì `offer_ids` là `One2many`, khi tạo offer mới inline trong list này, Odoo biết inverse field là `property_id` nên tự liên kết offer mới với property cha.

Nếu bỏ `editable` khỏi list:

- List không còn inline-edit trực tiếp theo dòng.
- User thường phải mở form/dialog của record con để tạo hoặc sửa.
- UI sẽ nặng hơn nhưng phù hợp hơn nếu record con có nhiều field, nhiều logic onchange, hoặc cần layout form rõ ràng.

Áp dụng trong source code:

- Có áp dụng `editable="bottom"` trong relational list `offer_ids` tại `views/estate_property_views.xml`.
- Chưa thấy ví dụ `editable="top"` trong module `my_estate`.

## Q32. Ẩn cột list view bằng `invisible` được không?

Không nên dùng `invisible` nếu mục tiêu là ẩn cả cột list view.

Trong list view Odoo, có 2 khái niệm cần tách:

| Attribute | Tác dụng chính trong list view |
| --- | --- |
| `invisible` | Ẩn nội dung cell theo từng record. Cột vẫn có thể còn header/space. |
| `column_invisible` | Ẩn cả column khỏi list. |

Ví dụ hiện tại:

```xml
<field name="best_price" invisible="1"/>
```

Với list view, `invisible="1"` làm cell của field này bị ẩn/rỗng. Nhưng vì column không bị loại khỏi danh sách active columns, UI có thể vẫn còn một cột trống.

Nếu mục tiêu là ẩn hẳn cột, nên dùng:

```xml
<field name="best_price" column_invisible="1"/>
```

`invisible` vẫn hữu ích khi cần field có mặt trong view để phục vụ modifier/domain/onchange logic, nhưng không muốn hiển thị giá trị ở từng cell.

Áp dụng trong source code:

- Có áp dụng `invisible="1"` trên field `best_price` trong list view `views/estate_property_views.xml`.
- Chưa thấy `column_invisible` trong module `my_estate`.
- Rà source Odoo local `odoo-19`: list renderer lọc active columns bằng `column_invisible`; còn `invisible` được evaluate khi render từng cell.

## Q33. Button type trong Odoo view có bao nhiêu loại phổ biến?

Trong Odoo backend XML view, `button` thường dùng 2 loại `type` chính:

| Button type | Ý nghĩa |
| --- | --- |
| `type="object"` | Gọi Python method trên model/recordset hiện tại. |
| `type="action"` | Chạy một Odoo action đã khai báo sẵn. |

Ví dụ `type="object"`:

```xml
<button name="action_sold"
        type="object"
        string="Sold"/>
```

Khi bấm, Odoo gọi method Python:

```python
def action_sold(self):
    ...
```

Ví dụ `type="action"`:

```xml
<button name="%(my_estate.estate_property_offer_action)d"
        type="action"
        string="Open Offers"/>
```

Khi bấm, Odoo mở action `estate_property_offer_action`.

Trong wizard còn có:

```xml
<button string="Discard" special="cancel"/>
```

`special="cancel"` không phải là `type`. Nó là behavior đặc biệt của form/wizard để đóng popup hoặc hủy thao tác.

Lưu ý: button trong website template như:

```xml
<button type="submit">Report</button>
```

là HTML button, không phải Odoo backend view button `type="object"`/`type="action"`.

Áp dụng trong source code:

- Có áp dụng `type="object"` ở các button `action_sold`, `action_open_cancel_wizard`, `action_accept`, `action_refuse`, và wizard `action_confirm_cancel`.
- Có áp dụng `type="action"` ở button `Open Offers`.
- Có áp dụng `special="cancel"` ở wizard cancel button.
- Có HTML button `type="submit"` trong website template, nhưng nó thuộc HTML form behavior, không phải Odoo backend button action behavior.
