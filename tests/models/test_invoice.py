import pytest
from database.queries import DatabaseQueries

def test_create_invoice_with_items(clean_db):
    """
    Test creating an invoice and adding items to it.
    """
    queries = DatabaseQueries()
    
    # 1. Add a dummy product
    product_id = queries.add_product(
        name="Keyboard", category="Accessories", hsn="8471", 
        cost=1000, selling=1500, gst=18, stock=20, supplier_id=None
    )
    
    # 2. Add a dummy customer
    customer_id = queries.add_customer("Test Corp", "111", "test@test.com", "GST1", "Address")
    
    # 3. Create Invoice Header
    invoice_data = {
        'invoice_number': "INV-2026-001",
        'customer_id': customer_id,
        'company_id': 1,
        'subtotal': 1500.0,
        'discount': 0.0,
        'cgst': 135.0,
        'sgst': 135.0,
        'igst': 0.0,
        'total_tax': 270.0,
        'total_amount': 1770.0,
        'payment_method': "Cash",
        'status': "Paid",
        'amount_paid': 1770.0,
        'notes': "Test note",
        'created_by': 1,
        'qr_hash': "dummy_hash"
    }
    
    invoice_id = queries.create_invoice(invoice_data)
    assert invoice_id is not None
    
    # 4. Add Invoice Item
    item_data = {
        'product_id': product_id,
        'quantity': 1,
        'price': 1500.0,
        'discount': 0.0,
        'gst_percentage': 18.0,
        'total': 1770.0
    }
    queries.add_invoice_item(invoice_id, item_data)
    
    # 5. Verify Data
    invoice = queries.get_by_id("invoices", invoice_id)
    assert invoice['invoice_number'] == "INV-2026-001"
    assert invoice['total_amount'] == 1770.0
    
    items = queries.db.fetchall("SELECT * FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
    assert len(items) == 1
    assert items[0]['product_id'] == product_id
    assert items[0]['total'] == 1770.0
