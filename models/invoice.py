############################################################
# Project : Smart ERP Billing System
#
# File    : invoice.py
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
File: invoice.py

Purpose:
Defines the complex data models required for Invoicing, including both 
the overall Invoice itself and the individual line items contained within it.

Dependencies:
- dataclasses
- typing
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
from dataclasses import dataclass, field
from typing import List

# This class represents a single row/item on a physical invoice.
# It exists because an invoice is composed of multiple products, each with its own
# specific quantity, discount, and calculated tax at the time of sale.
# It ensures item-level tax calculations remain tied to the specific transaction.
# ---------------------------------------------
# Team Member 4
# Class: InvoiceItem
# Purpose:
# Represents a single purchased item row on an invoice.
# ---------------------------------------------
@dataclass
class InvoiceItem:
    """
    Represents a single purchased item row on an invoice.
    """
    # The database ID of the actual product sold
    product_id: int
    
    # How many units were purchased
    quantity: int
    
    # The unit price at the time of sale (locks in the price even if the master product price changes later)
    price: float
    
    # The monetary discount applied specifically to this item row
    discount: float
    
    # The GST tax rate applied to this item
    gst_percentage: float
    
    # The final calculated total for this row (Qty * Price - Discount + Tax)
    total: float

# This class represents a complete financial billing transaction.
# It solves the problem of aggregating all sub-totals, taxes, and items into one coherent object.
# Its responsibility is to represent the finalized state of a bill for storage, PDF printing, or QR generation.
# ---------------------------------------------
# Team Member 4
# Class: Invoice
# Purpose:
# Represents a full Invoice containing customer details, totals, and a list of purchased items.
# ---------------------------------------------
@dataclass
class Invoice:
    """
    Represents a full Invoice containing customer details, totals, and a list of purchased items.
    """
    # Unique database ID
    id: int
    
    # Human-readable, sequentially generated string (e.g., INV-20231024001)
    invoice_number: str
    
    # Database ID of the customer who was billed
    customer_id: int
    
    # Database ID of the company issuing the invoice
    company_id: int
    
    # Total sum of all items before taxes and invoice-level discounts
    subtotal: float
    
    # Total discount applied across the entire invoice
    discount: float
    
    # Central Goods and Services Tax total amount
    cgst: float
    
    # State Goods and Services Tax total amount
    sgst: float
    
    # Integrated Goods and Services Tax total amount (for inter-state sales)
    igst: float
    
    # The sum of CGST + SGST + IGST
    total_tax: float
    
    # The final grand total that the customer must pay
    total_amount: float
    
    # How the customer intends to pay (Cash, Card, UPI, etc.)
    payment_method: str
    
    # The current payment status (e.g., 'Paid', 'Pending', 'Overdue')
    status: str
    
    # How much of the total_amount has actually been collected
    amount_paid: float
    
    # Free-text notes or terms & conditions for the invoice
    notes: str
    
    # The user ID of the employee/admin who generated the invoice (for audit logs)
    created_by: int
    
    # A list containing all the individual InvoiceItem rows.
    # We use a default_factory so new invoices start with an empty list instead of sharing the same list reference in memory.
    items: List[InvoiceItem] = field(default_factory=list)













