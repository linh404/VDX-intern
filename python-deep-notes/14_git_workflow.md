# Git Workflow - Take Notes

Ghi chú về các lệnh Git đi làm hay dùng, tập trung vào staging, commit sạch, sửa commit, stash, rebase, cherry-pick, reflog và dọn file rác.

---

## 1. Khái niệm cơ bản

* **Working tree**: Là vùng code đang sửa trực tiếp trong project.
* **Staging area / Index**: Là vùng trung gian chứa những thay đổi chuẩn bị được đưa vào commit.
* **Commit history**: Là lịch sử các commit đã được lưu lại.
* **Remote branch**: Là branch trên server, ví dụ `origin/main`, `origin/feature/login`.
* **Local branch**: Là branch trên máy mình.

> **Phân biệt nhanh**: Code sửa trong file chưa chắc đã vào commit. Muốn vào commit thì thường phải qua bước `git add` để đưa vào staging.

---

## 2. Kiểm tra trạng thái trước khi làm gì

* **`git status`**: Xem trạng thái hiện tại của repo.

```bash
git status
```

Dùng để biết:

* Đang ở branch nào.
* File nào đã sửa.
* File nào đã stage.
* File nào chưa được Git track.
* Có đang rebase, merge, cherry-pick dở hay không.

> Đi làm nên có thói quen chạy `git status` rất thường xuyên.

---

## 3. Kiểm tra code thay đổi

* **`git diff`**: Xem thay đổi ở working tree, tức là code đã sửa nhưng chưa stage.

```bash
git diff
```

* **`git diff --staged`**: Xem thay đổi đã stage, tức là thứ chuẩn bị đi vào commit.

```bash
git diff --staged
```

Flow nên dùng trước khi commit:

```bash
git status
git diff
git add -p
git diff --staged
git commit -m "message"
```

> **Nhớ nhanh**: `git diff` xem cái chưa add, `git diff --staged` xem cái đã add.

---

## 4. Stage code trước khi commit

* **`git add -p`**: Chọn từng đoạn code để stage.

```bash
git add -p
```

Dùng khi một file có nhiều thay đổi nhưng chỉ muốn commit một phần.

Ví dụ trong cùng một file có:

```text
- sửa validate email
- thêm print debug
```

Ta có thể dùng `git add -p` để chỉ stage phần validate, không stage phần debug.

---

* **`git add -u`**: Stage các file đã được Git track.

```bash
git add -u
```

Nó stage:

```text
file đã sửa
file đã xóa
```

Nhưng không stage file mới.

Dùng khi project có nhiều file mới sinh ra, tránh add nhầm file rác.

---

* **`git add -A`**: Stage tất cả thay đổi.

```bash
git add -A
```

Bao gồm:

```text
file mới
file đã sửa
file đã xóa
```

Chỉ nên dùng khi đã kiểm tra kỹ bằng `git status`.

---

* **`git add -f`**: Force add file bị `.gitignore` chặn.

```bash
git add -f file_name
```

Ví dụ:

```bash
git add -f .env.example
```

Dùng khi file bị ignore bởi rule chung nhưng thật sự cần commit.

Không dùng để add:

```text
.env thật
password
token
private key
secret config
```

> **Phân biệt nhanh**: `git add -f` không phải add “mạnh hơn” cho mọi thứ. Nó chủ yếu dùng để ép Git add file đang bị `.gitignore` bỏ qua.

---

## 5. Gỡ nhầm khỏi staging

* **`git restore --staged file`**: Gỡ file khỏi staging.

```bash
git restore --staged file.py
```

Nó không xóa code, chỉ đưa file từ trạng thái staged về unstaged.

Ví dụ:

```bash
git add .
git restore --staged debug.py
git commit -m "Fix sale order validation"
```

> **Nhớ nhanh**: Lỡ `git add` nhầm thì dùng `git restore --staged`.

---

## 6. Sửa commit vừa tạo

