# May10 QMS i18n CI — Implementation specification

## 1. Document control

### 1.1. Mục đích

Document này mô tả cách triển khai chi tiết hai job i18n theo plan tổng thể:

- [`may10-qms-weblate-integration-assessment.md`](may10-qms-weblate-integration-assessment.md): kiến trúc và plan tổng thể;
- `/home/linh/odoo-qms/pipelines/i18n-test.yml`: source tham chiếu chính cho implementation và behavior đã test.

Mọi mô tả trong document này ưu tiên behavior đang có trong YAML pilot. Phần khác biệt giữa pilot và cấu hình target May10 được đánh dấu riêng ở mục 8.

### 1.2. Job được triển khai

| Job | YAML definition | Trigger thực tế trong pilot |
|---|---|---|
| `validate-i18n` | `/home/linh/odoo-qms/pipelines/i18n-test.yml:73` | MR có thay đổi `*.po` hoặc `*.pot` |
| `export-i18n` | `/home/linh/odoo-qms/pipelines/i18n-test.yml:291` | Pipeline trên branch `dev`, ngoại trừ MR pipeline |

## 2. YAML structure và pipeline contract

### 2.1. Standalone pilot

Pilot hiện khai báo stage riêng:

```yaml
stages:
  - i18n
```

Đây là cấu hình cho pipeline test độc lập. Khi include vào May10 QMS, không được thay thế stage list hiện tại; phải chèn stage `i18n` sau `test` và trước `deploy`:

```yaml
stages:
  - build
  - quality
  - test
  - i18n
  - deploy
  - recovery
```

### 2.2. Job-level controls

Cả hai job trong pilot dùng:

```yaml
stage: i18n
resource_group: qms-i18n
tags:
  - qms-local-shell
```

Ý nghĩa:

- `stage: i18n`: đặt i18n sau test và trước deploy khi chạy trong pipeline đầy đủ;
- `resource_group: qms-i18n`: serialize các job có thể dùng chung Shell Runner/workspace;
- `qms-local-shell`: runner pilot có Odoo virtualenv và PostgreSQL local.

Hai job không khai báo `allow_failure: true`; vì vậy đều blocking khi được tạo.

### 2.3. Global variables

Các biến được khai báo ở `/home/linh/odoo-qms/pipelines/i18n-test.yml:6-71`.

#### Git và commit

| Variable | Giá trị pilot | Sử dụng |
|---|---|---|
| `GIT_DEPTH` | `0` | Đảm bảo có đủ lịch sử để tính diff |
| `LC_ALL` | `C.UTF-8` | Chuẩn hóa encoding/locale |
| `I18N_PUSH_ENABLED` | `true` | Bật push POT sau khi export |
| `I18N_PUSH_BRANCH` | `dev` | Branch nhận bot commit |
| `I18N_PUSH_REMOTE` | `origin` | Git remote được push |
| `I18N_GIT_USER_NAME` | `Odoo i18n CI Bot` | Identity commit |
| `I18N_GIT_USER_EMAIL` | `odoo-i18n-bot@noreply.invalid` | Email commit |
| `I18N_COMMIT_MESSAGE` | `[skip ci] [i18n] Update POT templates` | Commit message và loop prevention |

#### Module selection và impact detection

| Variable | Giá trị pilot | Sử dụng |
|---|---|---|
| `I18N_FORCE_MODULES` | rỗng | Chỉ dùng cho backfill/test; bỏ qua module selection từ diff |
| `I18N_EXCLUDE_MODULES` | rỗng | Loại module khỏi managed module set |
| `I18N_IMPACT_POLICY` | `strict-local` | Chọn direct module hoặc mở rộng dependency |
| `I18N_DB_PREFIX` | `odoo_i18n` | Prefix temporary database |
| `I18N_GLOBAL_GLOBS` | rỗng | Path làm full fallback |
| `I18N_IRRELEVANT_GLOBS` | multiline | Path không cần export |

