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
    def new_name(cls,name):
        cls.default_role=name



class Admin(User):
    default_role = "admin"


class Staff(User):
    default_role = "staff"



# Gọi khởi tạo qua classmethod
user = User.create_default("An")  # Tạo User(name="An", role="user")
admin = Admin.create_default("Bình")  # Tạo Admin(name="Bình", role="admin")
staff = Staff.create_default("Cường")  # Tạo Staff(name="Cường", role="staff")à

staff.new_name("name")
print("staff role: ", staff.default_role)
print("admin role: ", admin.default_role)