* **`git commit --amend`**: Sửa commit cuối cùng.

Dùng khi commit xong mới phát hiện:

```text
thiếu file
message sai
cần sửa nhẹ commit cuối
```

Thêm file vào commit cuối:

```bash
git add missing_file.py
git commit --amend
```

Sửa message commit cuối:

```bash
git commit --amend -m "Fix sale order validation"
```

Lưu ý:

* Commit chưa push: dùng khá thoải mái.
* Commit đã push: cẩn thận vì `amend` làm đổi lịch sử commit.

> **Phân biệt nhanh**: `commit --amend` không tạo commit mới bình thường, mà thay commit cuối bằng một commit mới khác.

---

## 7. Tách lại commit

* **`git reset --mixed HEAD~1`**: Xóa commit cuối nhưng giữ lại code.

```bash
git reset --mixed HEAD~1
```

Ý nghĩa:

```text
xóa commit cuối
giữ code trong working tree
đưa code về trạng thái chưa stage
```

Dùng khi commit một cục quá to, muốn tách lại thành nhiều commit nhỏ.

Ví dụ:

```bash
git reset --mixed HEAD~1

git add -p
git commit -m "Fix validation"

git add -p
git commit -m "Add test"
```

> **Nhớ nhanh**: Muốn tách commit cuối thì thường dùng `git reset --mixed HEAD~1` rồi `git add -p` lại.

---

## 8. Cất code đang làm dở

* **`git stash push -u -m "message"`**: Cất tạm code đang sửa.

```bash
git stash push -u -m "wip sale order"
```

Trong đó:

* **`-u`**: Stash cả file mới chưa được Git track.
* **`-m`**: Đặt tên cho stash.

Xem danh sách stash:

```bash
git stash list
```

Lấy lại code đã stash:

```bash
git stash pop
```

Ví dụ thực tế:

```bash
git stash push -u -m "wip before rebase"
git pull --rebase
git stash pop
```

> **Phân biệt nhanh**: `stash` dùng khi đang code dở nhưng cần đổi branch, pull code mới, hoặc xử lý việc khác trước.

---

## 9. Rebase branch cá nhân với main

* **`git fetch origin`**: Lấy thông tin mới nhất từ remote.

```bash
git fetch origin
```

* **`git rebase origin/main`**: Đưa commit của branch hiện tại lên đầu `main` mới nhất.

```bash
git rebase origin/main
```

Hiểu đơn giản:

```text
main có code mới
branch mình có commit riêng
rebase = bê commit của mình đặt lên đầu main mới nhất
```

Nếu có conflict, sửa file conflict rồi chạy:

```bash
git add .
git rebase --continue
```

Nếu muốn hủy rebase:

```bash
git rebase --abort
```

Lưu ý:

* Branch cá nhân: có thể rebase.
* Branch dùng chung với người khác: phải cẩn thận.
* Không rebase bừa trên branch nhiều người cùng push.

> **Phân biệt nhanh**: `merge` thường tạo commit gộp, còn `rebase` viết lại vị trí commit của mình trên base mới.

---

## 10. Push sau khi amend hoặc rebase

* **`git push --force-with-lease`**: Push an toàn hơn sau khi sửa lịch sử commit.

```bash
git push --force-with-lease
```

Dùng sau khi:

```text
git commit --amend
git rebase
git rebase -i
```

Không nên dùng bừa:

```bash
git push --force
```

Vì `--force-with-lease` an toàn hơn, tránh ghi đè commit mới của người khác trên remote.

> **Nhớ nhanh**: Sau khi rebase hoặc amend mà push bị reject, thường dùng `git push --force-with-lease`, không dùng `--force` bừa.

---

## 11. Lấy một commit từ branch khác

* **`git cherry-pick commit_hash`**: Lấy riêng một commit từ branch khác sang branch hiện tại.

```bash
git cherry-pick commit_hash
```

Ví dụ:

