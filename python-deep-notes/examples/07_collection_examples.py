class CustomRange:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        val = self.current
        self.current += 1
        return val

def demo_iterable_iterator():
    custom_seq = CustomRange(1, 4)
    print('Custom Iterable Iteration:')
    for num in custom_seq:
        print(' ', num)
    iterator_obj = iter(CustomRange(10, 13))
    print('Manual Iterator next calls:')
    print(' ', next(iterator_obj))
    print(' ', next(iterator_obj))
    print(' ', next(iterator_obj))
    try:
        next(iterator_obj)
    except StopIteration:
        print('  StopIteration caught successfully')

def demo_comprehensions():
    lst_comp = [x * 2 for x in range(3)]
    dict_comp = {x: x ** 2 for x in range(3)}
    set_comp = {x % 2 for x in [1, 2, 3, 4]}
    print('Comprehensions:', lst_comp, dict_comp, set_comp)

def demo_enumerate_zip():
    items = ['apple', 'banana', 'cherry']
    print('Enumerate:')
    for idx, item in enumerate(items):
        print(' ', idx, item)
    prices = [1.2, 0.5, 2.5]
    print('Zip:')
    for item, price in zip(items, prices):
        print(' ', item, price)

def demo_sorted_key():
    data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}, {'name': 'Charlie', 'age': 35}]
    sorted_by_age = sorted(data, key=lambda x: x['age'])
    print('Sorted by key:', sorted_by_age)

def main():
    demo_iterable_iterator()
    print('---')
    demo_comprehensions()
    print('---')
    demo_enumerate_zip()
    print('---')
    demo_sorted_key()
if __name__ == '__main__':
    main()
