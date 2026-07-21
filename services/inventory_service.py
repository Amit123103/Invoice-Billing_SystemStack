############################################################
# Project : Smart ERP Billing System
#
# File    : inventory_service.py
#
# Team Member :
# Team Member 2
#
# Module :
# Inventory Management
#
# Responsibilities :
# - Product CRUD
# - Inventory
# - Categories
# - Supplier Management
#
# Developed By :
# Team Member 2
############################################################
"""
File: inventory_service.py

Purpose:
Manages product stock levels and triggers low-stock alerts.

Dependencies:
- database.queries

"""

###########################################################
# Team Member 2
# Module: Inventory Management
# Completed:
# - Product CRUD
# - Inventory
# - Categories
# - Supplier Management
###########################################################
from database.queries import DatabaseQueries

# This class handles inventory checking and modifications.
# It solves the problem of scattering stock logic throughout the app.
# Its responsibility is keeping stock levels accurate and alerting when they drop too low.
# ---------------------------------------------
# Team Member 2
# Class: InventoryService
# Purpose:
# Service class managing stock levels and alerts.
# ---------------------------------------------
class InventoryService:
    """
    Service class managing stock levels and alerts.
    """
    
    # ---------------------------------------------
    # Team Member 2
    # Function: __init__
    # Purpose:
    # Handles logic for   init  
    # ---------------------------------------------
    def __init__(self):
        self.db = DatabaseQueries()

    # Purpose: Manually adds or removes stock (outside of invoicing).
    # Parameters:
    # product_id (int): The ID of the product.
    # amount (int): The number of items to add (or remove if negative).
    # user_id (int): The ID of the admin making the change.
    # ---------------------------------------------
    # Team Member 2
    # Function: add_stock
    # Purpose:
    # Manually adjusts the stock of a product.
    # product_id (int): ID of the product.
    # amount (int): Positive to add, negative to remove.
    # ---------------------------------------------
    def add_stock(self, product_id, amount, user_id):
        """
        Manually adjusts the stock of a product.

        Args:
            product_id (int): ID of the product.
            amount (int): Positive to add, negative to remove.
            user_id (int): ID of the user performing the action.
        """
        # Call the database to adjust the stock and log the reason as "Added Stock"
        self.db.update_stock(product_id, amount, user_id, "Added Stock")
        
    # Purpose: Identifies which products need to be reordered.
    # Parameters: threshold (int): The stock level at which an alert is generated.
    # Returns: list: A list of products that are below the threshold.
    # ---------------------------------------------
    # Team Member 2
    # Function: get_low_stock_alerts
    # Purpose:
    # Retrieves a list of products whose stock has dropped below a certain threshold.
    # threshold (int, optional): The warning limit. Defaults to 10.
    # list: List of product dictionaries that need reordering.
    # ---------------------------------------------
    def get_low_stock_alerts(self, threshold=10):
        """
        Retrieves a list of products whose stock has dropped below a certain threshold.

        Args:
            threshold (int, optional): The warning limit. Defaults to 10.

        Returns:
            list: List of product dictionaries that need reordering.
        """
        # Fetch every single product in the database
        products = self.db.get_all("products")
        
        # Use a list comprehension to filter only those products whose stock is dangerously low
        return [p for p in products if p['stock_quantity'] <= threshold]