`I18N_IRRELEVANT_GLOBS` hiện bao gồm README/docs, CI metadata, dependency files, Docker files, `.build/**`, `**/*.po` và `**/*.pot`. Khi thêm loại file mới vào repository, phải cập nhật biến này nếu file đó không ảnh hưởng POT.

#### Odoo và PostgreSQL

| Variable | Giá trị pilot | Sử dụng |
|---|---|---|
| `ODOO_SERIES` | `18.0` | Odoo series cho Manifestoo |
| `ODOO_CORE_ROOT` | `/home/linh/odoo-18` | Odoo source/addons root |
| `ODOO_BIN` | `/home/linh/odoo-18/odoo-bin` | Odoo executable |
| `ODOO_PYTHON` | `/home/linh/odoo-qms/.venv/bin/python` | Python runtime |
| `MANIFESTOO_BIN` | `/home/linh/odoo-qms/.venv/bin/manifestoo` | Module dependency tool |
| `ODOO_DB_HOST` | `127.0.0.1` | PostgreSQL host |
| `ODOO_DB_PORT` | `5432` | PostgreSQL port |
| `ODOO_DB_USER` | `odoo_ci` | DB role |
| `ODOO_DB_PASSWORD` | `odoo_ci` | DB credential |

Path local của pilot không được copy nguyên vào template dùng chung. Khi chuyển sang May10, các path và credential phải là project/runner variable hoặc secret.

#### PO/POT policy

| Variable | Giá trị pilot | Behavior |
|---|---|---|
| `I18N_ENFORCE_PO_POLICY` | `false` | Không enforce source identity trong pilot mặc định |
| `I18N_ALLOWED_PO_SOURCE_PROJECT` | rỗng | Project được phép tạo MR PO/POT |
| `I18N_ALLOWED_PO_SOURCE_BRANCH_PREFIX` | rỗng | Prefix branch được phép |

Khi bật `I18N_ENFORCE_PO_POLICY=true`, MR pass nếu source project khớp hoặc source branch bắt đầu bằng prefix được cấu hình. Nếu cả hai giá trị được phép đều rỗng, mọi MR PO/POT sẽ fail.

## 3. `validate-i18n` — implementation detail

### 3.1. Metadata và rule

Block YAML tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:73-89`:

```yaml
validate-i18n:
  stage: i18n
  resource_group: qms-i18n
  tags:
    - qms-local-shell
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      changes:
        - '**/*.po'
        - '**/*.pot'
      when: on_success
    - when: never
```

Job creation behavior:

| Pipeline | MR diff | Job |
|---|---|---|
| MR | Không có PO/POT | Skip |
| MR | Có PO/POT | Tạo job, blocking |
| Push branch | Bất kỳ | Skip |
| Web/manual pipeline | Bất kỳ | Skip |

### 3.2. Preflight và workspace

`before_script` tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:90-110` thực hiện:

1. `set -Eeuo pipefail`.
2. `cd "$CI_PROJECT_DIR"`.
3. Kiểm tra command bắt buộc:

   ```text
   git msgfmt python3
   ```

4. Xóa `.ci-i18n-validate` từ lần chạy trước.
5. Kiểm tra Git worktree sạch bằng `git status --porcelain --untracked-files=all`.
6. Tạo workspace artifact `.ci-i18n-validate`.

Job không yêu cầu Odoo, PostgreSQL hoặc Manifestoo.

### 3.3. Xác định file thay đổi

Script tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:112-155` chọn base commit theo thứ tự:

1. `CI_MERGE_REQUEST_DIFF_BASE_SHA`;
2. `CI_COMMIT_BEFORE_SHA`;
3. `HEAD^` nếu giá trị rỗng hoặc toàn số `0`.

Sau đó chạy:

```bash
git diff --name-only --diff-filter=ACMR "$base_sha" "$CI_COMMIT_SHA" \
  -- '*.po' '*.pot'
