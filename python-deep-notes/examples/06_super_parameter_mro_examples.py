class A:

    def test(self):
        print('A.test')

class B(A):

    def test(self):
        print('B.test starting')
        super().test()
        print('B.test finished')

class C(A):

    def test(self):
        print('C.test starting')
        super().test()
        print('C.test finished')

class D(B, C):

    def test(self):
        print('D.test starting')
        super().test()
        print('D.test finished')

    def test_explicit(self):
        print('D.test_explicit starting')
        super(D, self).test()
        print('D.test_explicit finished')

def main():
    print('MRO of class D:')
    for cls in D.__mro__:
        print(' ', cls)
    print('---')
    print('Executing d.test() to show MRO routing:')
    d = D()
    d.test()
    print('---')
    print('Executing d.test_explicit() using super(D, self):')
    d.test_explicit()
if __name__ == '__main__':
    main()
