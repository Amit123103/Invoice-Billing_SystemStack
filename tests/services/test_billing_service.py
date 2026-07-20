import pytest
from services.billing_service import BillingService
from database.queries import DatabaseQueries

def test_generate_invoice(clean_db):
    """
    Test generating an invoice using BillingService, which should create the invoice,
    add items, and reduce stock.
    """
    queries = DatabaseQueries()
    billing_service = BillingService()
    
    # Pre-setup data
    product_id = queries.add_product(
        name="Test Item", category="Test", hsn="1111", 
        cost=100, selling=200, gst=18, stock=50, supplier_id=None
    )
    
    # 2. Create Invoice Data
    invoice_data = {
        'invoice_number': "BILL-001",
        'customer_id': None,
        'company_id': 1,
        'subtotal': 200.0,
        'discount': 0.0,
        'cgst': 18.0,
        'sgst': 18.0,
        'igst': 0.0,
        'total_tax': 36.0,
        'total_amount': 236.0,
        'payment_method': "Card",
        'status': "Paid",
        'amount_paid': 236.0,
        'notes': "",
        'created_by': 1,
        'qr_hash': ""
    }
    
    items = [{
        'product_id': product_id,
        'quantity': 5,
        'price': 200.0,
        'discount': 0.0,
        'gst_percentage': 18.0,
        'total': 1180.0
    }]
    
    # Execute Service
    invoice_id = billing_service.generate_invoice(invoice_data, items)
    
    # Verify Invoice was created
    assert invoice_id is not None
    invoice = queries.get_by_id("invoices", invoice_id)
    assert invoice['invoice_number'] == "BILL-001"
    
    # Verify Items attached
    db_items = queries.db.fetchall("SELECT * FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
    assert len(db_items) == 1
    assert db_items[0]['quantity'] == 5
    
    # Verify Stock Deducted
    product = queries.get_by_id("products", product_id)
    assert product['stock_quantity'] == 45  # 50 - 5 = 45
