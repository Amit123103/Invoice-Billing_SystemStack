"""
File: report_service.py

Purpose:
Handles the generation of physical PDF documents like Invoices and Reports.

Dependencies:
- reportlab.pdfgen.canvas (To draw text/images onto a PDF)
- reportlab.lib.pagesizes.A4 (Standard paper sizing)
- os (For file paths)

Author: Amit Kumar
Project: Smart ERP Billing System
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
    def generate_invoice_pdf(self, invoice_data, items_data, qr_path):
        """
        Generates a PDF invoice.

        Args:
            invoice_data (dict): The main invoice header data.
            items_data (list): The list of purchased items.
            qr_path (str): File path to the generated QR code image.

        Returns:
            str: Path to the generated PDF.
        """
        # Determine the file name based on the unique invoice number
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
