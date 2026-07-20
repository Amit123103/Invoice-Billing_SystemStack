import pytest
from services.inventory_service import InventoryService
from database.queries import DatabaseQueries

def test_add_stock(clean_db):
    """
    Test adding stock via InventoryService.
    """
    queries = DatabaseQueries()
    service = InventoryService()
    
    product_id = queries.add_product(
        name="Box", category="Pack", hsn="999", 
        cost=10, selling=20, gst=0, stock=5, supplier_id=None
    )
    
    service.add_stock(product_id, amount=10, user_id=1)
    
    product = queries.get_by_id("products", product_id)
    assert product['stock_quantity'] == 15
    
def test_get_low_stock_alerts(clean_db):
    """
    Test getting alerts for products below a threshold.
    """
    queries = DatabaseQueries()
    service = InventoryService()
    
    # Add products with various stock levels
    queries.add_product("High Stock", "A", "1", 1, 2, 0, 50, None)
    queries.add_product("Low Stock", "A", "1", 1, 2, 0, 5, None)
    queries.add_product("Critical", "A", "1", 1, 2, 0, 1, None)
    
    alerts = service.get_low_stock_alerts(threshold=10)
    
    assert len(alerts) == 2
    names = [p['name'] for p in alerts]
    assert "Low Stock" in names
    assert "Critical" in names
    assert "High Stock" not in names
