def demo_basic_comprehension():
    print('1. Công thức cơ bản (Biến đổi danh sách):')
    numbers = [1, 2, 3, 4, 5]
    squares_loop = []
    for n in numbers:
        squares_loop.append(n * n)
    squares_comp = [n * n for n in numbers]
    print('Vòng lặp for truyền thống:', squares_loop)
    print('List Comprehension:', squares_comp)
    print()

def demo_filtering_if():
    print("2. Lọc danh sách bằng điều kiện 'if' ở cuối:")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    div_by_three = [n for n in numbers if n % 3 == 0]
    squares_of_evens = [n * n for n in numbers if n % 2 == 0]
    print('Số chia hết cho 3:', div_by_three)
    print('Bình phương các số chẵn:', squares_of_evens)
    print()

def demo_conditional_transformation_if_else():
    print("3. Quyết định giá trị trả về bằng 'if else' trước 'for':")
    numbers = [1, 2, 3, 4, 5]
    categorized = ['Big' if n > 3 else 'Small' for n in numbers]
    print('Phân loại (Big/Small):', categorized)
    print()

def demo_list_of_dicts():
    print('4. Xử lý danh sách chứa các dict:')
    users = [{'name': 'An', 'age': 20, 'active': True}, {'name': 'Binh', 'age': 17, 'active': True}, {'name': 'Cuong', 'age': 22, 'active': False}, {'name': 'Dung', 'age': 25, 'active': True}]
    active_adults = [user['name'] for user in users if user['age'] >= 18 and user['active']]
    print('User hoạt động và >= 18 tuổi:', active_adults)
    print()

def demo_immutability_of_source():
    print('5. Xác minh List Comprehension tạo danh sách mới và không sửa đổi danh sách gốc:')
    numbers = [1, 2, 3]
    scaled_numbers = [n * 10 for n in numbers]
    print('Danh sách gốc:', numbers, 'id:', id(numbers))
    print('Danh sách mới:', scaled_numbers, 'id:', id(scaled_numbers))
    print('Có chung id không?', id(numbers) == id(scaled_numbers))
    print()

def main():
    demo_basic_comprehension()
    print('-' * 40)
    demo_filtering_if()
    print('-' * 40)
    demo_conditional_transformation_if_else()
    print('-' * 40)
    demo_list_of_dicts()
    print('-' * 40)
    demo_immutability_of_source()
if __name__ == '__main__':
    main()