```

`D` không nằm trong diff filter; file PO/POT bị xóa được ghi nhận ở rule nhưng không được validate nội dung vì file không còn tồn tại.

Nếu danh sách rỗng, job ghi summary và exit `0`.

### 3.4. Policy check

Policy chạy trước `msgfmt` nếu `I18N_ENFORCE_PO_POLICY=true`:

```text
source_project = CI_MERGE_REQUEST_SOURCE_PROJECT_PATH
source_branch  = CI_MERGE_REQUEST_SOURCE_BRANCH_NAME

pass nếu:
  source_project == I18N_ALLOWED_PO_SOURCE_PROJECT
  hoặc
  source_branch bắt đầu bằng I18N_ALLOWED_PO_SOURCE_BRANCH_PREFIX
```

Nếu không pass, job exit `1` với source project/branch trong log. Policy không dựa vào tên người commit.

### 3.5. GNU gettext validation

Mỗi file tồn tại trong changed-file list được validate bằng:

```bash
msgfmt --check --check-format \
  --output-file=/dev/null \
  path/to/file.po
```

`msgfmt` kiểm tra:

- cú pháp PO/POT;
- encoding và quoted string;
- header/catalog format;
- format string khi catalog có cờ format;
- plural/message format theo khả năng của GNU gettext.

Job không dùng `msgmerge` và không export POT.

### 3.6. Placeholder checker

Script Python inline tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:179-256` không dùng thư viện ngoài. Nó:

1. Parse entry theo `msgid`, `msgid_plural`, `msgstr` và `msgstr[n]`.
2. Decode quoted literal bằng `ast.literal_eval`.
3. Bỏ qua header có `msgid ""`.
4. Bỏ qua `msgstr` rỗng.
5. Trích xuất và so sánh Counter của:
   - printf placeholder `%s`, `%d`, `%(name)s` và biến thể format;
   - brace placeholder `{name}`.
6. Với plural entry, cho phép `msgstr[n]` khớp `msgid` hoặc `msgid_plural`.
7. Ghi lỗi theo file, entry index và field nếu Counter không khớp.

### 3.7. Output và artifact

Artifact luôn upload với thời hạn một tuần:

```text
.ci-i18n-validate/changed-files.txt
.ci-i18n-validate/validation.log
.ci-i18n-validate/placeholder.log
.ci-i18n-validate/summary.txt
```

Job fail nếu một trong các bước policy, `msgfmt` hoặc placeholder checker fail. Job không commit, push, tạo database hoặc deploy.

## 4. `export-i18n` — implementation detail

### 4.1. Metadata và rule thực tế của pilot

Block YAML tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:291-305`:

```yaml
export-i18n:
  stage: i18n
  resource_group: qms-i18n
  tags:
    - qms-local-shell
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: never
    - if: '$CI_COMMIT_BRANCH == "dev"'
      when: on_success
    - when: never
```

Behavior hiện tại:

| Pipeline | Branch | Job |
|---|---|---|
| MR | `dev` hoặc branch khác | Skip |
| Push | `dev` | Run |
| Web/manual | `dev` | Có thể run nếu GitLab set `CI_COMMIT_BRANCH=dev` |
| Push | `production` | Skip |
| Push | branch khác | Skip |

Target May10 nên siết rule thành `CI_PIPELINE_SOURCE == "push" && CI_COMMIT_BRANCH == "dev"` nếu không muốn web/manual pipeline trên `dev` gọi export.

### 4.2. Preflight và cleanup trước script

`before_script` tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:307-346`:

1. Bật `set -Eeuo pipefail`.
2. Kiểm tra `git`, `find`, `realpath`.
3. Kiểm tra `$CI_PROJECT_DIR` và executable `$ODOO_PYTHON`.
4. Xóa workspace job-owned:

   ```text
   .ci-i18n
   .ci-i18n-validate
   .odoo-data
   ```

5. Kiểm tra repository sạch.
6. Tạo diagnostics:

   ```text
   .ci-i18n/export.log
   .ci-i18n/validation.log
   .ci-i18n/dependency.log
   .ci-i18n/impact-analysis.txt
   .ci-i18n/changed-files.txt
   .ci-i18n/cleanup.log
   .ci-i18n/i18n-summary.txt
   .ci-i18n/i18n.patch
   ```

