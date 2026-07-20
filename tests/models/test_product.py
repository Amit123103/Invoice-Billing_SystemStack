import pytest
from database.queries import DatabaseQueries

def test_add_product(clean_db):
    """
    Test adding a product to the database.
    """
    queries = DatabaseQueries()
    
    product_id = queries.add_product(
        name="Laptop",
        category="Electronics",
        hsn="8471",
        cost=50000.0,
        selling=60000.0,
        gst=18.0,
        stock=10,
        supplier_id=None
    )
    
    assert product_id is not None
    
    # Verify product in database
    product = queries.get_by_id("products", product_id)
    assert product is not None
    assert product['name'] == "Laptop"
    assert product['stock_quantity'] == 10
    assert product['selling_price'] == 60000.0

def test_update_stock(clean_db):
    """
    Test updating product stock level.
    """
    queries = DatabaseQueries()
    
    product_id = queries.add_product(
        name="Mouse", category="Accessories", hsn="8471", 
        cost=500, selling=800, gst=18, stock=50, supplier_id=None
    )
    
    # Decrease stock by 5
    queries.update_stock(product_id, quantity_change=-5, user_id=1, reason="Sale")
    
    product = queries.get_by_id("products", product_id)
    assert product['stock_quantity'] == 45
    
    # Increase stock by 20
    queries.update_stock(product_id, quantity_change=20, user_id=1, reason="Restock")
    
    product = queries.get_by_id("products", product_id)
    assert product['stock_quantity'] == 65