```bash
git switch feature/sale-order
git cherry-pick abc123
```

Hay gặp khi leader bảo:

```text
Lấy commit fix bug kia sang branch này.
```

> **Phân biệt nhanh**: `merge` lấy cả nhánh, còn `cherry-pick` lấy riêng một commit.

---

## 12. Cứu lỗi bằng reflog

* **`git reflog`**: Xem lịch sử HEAD từng trỏ tới đâu.

```bash
git reflog
```

Dùng khi lỡ:

```text
reset nhầm
rebase hỏng
mất commit
checkout lung tung
```

Quay lại trạng thái cũ:

```bash
git reset --hard HEAD@{1}
```

Hoặc tạo branch cứu từ commit cũ:

```bash
git switch -c rescue-branch commit_hash
```

> **Nhớ nhanh**: Khi tưởng mất commit, đừng hoảng. Chạy `git reflog` trước.

---

## 13. Dọn file rác

* **`git clean -n`**: Xem trước file untracked nào sẽ bị xóa.

```bash
git clean -n
```

* **`git clean -fd`**: Xóa file/folder untracked.

```bash
git clean -fd
```

Dùng khi project sinh nhiều file rác sau khi build/test.

Cẩn thận:

```text
File bị xóa bằng git clean thường khó cứu.
Luôn chạy git clean -n trước khi chạy git clean -fd.
```

> **Phân biệt nhanh**: `git clean` xử lý file chưa được Git track, còn `git reset` thường xử lý file/commit đã được Git track.

---

## 14. Flow đi làm hay dùng

### Trước khi commit

```bash
git status
git diff
git add -p
git diff --staged
git commit -m "message"
```

---

### Lỡ add nhầm file

```bash
git restore --staged file.py
```

---

### Commit xong mới thiếu file

```bash
git add missing_file.py
git commit --amend
```

---

### Commit quá to, muốn tách lại

```bash
git reset --mixed HEAD~1
git add -p
git commit -m "Part 1"
git add -p
git commit -m "Part 2"
```

---

### Đang code dở cần đổi branch

```bash
git stash push -u -m "wip something"
git switch other-branch
```

Lấy lại:

```bash
git stash pop
```

---

### Update branch cá nhân theo main

```bash
git fetch origin
git rebase origin/main
```

Nếu conflict:

```bash
git add .
git rebase --continue
```

Nếu hủy:

```bash
git rebase --abort
```

---

### Sau khi rebase hoặc amend mà cần push

```bash
git push --force-with-lease
```

---

## 15. Danh sách lệnh cần nhớ

```bash
git status
git diff
git diff --staged

git add -p
git add -u
git add -A
git add -f

git restore --staged

git commit --amend
git reset --mixed HEAD~1

git stash push -u -m "..."
git stash list
git stash pop

git fetch origin
git rebase origin/main
git rebase --continue
git rebase --abort

git push --force-with-lease

git cherry-pick commit_hash

git reflog

git clean -n
git clean -fd
```

---

## 16. Chốt tư duy

Không cần học quá nhiều lệnh Git ngay từ đầu.

Đi làm nên tập trung vào:

* Commit sạch.
* Không add nhầm file rác.
* Biết sửa commit cuối.
* Biết tách commit.
* Biết stash khi đang code dở.
* Biết rebase branch cá nhân.
* Biết push an toàn sau rebase.
* Biết lấy riêng commit bằng cherry-pick.
* Biết cứu lỗi bằng reflog.
* Biết dọn file rác cẩn thận.

> **Nhớ cuối cùng**: Trước khi dùng lệnh nguy hiểm như `reset --hard`, `push --force`, `clean -fd`, luôn chạy `git status` và đọc kỹ mình đang ở branch nào, file nào đang thay đổi.

---

## 17. Ví dụ cần xem

[git_workflow_examples.md](file:///home/linh/VDX-intern/python-deep-notes/examples/git_workflow_examples.md)
