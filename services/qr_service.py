"""
File: qr_service.py

Purpose:
Generates secure Quick Response (QR) code images for printed invoices.
It embeds a cryptographic hash inside the QR code to verify the invoice's authenticity.

Dependencies:
- qrcode (External library to draw the QR image)
- hashlib (For generating the tamper-proof hash)
- os (For saving image files to disk)

Project: Smart ERP Billing System
"""

import qrcode
import hashlib
import os

# This class isolates all QR code generation logic.
# It exists because generating graphics is an independent, specialized task.
# Its responsibility is taking invoice metadata, signing it securely, and producing an image file.
class QRService:
    """
    Service class responsible for generating cryptographic QR code images.
    """
    
    def __init__(self):
        # Determine where to save the images (the 'qrcodes' folder in the project root)
        self.qr_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'qrcodes')
        
        # Ensure the directory exists; if it doesn't, create it automatically
        os.makedirs(self.qr_dir, exist_ok=True)

    # Purpose:
    # Generates a QR code PNG image containing the invoice details and a verification hash.
    #
    # Parameters:
    # invoice_number (str): The visible invoice string.
    # customer_name (str): The billed customer.
    # amount (float): The final amount on the bill.
    #
    # Returns:
    # tuple(str, str): A tuple containing the (FilePath to the image, The generated Hash string).
    def generate_qr(self, invoice_number, customer_name, amount):
        """
        Generates a QR code image for an invoice and signs it with SHA-256.

        Args:
            invoice_number (str): Invoice ID.
            customer_name (str): Customer name.
            amount (float): Total bill amount.

        Returns:
            tuple: (absolute_path_to_image, sha256_hash_string)
        """
        # Concatenate the critical billing data into a single plain text string
        data = f"INV:{invoice_number}|CUST:{customer_name}|AMT:{amount}"
        
        # Generate a SHA-256 hash of this data. If anyone tampers with the printed PDF later, 
        # scanning the QR and comparing the hash will prove it's a forgery.
        qr_hash = hashlib.sha256(data.encode()).hexdigest()
        
        # Create the actual graphical QR code containing both the data and the hash
        img = qrcode.make(f"{data}|HASH:{qr_hash}")
        
        # Define the exact file path where this image will be saved (e.g. qrcodes/INV-001.png)
        path = os.path.join(self.qr_dir, f"{invoice_number}.png")
        
        # Write the image to disk
        img.save(path)
        
        # Return both the path (so the PDF generator can embed it) and the hash (so the DB can store it)
        return path, qr_hash
