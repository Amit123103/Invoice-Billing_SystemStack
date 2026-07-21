############################################################
# Project : Smart ERP Billing System
#
# File    : customer.py
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
File: customer.py

Purpose:
Defines the Customer data structure used throughout the Smart ERP application.
It acts as a data transfer object between the database layer and the GUI/services.

Dependencies:
- dataclasses
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
from dataclasses import dataclass

# This class manages the representation of a single Customer entity.
# It exists so we can safely and predictably pass customer data across the app
# (like passing a Customer object to the Invoice generation service).
# Its responsibility is purely data storage and type definition.
# ---------------------------------------------
# Team Member 3
# Class: Customer
# Purpose:
# Data container for a Customer record.
# ---------------------------------------------
@dataclass
class Customer:
    """
    Data container for a Customer record.
    """
    
    # Unique primary key ID from the database
    id: int
    
    # Full name of the customer
    name: str
    
    # Contact phone number for SMS or calls
    phone: str
    
    # Contact email address for sending digital invoices
    email: str
    
    # Customer's GST identification number, required for B2B tax invoices
    gst_number: str
    
    # Billing address where products/invoices will be sent
    address: str




