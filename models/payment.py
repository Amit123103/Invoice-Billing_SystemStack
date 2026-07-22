############################################################
# Project : Smart ERP Billing System
#
# File    : payment.py
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
File: payment.py

Purpose:
Defines the Payment model for tracking individual transactions made against invoices.

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

# This class represents a financial payment record.
# It solves the problem of tracking partial payments or split payments for a single invoice.
# Its responsibility is linking an amount paid to a specific invoice at a specific time.
# ---------------------------------------------
# Team Member 3
# Class: Payment
# Purpose:
# Data container for an Invoice Payment record.
# ---------------------------------------------
@dataclass
class Payment:
    """
    Data container for an Invoice Payment record.
    """
    
    # The ID of the invoice this payment is paying off
    invoice_id: int
    
    # The monetary amount received
    amount: float
    
    # The transaction method (e.g., Cash, Credit Card)
    method: str
    
    # ISO formatted string representing the date and time of the payment
    date: str







