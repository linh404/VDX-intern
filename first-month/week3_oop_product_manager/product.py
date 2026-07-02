# ==========================================
# Week 3 - OOP: Class Product
# ==========================================

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_total_value(self):
        return self.price * self.quantity

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

    def __str__(self):
        return f"{self.name} - Giá: {self.price} - SL: {self.quantity}"
