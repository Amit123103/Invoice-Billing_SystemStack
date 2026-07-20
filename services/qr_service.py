import qrcode
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
