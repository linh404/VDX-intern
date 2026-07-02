def demo_basic_slicing():
    lst = [10, 20, 30, 40, 50]
    print('Basic slicing [1:4]:', lst[1:4])
    print('Basic slicing [:3]:', lst[:3])
    print('Basic slicing [2:]:', lst[2:])

def demo_steps():
    lst = [10, 20, 30, 40, 50, 60, 70]
    print('Slice with step 2:', lst[0:6:2])
    print('Slice with negative step -1:', lst[::-1])
    print('Slice with negative step -2:', lst[6:1:-2])

def demo_string_slicing():
    text = 'PythonDeepDive'
    print('String slice [6:10]:', text[6:10])
    print('String reverse:', text[::-1])

def demo_shallow_copy():
    lst = [[1, 2], [3, 4]]
    copied_lst = lst[:]
    print('Shallow copy identities:')
    print('  Distinct top-level container:', copied_lst is not lst)
    print('  Identical nested containers:', copied_lst[0] is lst[0])
    copied_lst[0].append(99)
    print('  Modification in nested container affects original:')
    print('    original:', lst)
    print('    copied:', copied_lst)

def main():
    demo_basic_slicing()
    print('---')
    demo_steps()
    print('---')
    demo_string_slicing()
    print('---')
    demo_shallow_copy()
if __name__ == '__main__':
    main()
