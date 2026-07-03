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


class PhysicalProduct(Product):
    def __init__(self, name, price, quantity, weight):
        super().__init__(name, price, quantity)
        self.weight = weight

    def to_dict(self):
        product_data = super().to_dict()
        product_data["weight"] = self.weight
        return product_data

    def shipping_info(self):
        return "Sản phẩm vật lý cần giao hàng"

    def __str__(self):
        return f"{super().__str__()} - Cân nặng: {self.weight} kg"


class DigitalProduct(Product):
    def __init__(self, name, price, quantity, file_size):
        super().__init__(name, price, quantity)
        self.file_size = file_size

    def to_dict(self):
        product_data = super().to_dict()
        product_data["file_size"] = self.file_size
        return product_data

    def download_info(self):
        return "Sản phẩm số có thể tải xuống"

    def __str__(self):
        return f"{super().__str__()} - Dung lượng: {self.file_size} MB"


class HybridProduct(PhysicalProduct, DigitalProduct):
    def __init__(self, name, price, quantity, weight, file_size):
        Product.__init__(self, name, price, quantity)
        self.weight = weight
        self.file_size = file_size

    def __str__(self):
        return (
            f"{self.name} - Giá: {self.price} - SL: {self.quantity} "
            f"- Cân nặng: {self.weight} kg - Dung lượng: {self.file_size} MB"
        )
