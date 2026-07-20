"""
File: product.py

Purpose:
Defines the core Product data model which represents items that can be sold or tracked in inventory.

Dependencies:
- dataclasses

Project: Smart ERP Billing System
"""

from dataclasses import dataclass

# This class defines what a Product looks like in our Python code.
# It solves the problem of inconsistently referencing product attributes 
# by enforcing strict variable names and types.
# Its main responsibility is to hold financial, taxation, and stock data for a single item.
@dataclass
class Product:
    """
    Data container for an Inventory Product.
    """
    
    # Unique database identifier
    id: int
    
    # Name or title of the product
    name: str
    
    # Grouping category (e.g., Electronics, Accessories)
    category: str
    
    # Harmonized System of Nomenclature code used internationally to classify goods for taxation
    hsn_code: str
    
    # The baseline cost incurred to acquire the product (useful for profit calculations)
    cost_price: float
    
    # The retail price at which the product is sold to customers (before tax)
    selling_price: float
    
    # The specific GST tax bracket percentage applied to this product (e.g., 5, 12, 18, 28)
    gst_percentage: float
    
    # The total number of units currently available in the warehouse/store
    stock_quantity: int
    
    # Foreign key reference to the Supplier who provides this product
    supplier_id: int
