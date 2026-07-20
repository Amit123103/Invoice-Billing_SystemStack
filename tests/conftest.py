import pytest
import sqlite3
import os
import tempfile
import sys

# Ensure the root folder is in the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.connection import DatabaseConnection
from database.schema import create_tables

@pytest.fixture(scope="session")
def test_db():
    """
    Creates a temporary SQLite database for testing, sets up the schema,
    and forces the DatabaseConnection singleton to use it instead of smart_erp.db.
    """
    # Create a temporary file
    fd, path = tempfile.mkstemp(suffix='.db')
    
    # Override the database path in the singleton
    db_conn = DatabaseConnection()
    db_conn.db_path = path
    
    # Run schema.py logic to initialize tables in the temp db
    create_tables()
    
    yield db_conn
    
    # Teardown
    os.close(fd)
    try:
        os.remove(path)
    except PermissionError:
        pass

@pytest.fixture(autouse=True)
def clean_db(test_db):
    """
    This fixture runs before every test to ensure tables are empty or in a known state.
    """
    conn = test_db.get_connection()
    cursor = conn.cursor()
    
    tables = [
        "invoice_items",
        "invoices",
        "products",
        "suppliers",
        "customers",
        "companies",
        "users",
        "inventory_logs",
        "audit_logs"
    ]
    
    # Disable foreign keys temporarily to truncate safely
    cursor.execute("PRAGMA foreign_keys = OFF")
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Insert default admin user and company since they are required for foreign keys
    cursor.execute("INSERT INTO users (id, username, password_hash, role) VALUES (1, 'admin', 'hash', 'Admin')")
    cursor.execute("INSERT INTO companies (id, name, gst_number) VALUES (1, 'Test Company', 'GST123')")
    
    conn.commit()
    conn.close()
