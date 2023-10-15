class ProductNotFound(Exception):
    def __init__(self, sku):
        self.sku = sku
        self.message = f"Product with SKU {sku} not found."
        super().__init__(self.message)