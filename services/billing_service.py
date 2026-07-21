############################################################
# Project : Smart ERP Billing System
#
# File    : billing_service.py
#
# Team Member :
# Team Member 3
#
# Module :
# Customer & Billing
#
# Responsibilities :
# - Customer CRUD
# - Billing
# - Cart
# - GST
# - Discount
#
# Developed By :
# Team Member 3
############################################################
"""
File: billing_service.py

Purpose:
Handles complex business logic for creating and managing invoices. 
It acts as the bridge between the GUI layer and the Database Queries.

Dependencies:
- database.queries

"""

###########################################################
# Team Member 3
# Module: Customer & Billing
# Completed:
# - Customer CRUD
# - Billing
# - Cart
# - GST
# - Discount
###########################################################
from database.queries import DatabaseQueries

# This class manages the billing lifecycle.
# It solves the problem of having complex, multi-step database operations inside GUI buttons.
# Its responsibility is to ensure that when an invoice is generated, the invoice is saved,
# the individual items are saved, and the inventory stock is correctly deducted in one seamless flow.
# ---------------------------------------------
# Team Member 3
# Class: BillingService
# Purpose:
# Service class executing billing business logic.
# ---------------------------------------------
class BillingService:
    """
    Service class executing billing business logic.
    """
    
    # ---------------------------------------------
    # Team Member 3
    # Function: __init__
    # Purpose:
    # Handles logic for   init  
    # ---------------------------------------------
    def __init__(self):
        # Initialize the DAO (Data Access Object) to speak to the DB.
        self.db = DatabaseQueries()

    # Purpose:
    # Orchestrates the creation of a complete invoice, including items and stock adjustments.
    #
    # Parameters:
    # data (dict): The header data for the invoice (total amounts, customer, etc.)
    # items (list): A list of dictionaries representing individual purchased products.
    #
    # Returns:
    # int: The generated primary key ID of the new Invoice.
    # ---------------------------------------------
    # Team Member 3
    # Function: generate_invoice
    # Purpose:
    # Creates an invoice, saves items, and reduces stock.
    # data (dict): Invoice header dictionary.
    # items (list): List of invoice item dictionaries.
    # ---------------------------------------------
    def generate_invoice(self, data, items):
        """
        Creates an invoice, saves items, and reduces stock.

        Args:
            data (dict): Invoice header dictionary.
            items (list): List of invoice item dictionaries.

        Returns:
            int: The new invoice ID.
        """
        # Step 1: Save the parent invoice record to the database and get its new ID
        invoice_id = self.db.create_invoice(data)
        
        # Step 2: Loop through every item the customer purchased
        for item in items:
            # Attach the product row to the invoice we just created
            self.db.add_invoice_item(invoice_id, item)
            
            # Step 3: Crucially, reduce the inventory stock by the quantity sold!
            # We pass negative quantity to deduct from stock.
            # This maintains data consistency across the ERP.
            self.db.update_stock(item['product_id'], -item['quantity'], data.get('created_by'))
            
        # Return the ID so the GUI can proceed to generate PDFs if needed.
        return invoice_id








