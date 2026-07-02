import inspect

def demo_args_kwargs():
    print("1. Demonstration of *args and **kwargs:")
    def sum_numbers(*args):
        print("  Arguments tuple (args):", args)
        return sum(args)

    def print_info(**kwargs):
        print("  Arguments dict (kwargs):", kwargs)

    total = sum_numbers(1, 2, 3, 4)
    print("  Sum result:", total)
    print_info(name="Linh", age=20, role="Intern")
    print()

def demo_argument_control():
    print("2. Demonstration of Positional-only (/) and Keyword-only (*) control:")
    # name: positional-only, greeting: positional-or-keyword, tax_rate: keyword-only
    def greet_and_tax(name, /, greeting="Hello", *, tax_rate):
        return f"{greeting}, {name}. Tax rate is {tax_rate}."

    # Valid calls
    res1 = greet_and_tax("Linh", tax_rate=0.1)
    res2 = greet_and_tax("Linh", "Hi", tax_rate=0.1)
    print("  Call 1 (positional name, keyword tax_rate):", res1)
    print("  Call 2 (positional name and greeting, keyword tax_rate):", res2)

    # Invalid call checks (wrapped in try-except to show verification)
    try:
        greet_and_tax(name="Linh", tax_rate=0.1) # Error: name is positional-only
    except TypeError as e:
        print("  Caught expected error (passing keyword to positional-only):", e)

    try:
        greet_and_tax("Linh", "Hi", 0.1) # Error: tax_rate is keyword-only
    except TypeError as e:
        print("  Caught expected error (passing positional to keyword-only):", e)
    print()

def demo_signature_introspection():
    print("3. Demonstration of inspect.signature:")
    def process_data(user_id: int, status: str = "active", *, force: bool = False) -> bool:
        return True

    sig = inspect.signature(process_data)
    print("  Function signature:", sig)
    print("  Return annotation:", sig.return_annotation)
    for name, param in sig.parameters.items():
        print(f"  Parameter: {name}")
        print(f"    Kind: {param.kind}")
        print(f"    Annotation: {param.annotation}")
        print(f"    Default value: {param.default}")
    print()

def main():
    demo_args_kwargs()
    print("---")
    demo_argument_control()
    print("---")
    demo_signature_introspection()

if __name__ == '__main__':
    main()
