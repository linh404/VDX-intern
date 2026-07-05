class User:
    default_role = "user"

    def __init__(self, name, role):
        self.name = name
        self.role = role

    @classmethod
    def create_default(cls, name):
        # cls sẽ linh động trỏ về User, Admin hoặc Staff tùy thuộc vào class gọi nó
        return cls(name, cls.default_role)

    @classmethod
    def create_default_by_user_class(cls, name):
        # Ghi thẳng User thì dù Admin/Staff gọi, kết quả vẫn là User
        return User(name, User.default_role)

    @classmethod
    def change_role_by_current_class(cls, name):
        # cls là class đang gọi method
        cls.default_role = name

    @classmethod
    def change_role_by_user_class(cls, name):
        # Ghi thẳng User thì luôn đổi class cha User
        User.default_role = name


class Admin(User):
    default_role = "admin"


class Staff(User):
    default_role = "staff"



# Gọi khởi tạo qua classmethod
user = User.create_default("An")  # Tạo User(name="An", role="user")
admin = Admin.create_default("Bình")  # Tạo Admin(name="Bình", role="admin")
staff = Staff.create_default("Cường")  # Tạo Staff(name="Cường", role="staff")

print("--- Dùng cls trong return ---")
print(type(user).__name__, user.role)
print(type(admin).__name__, admin.role)
print(type(staff).__name__, staff.role)

staff_created_by_user = Staff.create_default_by_user_class("Dũng")

print("\n--- Ghi thẳng User trong return ---")
print(type(staff_created_by_user).__name__, staff_created_by_user.role)

print("\n--- Dùng cls để đổi class đang gọi ---")
Staff.change_role_by_current_class("staff changed")
print("User.default_role:", User.default_role)
print("Admin.default_role:", Admin.default_role)
print("Staff.default_role:", Staff.default_role)

print("\n--- Ghi thẳng User để đổi class cha ---")
Staff.change_role_by_user_class("user changed")
print("User.default_role:", User.default_role)
print("Admin.default_role:", Admin.default_role)
print("Staff.default_role:", Staff.default_role)
