def demo_parameter_vs_argument():
    print("1. Parameter và argument")

    def greet(name, age):
        print("name =", name)
        print("age =", age)

    greet("Linh", 20)

    print("name, age là parameter vì nằm trong phần định nghĩa hàm.")
    print('"Linh", 20 là argument vì là giá trị truyền vào khi gọi hàm.')
    print()


def demo_positional_argument():
    print("2. Positional argument")

    def create_user(name, age):
        print("name =", name)
        print("age =", age)

    create_user("Linh", 20)

    print("Python map theo vị trí:")
    print('name = "Linh"')
    print("age = 20")
    print()


def demo_keyword_argument():
    print("3. Keyword argument")

    def create_user(name, age):
        print("name =", name)
        print("age =", age)

    create_user(age=20, name="Linh")

    print("Python map theo tên parameter, nên đảo thứ tự vẫn đúng:")
    print('name = "Linh"')
    print("age = 20")
    print()


def demo_args():
    print("4. *args")

    def demo(a, b, *args):
        print("a =", a)
        print("b =", b)
        print("args =", args)

    demo(1, 2, 3, 4, 5)

    print("1 được map vào a.")
    print("2 được map vào b.")
    print("3, 4, 5 là positional arguments còn dư nên bị gom vào args.")
    print()


def demo_kwargs():
    print("5. **kwargs")

    def demo(a, b, **kwargs):
        print("a =", a)
        print("b =", b)
        print("kwargs =", kwargs)

    demo(a=1, b=2, name="Linh", age=20)

    print("a=1 được map vào parameter a.")
    print("b=2 được map vào parameter b.")
    print("name và age là keyword lạ nên bị gom vào kwargs.")
    print()


def demo_keyword_not_fall_into_kwargs():
    print("6. Keyword khớp parameter thì không rơi vào kwargs")

    def demo(a, b, **kwargs):
        print("a =", a)
        print("b =", b)
        print("kwargs =", kwargs)

    demo(b=1, a=2)

    print("b=1 map vào parameter b.")
    print("a=2 map vào parameter a.")
    print("Vì a và b đã có chỗ nhận riêng nên kwargs rỗng.")
    print()


def demo_keyword_only_after_args():
    print("7. Parameter sau *args là keyword-only")

    def demo(a, b, *args, c, d=10):
        print("a =", a)
        print("b =", b)
        print("args =", args)
        print("c =", c)
        print("d =", d)

    demo(1, 2, 3, 4, c=5, d=6)

    print("1 map vào a.")
    print("2 map vào b.")
    print("3, 4 bị gom vào args.")
    print("c đứng sau *args nên phải truyền bằng tên: c=5.")
    print("d đứng sau *args nên cũng truyền bằng tên: d=6.")
    print()

    print("Ví dụ sai:")
    try:
        demo(1, 2, 3, 4, 5)
    except TypeError as error:
        print(error)

    print("Số 5 bị gom vào args, không tự nhảy sang c được.")
    print()


def demo_keyword_only_without_args():
    print("8. Dấu * dùng để ép keyword-only")

    def calculate_tax(price, *, tax_rate):
        return price * tax_rate

    result = calculate_tax(100, tax_rate=0.1)
    print("calculate_tax(100, tax_rate=0.1) =", result)

    print("Ví dụ sai:")
    try:
        calculate_tax(100, 0.1)
    except TypeError as error:
        print(error)

    print("tax_rate đứng sau dấu * nên bắt buộc phải truyền bằng tên.")
    print()


def demo_positional_only():
    print("9. Dấu / dùng để ép positional-only")

    def greet(name, /, greeting="Hello"):
        return f"{greeting}, {name}"

    print(greet("Linh"))
    print(greet("Linh", greeting="Hi"))

    print("Ví dụ sai:")
    try:
        greet(name="Linh")
    except TypeError as error:
        print(error)

    print("name đứng trước dấu / nên chỉ được truyền bằng vị trí.")
    print()


def demo_unpacking_when_calling_function():
    print("10. * và ** khi gọi hàm là bung dữ liệu ra")

    def create_user(name, age, role):
        print("name =", name)
        print("age =", age)
        print("role =", role)

    data_tuple = ("Linh", 20)
    data_dict = {"role": "Intern"}

    create_user(*data_tuple, **data_dict)

    print("*data_tuple bung tuple thành positional arguments.")
    print("**data_dict bung dict thành keyword arguments.")
    print()


def main():
    demo_parameter_vs_argument()
    print("---")
    demo_positional_argument()
    print("---")
    demo_keyword_argument()
    print("---")
    demo_args()
    print("---")
    demo_kwargs()
    print("---")
    demo_keyword_not_fall_into_kwargs()
    print("---")
    demo_keyword_only_after_args()
    print("---")
    demo_keyword_only_without_args()
    print("---")
    demo_positional_only()
    print("---")
    demo_unpacking_when_calling_function()


if __name__ == "__main__":
    main()
