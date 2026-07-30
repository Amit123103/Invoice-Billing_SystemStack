############################################################
# Project : Smart ERP Billing System
#
# File    : report_service.py
#
# Team Member :Bhipender Singh
# Team Member 4
#
# Module :
# Invoice & Reports
#
# Responsibilities :
# - Invoice Generation
# - Reports
# - Analytics
# - PDF Export
#
# Developed By :
# Team Member 4
############################################################
"""
File: report_service.py

Purpose:
Handles the generation of physical PDF documents like Invoices and Reports.

Dependencies:
- reportlab.pdfgen.canvas (To draw text/images onto a PDF)
- reportlab.lib.pagesizes.A4 (Standard paper sizing)
- os (For file paths)

"""

###########################################################
# Team Member 4
# Module: Invoice & Reports
# Completed:
# - Invoice Generation
# - Reports
# - Analytics
# - PDF Export
###########################################################
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

# This class manages PDF exports.
# It solves the problem of converting application data into printable, professional documents.
# Its responsibility is drawing text, lines, and images (like logos and QR codes) onto a digital canvas.
# ---------------------------------------------
# Team Member 4
# Class: ReportService
# Purpose:
# Service class responsible for generating PDF documents using ReportLab.
# ---------------------------------------------
class ReportService:
    """
    Service class responsible for generating PDF documents using ReportLab.
    """
    
    # ---------------------------------------------
    # Team Member 4
    # Function: __init__
    # Purpose:
    # Handles logic for   init  
    # ---------------------------------------------
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
    # ---------------------------------------------
    # Team Member 4
    # Function: generate_invoice_pdf
    # Purpose:
    # Generates a PDF invoice.
    # invoice_data (dict): The main invoice header data.
    # items_data (list): The list of purchased items.
    # ---------------------------------------------
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
        amount_paid = float(invoice_data.get("amount_paid", 0))
        total_amount = float(invoice_data.get("total_amount", 0))
        due_amount = total_amount - amount_paid
        status = invoice_data.get("status", "Pending")
        
        # Draw the main title text near the top of the page (Coordinates: X=100, Y=800)
         # Draw the total amount text slightly lower (Y=780)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, 800, "SMART ERP BILLING SYSTEM")

        c.setFont("Helvetica", 12)
        c.drawString(100, 770, f"Invoice No : {invoice_data['invoice_number']}")
        c.drawString(100, 750, f"Total Amount : Rs {total_amount:.2f}")
        c.drawString(100, 730, f"Amount Paid : Rs {amount_paid:.2f}")
        c.drawString(100, 710, f"Due Amount : Rs {due_amount:.2f}")
        c.drawString(100, 690, f"Payment Status : {status}")
        
        # Check if a QR code image was successfully created and exists on the hard drive
        if qr_path and os.path.exists(qr_path):
            # Embed the QR image into the PDF on the right side (X=400)
            c.drawImage(qr_path, 400, 700, width=100, height=100)

            # ---------- Product Table ----------

            y = 620

            c.setFont("Helvetica-Bold", 12)

            c.drawString(50, y, "Product")
            c.drawString(250, y, "Qty")
            c.drawString(320, y, "Price")
            c.drawString(430, y, "Total")

            y -= 15
            c.line(50, y, 540, y)

            y -= 20

            c.setFont("Helvetica", 11)

            for item in items_data:

                c.drawString(50, y, item["name"])
                c.drawString(260, y, str(item["quantity"]))
                c.drawString(320, y, f"Rs {item['price']:.2f}")
                c.drawString(430, y, f"Rs {item['total']:.2f}")

                y -= 20


                y -= 20

        c.line(50, y, 540, y)

        y -= 25

        c.drawRightString(430, y, "Subtotal")
        c.drawRightString(540, y, f"Rs {invoice_data['subtotal']:.2f}")

        y -= 20

        c.drawRightString(430, y, "GST")
        c.drawRightString(540, y, f"Rs {invoice_data['total_tax']:.2f}")

        y -= 20

        c.drawRightString(430, y, "Discount")
        c.drawRightString(540, y, f"Rs {invoice_data['discount']:.2f}")

        y -= 20

        c.setFont("Helvetica-Bold", 12)

        c.drawRightString(430, y, "Grand Total")
        c.drawRightString(540, y, f"Rs {invoice_data['total_amount']:.2f}")


        y -= 30

        c.setFont("Helvetica", 11)

        c.drawString(50, y, f"Amount Paid : Rs {invoice_data['amount_paid']:.2f}")

        y -= 20

        due = invoice_data["total_amount"] - invoice_data["amount_paid"]

        c.drawString(50, y, f"Due Amount : Rs {due:.2f}")

        y -= 20

        c.drawString(50, y, f"Status : {invoice_data['status']}")
            
        # Finalize the current page
        c.showPage()
        
        # Save the PDF to the hard drive
        c.save()
        
        # Return the path so the GUI can notify the user where the file is
        return filename

    # ---------------------------------------------
    # Team Member 4
    # Function: generate_business_report_pdf
    # Purpose:
    # Generates a comprehensive business report PDF.
    # ---------------------------------------------
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
            if y < 150:
                c.showPage()
                y = 800
                c.setFont("Helvetica", 10)
            
            c.drawString(50, y, str(inv['date']))
            c.drawString(150, y, str(inv['number']))
            c.drawString(270, y, str(inv['customer'])[:18])
            c.drawString(400, y, str(inv['amount']))
            c.drawString(480, y, str(inv['status']))
            y -= 20
            
        # Add Verified Stamp and QR Code at the end of the report
        if y < 150:
            c.showPage()
            y = 800
            
        # Draw Verified Stamp
        c.setFont("Helvetica-Bold", 16)
        c.setFillColorRGB(0.06, 0.6, 0.2) # Professional Green
        c.drawString(50, y - 50, "*** VERIFIED BUSINESS REPORT ***")
        c.setFillColorRGB(0, 0, 0) # Reset to black
        
        # Generate and draw QR Code
        import qrcode
        import hashlib
        report_data = f"Smart ERP | Rev: {metrics['revenue']} | Inv: {metrics['invoices']}"
        report_hash = hashlib.sha256(report_data.encode()).hexdigest()
        img = qrcode.make(f"{report_data} | HASH: {report_hash}")
        qr_img_path = os.path.join(self.reports_dir, "temp_report_qr.png")
        img.save(qr_img_path)
        
        c.drawImage(qr_img_path, 400, y - 100, width=80, height=80)
            
        c.showPage()
        c.save()
        return output_path











