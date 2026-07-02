def demo_iterable_types():
    print('1. Duyệt qua các loại Iterable phổ biến:')
    numbers = [1, 2, 3]
    names = ('An', 'Binh')
    text = 'hi'
    unique_numbers = {4, 5}
    user = {'name': 'Linh'}
    print('Duyệt list:')
    for num in numbers:
        print(num, end=' ')
    print('\nDuyệt tuple:')
    for name in names:
        print(name, end=' ')
    print('\nDuyệt string:')
    for char in text:
        print(char, end=' ')
    print('\nDuyệt set:')
    for item in unique_numbers:
        print(item, end=' ')
    print('\nDuyệt dict keys:')
    for key in user:
        print(key, end=' ')
    print('\n')

def demo_iterator_creation_and_next():
    print('2. Tạo Iterator từ List và dùng next():')
    numbers = [10, 20, 30]
    it = iter(numbers)
    print('Type of numbers:', type(numbers))
    print('Type of iterator:', type(it))
    print('next(it):', next(it))
    print('next(it):', next(it))
    print('next(it):', next(it))
    print('\nThử gọi next() trực tiếp trên list:')
    try:
        next(numbers)
    except TypeError as e:
        print('Lỗi TypeError thành công:', e)
    print()

def demo_stop_iteration():
    print('3. Minh họa lỗi StopIteration khi hết phần tử:')
    numbers = [1, 2]
    it = iter(numbers)
    print('Lấy 1:', next(it))
    print('Lấy 2:', next(it))
    try:
        print('Lấy 3 (hết phần tử):')
        next(it)
    except StopIteration:
        print('Bắt được ngoại lệ StopIteration thành công!')
    print()

def demo_for_loop_under_the_hood():
    print('4. Giả lập cơ chế vòng lặp for bằng while + next() + StopIteration:')
    numbers = [100, 200, 300]
    it = iter(numbers)
    while True:
        try:
            item = next(it)
            print('Item:', item)
        except StopIteration:
            print('Đã gặp StopIteration -> Kết thúc vòng lặp.')
            break
    print()

def demo_iterator_stateful_nature():
    print('5. Tính chất có trạng thái và một chiều của Iterator:')
    numbers = [10, 20, 30]
    it = iter(numbers)
    print('Duyệt 2 phần tử đầu:')
    print('next(it):', next(it))
    print('next(it):', next(it))
    print('Duyệt phần tử cuối cùng:')
    print('next(it):', next(it))
    try:
        next(it)
    except StopIteration:
        print('Iterator đã cạn kiệt, không thể duyệt lại.')
    it_new = iter(numbers)
    print('Tạo iterator mới và duyệt phần tử đầu:', next(it_new))
    print()

def main():
    demo_iterable_types()
    print('-' * 40)
    demo_iterator_creation_and_next()
    print('-' * 40)
    demo_stop_iteration()
    print('-' * 40)
    demo_for_loop_under_the_hood()
    print('-' * 40)
    demo_iterator_stateful_nature()
if __name__ == '__main__':
    main()
