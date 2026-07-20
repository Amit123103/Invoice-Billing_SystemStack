"""
File: payment.py

Purpose:
Defines the Payment model for tracking individual transactions made against invoices.

Dependencies:
- dataclasses

Author: Amit Kumar
Project: Smart ERP Billing System
"""

from dataclasses import dataclass

# This class represents a financial payment record.
# It solves the problem of tracking partial payments or split payments for a single invoice.
# Its responsibility is linking an amount paid to a specific invoice at a specific time.
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
