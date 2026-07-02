import functools

def demo_function_as_object():

    def greet(name):
        return f'Hello, {name}'
    greet_fn = greet
    print('Function assignment identity:', greet_fn is greet)

    def execute_fn(fn, val):
        return fn(val)
    print('Function passed as argument:', execute_fn(greet, 'Alice'))

def simple_decorator(func):

    def wrapper():
        result = func()
        return result.upper()
    return wrapper

def demo_simple_decorator():

    @simple_decorator
    def get_greeting():
        return 'hello world'
    print('Simple decorator result:', get_greeting())

def decorator_with_args(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_str = ', '.join(map(str, args))
        res = func(*args, **kwargs)
        return f'Called with ({arg_str}) -> {res}'
    return wrapper

def demo_decorator_with_args():

    @decorator_with_args
    def add(a, b):
        return a + b
    print('Decorator with args:', add(5, 10))
    print('Name preservation via wraps:', add.__name__)

def repeat(num_times):

    def decorator_repeat(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(num_times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator_repeat

def demo_parameterized_decorator():

    @repeat(num_times=3)
    def greet_once(name):
        return f'Hi {name}'
    print('Parameterized decorator result:', greet_once('Bob'))

def main():
    demo_function_as_object()
    print('---')
    demo_simple_decorator()
    print('---')
    demo_decorator_with_args()
    print('---')
    demo_parameterized_decorator()
if __name__ == '__main__':
    main()
