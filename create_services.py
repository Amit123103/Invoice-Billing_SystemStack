import os
services_dir = 'c:/Users/amita/myprojects/invoice_billing/services'
utils_dir = 'c:/Users/amita/myprojects/invoice_billing/utils'
os.makedirs(services_dir, exist_ok=True)
os.makedirs(utils_dir, exist_ok=True)

services = {
    "__init__.py": "",
    "billing_service.py": '''from database.queries import DatabaseQueries
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
''',
    "inventory_service.py": '''from database.queries import DatabaseQueries

class InventoryService:
    def __init__(self):
        self.db = DatabaseQueries()

    def add_stock(self, product_id, amount, user_id):
        self.db.update_stock(product_id, amount, user_id, "Added Stock")
        
    def get_low_stock_alerts(self, threshold=10):
        products = self.db.get_all("products")
        return [p for p in products if p['stock_quantity'] <= threshold]
''',
    "gst_service.py": '''class GSTService:
    @staticmethod
    def calculate_gst(amount, gst_percentage):
        tax = (amount * gst_percentage) / 100
        return {
            "cgst": tax / 2,
            "sgst": tax / 2,
            "igst": 0,
            "total": tax
        }
''',
    "qr_service.py": '''import qrcode
import hashlib
import os

class QRService:
    def __init__(self):
        self.qr_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'qrcodes')
        os.makedirs(self.qr_dir, exist_ok=True)

    def generate_qr(self, invoice_number, customer_name, amount):
        data = f"INV:{invoice_number}|CUST:{customer_name}|AMT:{amount}"
        qr_hash = hashlib.sha256(data.encode()).hexdigest()
        
        img = qrcode.make(f"{data}|HASH:{qr_hash}")
        path = os.path.join(self.qr_dir, f"{invoice_number}.png")
        img.save(path)
        return path, qr_hash
''',
    "report_service.py": '''from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

class ReportService:
    def __init__(self):
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_invoice_pdf(self, invoice_data, items_data, qr_path):
        filename = os.path.join(self.reports_dir, f"{invoice_data['invoice_number']}.pdf")
        c = canvas.Canvas(filename, pagesize=A4)
        c.drawString(100, 800, f"Invoice: {invoice_data['invoice_number']}")
        c.drawString(100, 780, f"Total Amount: {invoice_data['total_amount']}")
        if qr_path and os.path.exists(qr_path):
            c.drawImage(qr_path, 400, 700, width=100, height=100)
        c.showPage()
        c.save()
        return filename
''',
    "backup_service.py": '''import shutil
import os
import datetime

class BackupService:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        self.backup_dir = os.path.join(self.root_dir, 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
        self.db_path = os.path.join(self.root_dir, 'smart_erp.db')

    def create_backup(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.db")
        if os.path.exists(self.db_path):
            shutil.copy2(self.db_path, backup_file)
        return backup_file
''',
    "audit_service.py": '''from database.queries import DatabaseQueries

class AuditService:
    def __init__(self):
        self.db = DatabaseQueries()

    def log(self, user_id, action, target_type=None, target_id=None, details=None):
        self.db.log_audit(user_id, action, target_type, target_id, details)
'''
}

utils = {
    "__init__.py": "",
    "auth.py": '''import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed
'''
}

for name, content in services.items():
    with open(os.path.join(services_dir, name), 'w') as f:
        f.write(content)

for name, content in utils.items():
    with open(os.path.join(utils_dir, name), 'w') as f:
        f.write(content)