Cleanup `.ci-i18n-validate` là bắt buộc khi Shell Runner dùng lại workspace sau một MR validation job.

### 4.3. Runtime paths

Script tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:348-382` tạo các path/job variables:

| Variable | Path/giá trị | Vai trò |
|---|---|---|
| `TEMP_DB` | `${I18N_DB_PREFIX}_${CI_PIPELINE_ID}_${CI_JOB_ID}` | Temporary database |
| `ODOO_DATA_DIR` | `$CI_PROJECT_DIR/.odoo-data` | Odoo data directory |
| `I18N_WORK_DIR` | `$CI_PROJECT_DIR/.ci-i18n` | Job workspace |
| `MODULE_INDEX_FILE` | `module-index.tsv` | Tất cả module discovered |
| `MANAGED_MODULES_FILE` | `managed-modules.tsv` | Module installable/được quản lý |
| `DIRECT_MODULES_FILE` | `direct-modules.txt` | Module sở hữu changed source |
| `EXPORT_MODULES_FILE` | `export-modules.tsv` | Module sẽ export |
| `IMPACT_MODE_FILE` | `impact-mode.txt` | `NO_RELEVANT_CHANGE`, `CHANGED_MODULES`, `FULL_FALLBACK`, `FORCED` |
| `GENERATED_LIST` | `generated-pot-files.txt` | POT được job tạo |
| `DB_CREATED_MARKER` | `db-created` | Xác nhận DB cần cleanup |

### 4.4. Module discovery

Python discovery block bắt đầu tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:384`:

1. `rglob("__manifest__.py")` trên `$CI_PROJECT_DIR`.
2. Bỏ qua `.git`, virtualenv, `node_modules`, cache và workspace i18n.
3. Chỉ nhận directory có cả `__manifest__.py` và `__init__.py`.
4. Parse manifest bằng `ast.literal_eval`.
5. Fail nếu manifest không parse được hoặc không phải dictionary.
6. Fail nếu trùng module name.
7. Phân loại module:
   - `noninstallable`: `installable: false`;
   - `excluded`: nằm trong `I18N_EXCLUDE_MODULES`;
   - `managed`: còn lại.
8. Ghi module index và managed module list.
9. Fail nếu không có managed installable module.

Project addon roots được thêm trước Odoo core addons để ưu tiên code trong checkout:

```text
<parent directory của mỗi project module>
ODOO_CORE_ROOT/addons
ODOO_CORE_ROOT/odoo/addons
```

### 4.5. Impact detection

Impact detector tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:537-805`.

#### Diff validation

Trước khi chạy `git diff`, job kiểm tra:

1. `CI_COMMIT_SHA` tồn tại.
2. `CI_COMMIT_BEFORE_SHA` tồn tại; nếu zero SHA thì thử `HEAD^`.
3. Before commit và current commit tồn tại trong object database.
4. Before commit là ancestor của current commit.
5. `git diff --name-status -z --find-renames before head` chạy thành công.

Nếu một điều kiện fail, detector tạo fallback reason và chuyển `FULL_FALLBACK`.

#### Phân loại changed path

| Classification | Điều kiện | Kết quả |
|---|---|---|
| `GLOBAL` | Khớp `I18N_GLOBAL_GLOBS` | Thêm fallback reason |
| `IRRELEVANT` | Khớp `I18N_IRRELEVANT_GLOBS` | Không chọn module |
| `UNKNOWN` | Không xác định owner module | Thêm fallback reason |
| `OUT_OF_SCOPE` | Thuộc module noninstallable/excluded | Không chọn module |
| `LOCAL` | Thuộc managed module | Thêm direct module |

Owner module được chọn bằng module path dài nhất khớp với changed path, vì vậy module lồng nhau được ưu tiên đúng scope.

#### Force mode

Nếu `I18N_FORCE_MODULES` không rỗng:

- parse danh sách theo comma/whitespace;
- kiểm tra mọi module có trong managed module set;
- module thiếu, excluded hoặc noninstallable làm job fail;
- đặt `impact_mode=FORCED`;
- bỏ qua Git diff để tạo direct/export module set.

#### Normal mode

Nếu không force:

| Mode | Điều kiện | Initial export set |
|---|---|---|
| `NO_RELEVANT_CHANGE` | Không có fallback reason và không có direct module | Rỗng; exit trước DB |
| `CHANGED_MODULES` | Có direct module và không có fallback reason | Direct modules |
| `FULL_FALLBACK` | Có global/unknown/Git fallback reason | Tất cả managed modules |

### 4.6. Impact policy và Manifestoo

Block `case "$I18N_IMPACT_POLICY"` tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:862-921` hỗ trợ:

