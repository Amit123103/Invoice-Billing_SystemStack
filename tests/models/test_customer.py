import pytest
from database.queries import DatabaseQueries

def test_add_customer(clean_db):
    """
    Test that a customer can be added successfully to the database.
    """
    queries = DatabaseQueries()
    
    # Add a customer
    customer_id = queries.add_customer(
        name="John Doe",
        phone="1234567890",
        email="john@example.com",
        gst="GST12345",
        address="123 Main St"
    )
    
    assert customer_id is not None
    assert isinstance(customer_id, int)
    
    # Retrieve the customer
    customer = queries.get_by_id("customers", customer_id)
    assert customer is not None
    assert customer['name'] == "John Doe"
    assert customer['phone'] == "1234567890"

def test_search_customers(clean_db):
    """
    Test the customer search functionality.
    """
    queries = DatabaseQueries()
    
    # Add some customers
    queries.add_customer("Alice Smith", "9998887776", "alice@test.com", "", "")
    queries.add_customer("Bob Jones", "5554443332", "bob@test.com", "BOBGST", "")
    
    # Search by name
    results = queries.search_customers("Alice")
    assert len(results) == 1
    assert results[0]['name'] == "Alice Smith"
    
    # Search by GST
    results_gst = queries.search_customers("BOBGST")
    assert len(results_gst) == 1
    assert results_gst[0]['name'] == "Bob Jones"
    
    # Search by partial string (case insensitive in SQLite LIKE)
    results_partial = queries.search_customers("test.com")
    assert len(results_partial) == 2
