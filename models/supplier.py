"""
File: supplier.py

Purpose:
Defines the Supplier data model representing vendors who provide products.

Dependencies:
- dataclasses
"""

from dataclasses import dataclass

# This class holds vendor/supplier information.
# It exists to give a structured schema to the individuals or companies 
# supplying inventory to the ERP system.
# Its primary responsibility is basic data encapsulation.
@dataclass
class Supplier:
    """
    Data container for a Supplier record.
    """
    
    # Unique supplier ID in the database
    id: int
    
    # Name of the supplying vendor or company
    name: str
    
    # Contact phone number
    phone: str
    
    # Contact email address
    email: str
    
    # Physical or billing address of the supplier
    address: str








