from database.queries import DatabaseQueries
from models.invoice import Invoice, InvoiceItem

class BillingService:
    def __init__(self):
        self.db = DatabaseQueries()

    def generate_invoice(self, data, items):
        invoice_id = self.db.create_invoice(data)
        for item in items:
            self.db.add_invoice_item(invoice_id, item)
            self.db.update_stock(item['product_id'], -item['quantity'], data.get('created_by'))
        return invoice_id
