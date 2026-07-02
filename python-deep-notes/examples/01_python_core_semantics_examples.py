def demo_assignment_binding():
    a = [1, 2, 3]
    b = a
    b.append(4)
    print('Assignment binding identical reference:', a is b, a == b)

def demo_identity_equality():
    x = [1, 2, 3]
    y = [1, 2, 3]
    print('Identity vs Equality (distinct lists):', x is y, x == y)
    small_int1 = 256
    small_int2 = 256
    print('Identity vs Equality (cached ints):', small_int1 is small_int2, small_int1 == small_int2)
    large_int1 = 1000000
    large_int2 = 1000000
    print('Identity vs Equality (non-cached ints):', large_int1 is large_int2, large_int1 == large_int2)

def demo_mutable_immutable():
    lst = [1, 2, 3]
    tup = (1, 2, 3)
    old_lst_id = id(lst)
    lst.append(4)
    new_lst_id = id(lst)
    print('Mutable object identity preserved:', old_lst_id == new_lst_id)
    old_tup_id = id(tup)
    tup = tup + (4,)
    new_tup_id = id(tup)
    print('Immutable object identity changed:', old_tup_id != new_tup_id)

class CustomTruthy:

    def __init__(self, value):
        self.value = value

    def __bool__(self):
        return bool(self.value)

def demo_truthy_falsy():
    print('Truthy/Falsy check:')
    print('None:', bool(None))
    print('Empty list:', bool([]))
    print('Empty string:', bool(''))
    print('Zero:', bool(0))
    print('Custom Truthy (True):', bool(CustomTruthy(True)))
    print('Custom Truthy (False):', bool(CustomTruthy(False)))
glob_var = 10

def demo_scopes():
    global glob_var
    glob_var += 5
    outer_var = 20

    def inner_func():
        nonlocal outer_var
        outer_var += 10
        local_var = 5
        print('Inner scopes:', glob_var, outer_var, local_var)
    inner_func()
    print('Outer scope after modification:', outer_var)

def main():
    demo_assignment_binding()
    print('---')
    demo_identity_equality()
    print('---')
    demo_mutable_immutable()
    print('---')
    demo_truthy_falsy()
    print('---')
    demo_scopes()
if __name__ == '__main__':
    main()
