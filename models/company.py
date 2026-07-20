"""
File: company.py

Purpose:
Defines the data structure for a Company entity in the Smart ERP Billing System.
This acts as a model to hold company profile information (like name, GST, logo).

Dependencies:
- dataclasses (For auto-generating class boilerplate like __init__)

Author: Amit Kumar
Project: Smart ERP Billing System
"""

from dataclasses import dataclass

# This class represents a single Company configuration in the system.
# It solves the problem of passing around loosely typed company dictionaries
# by providing a strict object-oriented structure with type hints.
# Responsibilities include holding company details securely for use in reports and invoices.
@dataclass
class Company:
    """
    Data container for a Company record.
    """
    
    # Unique identifier for the company in the database
    id: int
    
    # Legal or registered name of the company
    name: str
    
    # Goods and Services Tax number used for billing compliance in India
    gst_number: str
    
    # Physical or registered address of the company
    address: str
    
    # Primary contact phone number
    phone: str
    
    # Primary contact email address
    email: str
    
    # File system path pointing to the company's logo image used in PDF generation
    logo_path: str