| Policy | Behavior |
|---|---|
| `strict-local` | Giữ initial export set; không mở rộng reverse dependency |
| `conservative` | Nếu mode khác `FULL_FALLBACK`, gọi Manifestoo `list-codepends --transitive --include-selected` và union các codependent managed modules vào export set |
| Giá trị khác | Fail với danh sách supported values |

`FULL_FALLBACK` không gọi reverse dependency expansion vì export set đã là toàn bộ managed modules.

Sau policy expansion, job dùng Manifestoo để:

1. `list-missing`: fail nếu thiếu dependency.
2. `list-depends --transitive --include-selected`: tạo install module set.
3. Reject empty export/install set.

### 4.7. Early exit cho irrelevant-only diff

Nếu `EXPORT_MODULES_FILE` rỗng tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:814-831`:

- ghi `impact_mode`, policy và commit range vào summary;
- ghi rõ `NO RELEVANT CHANGE`;
- không kiểm tra `msgfmt` export commands;
- không tạo database;
- không gọi Odoo;
- không commit/push;
- exit `0`.

Đây là path xử lý commit chỉ thay đổi PO/POT, docs, `.build/**` hoặc file irrelevant khác.

### 4.8. Dependency preflight

Nếu có export module, job kiểm tra:

```text
msgfmt
psql
pg_isready
createdb
dropdb
git
realpath
comm
```

Sau đó kiểm tra:

- `ODOO_CORE_ROOT` tồn tại;
- `ODOO_BIN` readable;
- Odoo core addons tồn tại;
- `MANIFESTOO_BIN` executable;
- import `odoo` bằng `$ODOO_PYTHON`;
- Manifestoo version có thể query.

### 4.9. Temporary PostgreSQL database

Database lifecycle tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:997-1078`:

1. Validate `TEMP_DB` chỉ chứa `[A-Za-z0-9_]`.
2. `pg_isready` kiểm tra PostgreSQL.
3. `psql SELECT 1` kiểm tra credential.
4. Query `pg_roles.rolcreatedb`; fail nếu role không có `CREATEDB`.
5. Terminate session cũ cùng tên DB.
6. `dropdb --if-exists`.
7. `createdb --template=template0 --encoding=UTF8`.
8. Tạo marker `.ci-i18n/db-created`.
9. Query `current_database(), current_user`.

### 4.10. Install và export Odoo

Install dependency/module tại block bắt đầu khoảng `/home/linh/odoo-qms/pipelines/i18n-test.yml:1078`:

```bash
"$ODOO_PYTHON" "$ODOO_BIN" \
  --db_host="$ODOO_DB_HOST" \
  --db_port="$ODOO_DB_PORT" \
  --db_user="$ODOO_DB_USER" \
  --db_password="$ODOO_DB_PASSWORD" \
  --database="$TEMP_DB" \
  --addons-path="$ADDONS_PATH" \
  --data-dir="$ODOO_DATA_DIR" \
  --init="$install_modules_csv" \
  --without-demo=all \
  --no-http \
  --stop-after-init \
  --log-level=error
```

Mỗi export module dùng:

```bash
"$ODOO_PYTHON" "$ODOO_BIN" \
  --database="$TEMP_DB" \
  --addons-path="$ADDONS_PATH" \
  --data-dir="$ODOO_DATA_DIR" \
  --i18n-export="$temporary_pot" \
  --modules="$module_name" \
  --no-http \
  --stop-after-init \
  --log-level=error
```

Nếu install hoặc export fail, job exit `1` trước commit/push.

### 4.11. POT normalization và validation

`normalize_and_validate_pot` tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:1092-1167`:

1. Đọc POT tạm do Odoo sinh.
2. Lấy `POT-Creation-Date`/`PO-Revision-Date` từ POT tracked trước đó.
3. Nếu file mới, dùng timestamp cố định `1970-01-01 00:00+0000`.
4. Ghi candidate đã normalize để tránh diff do timestamp.
5. Reject entry ngoài header có `msgstr` không rỗng.
6. Chạy `msgfmt --check --check-format`.
7. Chỉ khi pass mới move candidate vào `<module>/i18n/<module>.pot`.

### 4.12. Stage boundary và changed-file guard

Sau export:

1. Ghi danh sách file generated vào `generated-pot-files.txt`.
2. `git add -f` chỉ các generated POT.
3. Reject staged file không khớp `*/i18n/*.pot`.
4. So sánh staged list với generated list bằng `comm`.
5. Kiểm tra tracked changes ngoài POT bằng cách hợp nhất `git diff --name-only` và `git diff --cached --name-only`.
6. Nếu có file ngoài scope, job fail.
7. Tạo `i18n.patch` và summary.

Job không được force-add PO hoặc source file.

### 4.13. Commit và push

Commit/push block tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:1318-1391`.

#### Không có POT diff

```text
changed_count == 0
→ git reset generated POT
→ không commit
→ không push
→ exit 0
```

#### Push bị disable

```text
I18N_PUSH_ENABLED != true
→ giữ POT staged để inspect
→ không commit/push
```

#### Push enabled

1. Xác định `push_branch` từ `I18N_PUSH_BRANCH`, fallback `CI_COMMIT_BRANCH`/`CI_COMMIT_REF_NAME`.
2. Reject nếu branch hiện tại khác target branch.
3. Reject nếu `I18N_COMMIT_MESSAGE` không chứa `[skip ci]`.
4. Set Git identity từ `I18N_GIT_USER_*`.
5. `git commit --only` trên generated POT list.
6. Require `CI_JOB_TOKEN` và `CI_PROJECT_URL`.
7. Tạo temporary `GIT_ASKPASS` trong `.ci-i18n`.
8. Set remote URL không chứa credential.
9. Push:

   ```bash
   git push origin HEAD:refs/heads/dev
   ```

10. Xóa askpass file sau push.

Không có force-push. Nếu push fail, job fail và ghi log.

### 4.14. After script và artifact

`after_script` tại `/home/linh/odoo-qms/pipelines/i18n-test.yml:1393-1454` luôn chạy với `set +e`:

1. Nếu có DB marker, terminate session và drop temporary DB.
2. Xóa DB marker.
3. Restore generated POT về `HEAD` để Shell Runner sạch.
4. Xóa `.odoo-data` và thư mục export tạm.
5. Xóa askpass còn sót.
6. Giữ diagnostics để upload artifact.

Artifact:

```text
.ci-i18n/impact-analysis.txt
.ci-i18n/changed-files.txt
.ci-i18n/dependency.log
.ci-i18n/export.log
.ci-i18n/validation.log
.ci-i18n/i18n-summary.txt
.ci-i18n/i18n.patch
.ci-i18n/cleanup.log
```

## 5. Dependency và runner setup

### 5.1. `validate-i18n`

Required:

```text
git
msgfmt      # GNU gettext package
python3
bash/coreutils
```

Không cần Odoo/PostgreSQL.

### 5.2. `export-i18n`

Required commands được preflight trong YAML:

```text
msgfmt
psql
pg_isready
createdb
dropdb
git
find
realpath
comm
```

Required runtime:

```text
Odoo 18 source/runtime
Python virtualenv của odoo-qms
Manifestoo pinned version
PostgreSQL server và role có CREATEDB
GitLab CI job token có quyền push dev
```

### 5.3. Runner mapping khi đưa vào May10

| Pilot | Target May10 |
|---|---|
| `qms-local-shell` | Dedicated May10 i18n shell runner hoặc runner có cùng runtime |
| Hard-coded `/home/linh/odoo-18` | Project/runner variable |
| `odoo_ci` local role | Secret/role được cấp riêng cho CI |
| `resource_group: qms-i18n` | Tên thống nhất cấp project, ví dụ `may10-qms-i18n` |
| Standalone `stages: [i18n]` | Include stage vào `build → quality → test → i18n → deploy → recovery` |

## 6. Cách chuyển từ pilot vào May10 QMS

### 6.1. Không copy nguyên YAML pilot

Tách cấu hình thành:

```text
templates/i18n-cicd.yml
├── validate-i18n
└── export-i18n

scripts/validate-i18n.sh
scripts/export-i18n.sh
```

Trong bước đầu có thể giữ inline script để đối chiếu output pilot. Sau khi behavior ổn định mới tách script để giảm kích thước template.

### 6.2. Thay đổi `pipelines/may10-qms.yml`

1. Include template i18n.
2. Thêm stage `i18n` sau `test`.
3. Truyền Odoo/Manifestoo/PostgreSQL variables của May10.
4. Truyền `I18N_IRRELEVANT_GLOBS` theo layout May10.
5. Chọn runner tag cho từng job.
6. Cài `gettext` vào image/runner của `validate-i18n`.
7. Cấu hình resource group.
8. Cấu hình policy source cho MR PO/POT.
9. Cấp quyền CI job token push vào `dev`.

### 6.3. Rule target cần chốt

Pilot hiện chỉ loại MR bằng `CI_PIPELINE_SOURCE`; target nên dùng rule rõ hơn cho post-merge push:

```yaml
export-i18n:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: never
    - if: '$CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH == "dev"'
      when: on_success
    - when: never
```

Điều này ngăn web/manual pipeline trên `dev` gọi export ngoài post-merge flow.

### 6.4. Policy target

Pilot để policy off vì source project/branch của MR translation chưa được chốt. Khi đã chốt:

```yaml
I18N_ENFORCE_PO_POLICY: "true"
I18N_ALLOWED_PO_SOURCE_PROJECT: "<approved-project>"
I18N_ALLOWED_PO_SOURCE_BRANCH_PREFIX: "<approved-prefix>"
```

Không hard-code branch prefix nếu chưa xác nhận từ GitLab/Weblate integration thực tế.

## 7. Test procedure dựa trên YAML

### 7.1. Static checks

```bash
python3 - <<'PY'
import yaml
from pathlib import Path

path = Path("/home/linh/odoo-qms/pipelines/i18n-test.yml")
data = yaml.safe_load(path.read_text())
assert "validate-i18n" in data
assert "export-i18n" in data
assert data["validate-i18n"]["stage"] == "i18n"
assert data["export-i18n"]["stage"] == "i18n"
PY
```

Kiểm tra thêm:

- `resource_group` của hai job;
- `rules` cho MR/`dev`;
- `msgfmt` tồn tại trên runner;
- Odoo/Manifestoo/PostgreSQL tồn tại trên export runner.

### 7.2. `validate-i18n` test cases

| Test | Cách chạy | Expected |
|---|---|---|
| Source-only MR | MR không đổi PO/POT | Job skip |
| PO hợp lệ | MR đổi PO hợp lệ | `msgfmt` + placeholder pass |
| POT hợp lệ | MR đổi POT hợp lệ | `msgfmt` pass |
| PO syntax lỗi | Tạo entry quote/header lỗi | Job fail tại `msgfmt` |
| Placeholder mismatch | Đổi `msgstr` làm mất `%s`/`{name}` | Job fail tại Python checker |
| Policy fail | Bật policy, dùng source branch không hợp lệ | Job fail trước `msgfmt` |
| Policy pass | Bật policy, project/branch khớp | Job tiếp tục validation |

### 7.3. `export-i18n` test cases

| Test | Input | Expected |
|---|---|---|
| PO/POT-only diff | Chỉ đổi `*.po`/`*.pot` | `NO_RELEVANT_CHANGE`, không DB/Odoo |
| Irrelevant-only diff | Docs/`.build/**`/CI metadata | Không DB/Odoo |
| Local module change | Đổi source trong managed module | `CHANGED_MODULES` |
| Unknown/global change | Đổi path không owner hoặc global glob | `FULL_FALLBACK` |
| Forced module | Set `I18N_FORCE_MODULES` | `FORCED`, validate module tồn tại |
| Strict local | `I18N_IMPACT_POLICY=strict-local` | Chỉ direct modules |
| Conservative | `I18N_IMPACT_POLICY=conservative` | Direct + Manifestoo transitive codependents |
| Invalid policy | Giá trị khác supported values | Job fail |
| POT unchanged | Odoo output không tạo staged diff | Không commit/push |
| POT changed, push off | `I18N_PUSH_ENABLED=false` | POT staged, không push |
| POT changed, push on | CI token/remote hợp lệ | Bot commit `[skip ci]` vào `dev` |
| Push guard | Target branch khác current branch | Job fail, không push |
| Export failure | Odoo/DB/Manifestoo fail | Không deploy tiếp, cleanup chạy |

### 7.4. Expected artifact inspection

Sau mỗi job kiểm tra:

```text
validate:
  .ci-i18n-validate/validation.log
  .ci-i18n-validate/placeholder.log
  .ci-i18n-validate/summary.txt

export:
  .ci-i18n/impact-analysis.txt
  .ci-i18n/dependency.log
  .ci-i18n/export.log
  .ci-i18n/i18n-summary.txt
  .ci-i18n/i18n.patch
  .ci-i18n/cleanup.log
```

## 8. Pilot/target differences cần xử lý

| Item | Pilot hiện tại | Target May10 |
|---|---|---|
| Stage list | Chỉ `i18n` | Merge `i18n` vào stage list đầy đủ |
| Runner tag | `qms-local-shell` | Dedicated runner theo May10 |
| Resource group | `qms-i18n` | Tên thống nhất cấp project |
| Export rule | Branch `dev`, MR bị loại | Nên giới hạn `push + dev` |
| PO policy | Off mặc định | Bật sau khi chốt source identity |
| Runtime paths | Hard-coded local path | Project/runner variables/secrets |
| Job source | Inline trong pilot YAML | Template + scripts dùng chung |
| Push credential | CI job token qua askpass | Protected/minimum scope token |

Các khác biệt này không thay đổi logic hai job; chúng là configuration step khi promote pilot thành May10 implementation.

## 9. Implementation checklist

- [ ] YAML pilot có đủ `validate-i18n` và `export-i18n`.
- [ ] `msgfmt` có trên validation runner.
- [ ] Odoo/Python/Manifestoo/PostgreSQL preflight pass trên export runner.
- [ ] `GIT_DEPTH=0` và diff base hoạt động.
- [ ] `I18N_IRRELEVANT_GLOBS` chứa PO/POT và file irrelevant của May10.
- [ ] `NO_RELEVANT_CHANGE` không tạo database.
- [ ] `strict-local`, `conservative`, `FULL_FALLBACK` được test.
- [ ] Output ngoài generated POT bị reject.
- [ ] Commit bot có `[skip ci]`, không force-push.
- [ ] Cleanup không để residue trên Shell Runner.
- [ ] Stage `i18n` nằm trước deploy trong May10.
- [ ] Policy source của MR PO/POT được cấu hình trước khi bật enforcement.
- [ ] Toàn bộ test matrix pass trước khi merge template vào May10.
