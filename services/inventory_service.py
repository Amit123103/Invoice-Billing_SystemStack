from database.queries import DatabaseQueries

class InventoryService:
    def __init__(self):
        self.db = DatabaseQueries()

    def add_stock(self, product_id, amount, user_id):
        self.db.update_stock(product_id, amount, user_id, "Added Stock")
        
    def get_low_stock_alerts(self, threshold=10):
        products = self.db.get_all("products")
        return [p for p in products if p['stock_quantity'] <= threshold]
