############################################################
# Project : Smart ERP Billing System
#
# File    : company.py
#
# Team Member :
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
File: company.py

Purpose:
Defines the data structure for a Company entity in the Smart ERP Billing System.
This acts as a model to hold company profile information (like name, GST, logo).

Dependencies:
- dataclasses (For auto-generating class boilerplate like __init__)

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
from dataclasses import dataclass

# This class represents a single Company configuration in the system.
# It solves the problem of passing around loosely typed company dictionaries
# by providing a strict object-oriented structure with type hints.
# Responsibilities include holding company details securely for use in reports and invoices.
# ---------------------------------------------
# Team Member 4
# Class: Company
# Purpose:
# Data container for a Company record.
# ---------------------------------------------
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






