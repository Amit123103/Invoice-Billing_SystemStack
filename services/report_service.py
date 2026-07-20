from reportlab.pdfgen import canvas
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
