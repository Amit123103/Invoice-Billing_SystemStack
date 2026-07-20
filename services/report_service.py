"""
File: report_service.py

Purpose:
Handles the generation of physical PDF documents like Invoices and Reports.

Dependencies:
- reportlab.pdfgen.canvas (To draw text/images onto a PDF)
- reportlab.lib.pagesizes.A4 (Standard paper sizing)
- os (For file paths)

"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

# This class manages PDF exports.
# It solves the problem of converting application data into printable, professional documents.
# Its responsibility is drawing text, lines, and images (like logos and QR codes) onto a digital canvas.
class ReportService:
    """
    Service class responsible for generating PDF documents using ReportLab.
    """
    
    def __init__(self):
        # Locate the 'reports' folder at the root of the project
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        # Create it if it doesn't exist
        os.makedirs(self.reports_dir, exist_ok=True)

    # Purpose:
    # Draws the final customer Invoice PDF document.
    #
    # Parameters:
    # invoice_data (dict): Header info (totals, customer ID).
    # items_data (list): The rows of purchased products.
    # qr_path (str): File path to the previously generated QR code image.
    #
    # Returns:
    # str: The absolute file path to the finished PDF.
    def generate_invoice_pdf(self, invoice_data, items_data, qr_path, output_path=None):
        """
        Generates a PDF invoice.

        Args:
            invoice_data (dict): The main invoice header data.
            items_data (list): The list of purchased items.
            qr_path (str): File path to the generated QR code image.
            output_path (str, optional): Target file path.

        Returns:
            str: Path to the generated PDF.
        """
        # Determine the file name based on the unique invoice number
        if output_path:
            filename = output_path
        else:
            filename = os.path.join(self.reports_dir, f"{invoice_data['invoice_number']}.pdf")
        
        # Initialize a new PDF canvas on standard A4 size paper
        c = canvas.Canvas(filename, pagesize=A4)
        
        # Draw the main title text near the top of the page (Coordinates: X=100, Y=800)
        c.drawString(100, 800, f"Invoice: {invoice_data['invoice_number']}")
        
        # Draw the total amount text slightly lower (Y=780)
        c.drawString(100, 780, f"Total Amount: {invoice_data['total_amount']}")
        
        # Check if a QR code image was successfully created and exists on the hard drive
        if qr_path and os.path.exists(qr_path):
            # Embed the QR image into the PDF on the right side (X=400)
            c.drawImage(qr_path, 400, 700, width=100, height=100)
            
        # Finalize the current page
        c.showPage()
        
        # Save the PDF to the hard drive
        c.save()
        
        # Return the path so the GUI can notify the user where the file is
        return filename

    def generate_business_report_pdf(self, metrics, invoices, output_path=None):
        """
        Generates a comprehensive business report PDF.
        """
        if not output_path:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.reports_dir, f"Business_Report_{timestamp}.pdf")
            
        c = canvas.Canvas(output_path, pagesize=A4)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, 800, "Smart ERP - Business Report")
        
        c.setFont("Helvetica", 14)
        c.drawString(50, 750, f"Total Revenue: {metrics['revenue']}")
        c.drawString(50, 730, f"Total Invoices: {metrics['invoices']}")
        c.drawString(50, 710, f"Total Customers: {metrics['customers']}")
        c.drawString(50, 690, f"Products in Stock: {metrics['products']}")
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 640, "Recent Invoices:")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 610, "Date")
        c.drawString(150, 610, "Invoice #")
        c.drawString(270, 610, "Customer")
        c.drawString(400, 610, "Amount")
        c.drawString(480, 610, "Status")
        
        c.setFont("Helvetica", 10)
        y = 590
        for inv in invoices[:25]: # limit to 25 items for one page roughly
            if y < 50:
                c.showPage()
                y = 800
                c.setFont("Helvetica", 10)
            
            c.drawString(50, y, str(inv['date']))
            c.drawString(150, y, str(inv['number']))
            c.drawString(270, y, str(inv['customer'])[:18])
            c.drawString(400, y, str(inv['amount']))
            c.drawString(480, y, str(inv['status']))
            y -= 20
            
        c.showPage()
        c.save()
        return output_path











