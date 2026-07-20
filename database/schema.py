"""
File: schema.py

Purpose:
Contains the Data Definition Language (DDL) logic to create the SQLite tables.
It ensures that the database structure exists before the app attempts to read or write data.

Dependencies:
- database.connection (For connecting to the DB and executing the CREATE TABLE scripts)

Project: Smart ERP Billing System
"""

from database.connection import DatabaseConnection

# Purpose:
# Sets up the entire SQLite database structure from scratch if it doesn't already exist.
# It creates all required tables with proper primary keys, foreign keys, and constraints.
#
# Returns:
# None
def create_tables():
    """
    Initializes the database schema and creates necessary tables if they do not exist.
    """
    # Instantiate the singleton database connection manager
    db = DatabaseConnection()
    
    # ---------------------------------------------------------
    # Users Table
    # Stores authentication and role data for employees.
    # ---------------------------------------------------------
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Admin', 'Manager', 'Cashier')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ---------------------------------------------------------
    # Companies Table
    # Stores the primary business profile generating the invoices.
    # ---------------------------------------------------------
    db.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gst_number TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            logo_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ---------------------------------------------------------
    # Customers Table
    # Stores client details for billing and CRM purposes.
    # ---------------------------------------------------------
    db.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            gst_number TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ---------------------------------------------------------
    # Suppliers Table
    # Stores vendor information from whom products are purchased.
    # ---------------------------------------------------------
    db.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ---------------------------------------------------------
    # Products Table
    # The central inventory table containing pricing and stock levels.
    # ---------------------------------------------------------
    # FOREIGN KEY constraint links this product to a supplier. ON DELETE SET NULL ensures 
    # that if a supplier is deleted, the product remains but the supplier_id becomes NULL.
    db.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            hsn_code TEXT,
            cost_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            gst_percentage REAL NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            supplier_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id) ON DELETE SET NULL
        )
    ''')

    # ---------------------------------------------------------
    # Invoices Table
    # Stores the header/totals data for a financial bill.
    # ---------------------------------------------------------
    db.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT NOT NULL UNIQUE,
            customer_id INTEGER,
            company_id INTEGER,
            subtotal REAL NOT NULL,
            discount REAL DEFAULT 0,
            cgst REAL DEFAULT 0,
            sgst REAL DEFAULT 0,
            igst REAL DEFAULT 0,
            total_tax REAL DEFAULT 0,
            total_amount REAL NOT NULL,
            payment_method TEXT,
            status TEXT CHECK(status IN ('Paid', 'Pending', 'Partial')),
            amount_paid REAL DEFAULT 0,
            notes TEXT,
            version INTEGER DEFAULT 1,
            parent_invoice_id INTEGER,
            status_type TEXT DEFAULT 'Normal' CHECK(status_type IN ('Normal', 'Refund', 'Return')),
            qr_hash TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (company_id) REFERENCES companies (id),
            FOREIGN KEY (parent_invoice_id) REFERENCES invoices (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')

    # ---------------------------------------------------------
    # Invoice Items Table
    # Stores the individual products sold within a specific invoice.
    # ---------------------------------------------------------
    # ON DELETE CASCADE ensures that if an invoice is deleted, all its items are automatically deleted too.
    db.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            discount REAL DEFAULT 0,
            gst_percentage REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # ---------------------------------------------------------
    # Inventory Logs Table
    # Keeps a historical audit trail of stock additions and deductions.
    # ---------------------------------------------------------
    db.execute('''
        CREATE TABLE IF NOT EXISTS inventory_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            change_amount INTEGER NOT NULL,
            reason TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')

    # ---------------------------------------------------------
    # Audit Logs Table
    # Tracks user actions for security and accountability.
    # ---------------------------------------------------------
    db.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            target_type TEXT,
            target_id INTEGER,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # ---------------------------------------------------------
    # Default Admin User
    # ---------------------------------------------------------
    # We use INSERT OR IGNORE so this query safely fails if the admin already exists, preventing duplicates.
    # '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9' is the SHA-256 hash for 'admin123'.
    db.execute('''
        INSERT OR IGNORE INTO users (id, username, password_hash, role) 
        VALUES (1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Admin')
    ''')

# Standard python idiom: execute the script directly only if run from the command line, not if imported as a module
if __name__ == '__main__':
    create_tables()
    print("Database tables created successfully.")
