import unittest
from product import Product

class TestProduct(unittest.TestCase):
    
    def test_product_initialization(self):
        p = Product("Test", 100, 2)
        self.assertEqual(p.name, "Test")
        self.assertEqual(p.price, 100)
        self.assertEqual(p.quantity, 2)
        
    def test_get_total_value(self):
        p = Product("Test", 100, 2)
        self.assertEqual(p.get_total_value(), 200)
        
    def test_to_dict(self):
        p = Product("Test", 100, 2)
        d = p.to_dict()
        self.assertEqual(d["name"], "Test")
        self.assertEqual(d["price"], 100)
        self.assertEqual(d["quantity"], 2)

if __name__ == '__main__':
    unittest.main()
