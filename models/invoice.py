from dataclasses import dataclass, field
from typing import List

@dataclass
class InvoiceItem:
    product_id: int
    quantity: int
    price: float
    discount: float
    gst_percentage: float
    total: float

@dataclass
class Invoice:
    id: int
    invoice_number: str
    customer_id: int
    company_id: int
    subtotal: float
    discount: float
    cgst: float
    sgst: float
    igst: float
    total_tax: float
    total_amount: float
    payment_method: str
    status: str
    amount_paid: float
    notes: str
    created_by: int
    items: List[InvoiceItem] = field(default_factory=list)
