from database.connection import DatabaseConnection

class DatabaseQueries:
    def __init__(self):
        self.db = DatabaseConnection()

    # User Queries
    def get_user_by_username(self, username):
        return self.db.fetchone("SELECT * FROM users WHERE username = ?", (username,))
    
    def create_user(self, username, password_hash, role):
        return self.db.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        ).lastrowid

    # Company Queries
    def get_company(self, company_id=1):
        return self.db.fetchone("SELECT * FROM companies WHERE id = ?", (company_id,))

    def save_company(self, name, gst_number, address, phone, email, logo_path, company_id=1):
        existing = self.get_company(company_id)
        if existing:
            self.db.execute('''
                UPDATE companies 
                SET name=?, gst_number=?, address=?, phone=?, email=?, logo_path=?
                WHERE id=?
            ''', (name, gst_number, address, phone, email, logo_path, company_id))
        else:
            self.db.execute('''
                INSERT INTO companies (id, name, gst_number, address, phone, email, logo_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (company_id, name, gst_number, address, phone, email, logo_path))

    # Generic CRUD
    def get_all(self, table_name):
        return self.db.fetchall(f"SELECT * FROM {table_name}")

    def get_by_id(self, table_name, record_id):
        return self.db.fetchone(f"SELECT * FROM {table_name} WHERE id = ?", (record_id,))

    def delete_by_id(self, table_name, record_id):
        self.db.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))

    # Custom Customer Queries
    def search_customers(self, search_term):
        term = f"%{search_term}%"
        return self.db.fetchall('''
            SELECT * FROM customers 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR gst_number LIKE ?
        ''', (term, term, term, term))

    def add_customer(self, name, phone, email, gst, address):
        return self.db.execute(
            "INSERT INTO customers (name, phone, email, gst_number, address) VALUES (?, ?, ?, ?, ?)",
            (name, phone, email, gst, address)
        ).lastrowid

    def update_customer(self, cust_id, name, phone, email, gst, address):
        self.db.execute('''
            UPDATE customers SET name=?, phone=?, email=?, gst_number=?, address=? WHERE id=?
        ''', (name, phone, email, gst, address, cust_id))

    # Product Queries
    def add_product(self, name, category, hsn, cost, selling, gst, stock, supplier_id):
        return self.db.execute('''
            INSERT INTO products (name, category, hsn_code, cost_price, selling_price, gst_percentage, stock_quantity, supplier_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, hsn, cost, selling, gst, stock, supplier_id)).lastrowid

    def update_product(self, prod_id, name, category, hsn, cost, selling, gst, stock, supplier_id):
        self.db.execute('''
            UPDATE products SET name=?, category=?, hsn_code=?, cost_price=?, selling_price=?, 
            gst_percentage=?, stock_quantity=?, supplier_id=? WHERE id=?
        ''', (name, category, hsn, cost, selling, gst, stock, supplier_id, prod_id))
        
    def search_products(self, search_term):
        term = f"%{search_term}%"
        return self.db.fetchall('''
            SELECT * FROM products 
            WHERE name LIKE ? OR category LIKE ? OR hsn_code LIKE ?
        ''', (term, term, term))

    # Inventory
    def update_stock(self, product_id, quantity_change, user_id, reason="Invoice Creation"):
        self.db.execute("UPDATE products SET stock_quantity = stock_quantity + ? WHERE id = ?", (quantity_change, product_id))
        self.db.execute(
            "INSERT INTO inventory_logs (product_id, change_amount, reason, created_by) VALUES (?, ?, ?, ?)",
            (product_id, quantity_change, reason, user_id)
        )

    # Invoices
    def create_invoice(self, data):
        # data is a dict
        cursor = self.db.execute('''
            INSERT INTO invoices (
                invoice_number, customer_id, company_id, subtotal, discount, 
                cgst, sgst, igst, total_tax, total_amount, payment_method, 
                status, amount_paid, notes, created_by, qr_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['invoice_number'], data.get('customer_id'), data.get('company_id', 1),
            data['subtotal'], data.get('discount', 0), data.get('cgst', 0),
            data.get('sgst', 0), data.get('igst', 0), data.get('total_tax', 0),
            data['total_amount'], data.get('payment_method'), data.get('status', 'Pending'),
            data.get('amount_paid', 0), data.get('notes', ''), data.get('created_by'), data.get('qr_hash', '')
        ))
        return cursor.lastrowid

    def add_invoice_item(self, invoice_id, item):
        self.db.execute('''
            INSERT INTO invoice_items (invoice_id, product_id, quantity, price, discount, gst_percentage, total)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            invoice_id, item['product_id'], item['quantity'], item['price'], 
            item.get('discount', 0), item['gst_percentage'], item['total']
        ))

    def log_audit(self, user_id, action, target_type=None, target_id=None, details=None):
        self.db.execute('''
            INSERT INTO audit_logs (user_id, action, target_type, target_id, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, action, target_type, target_id, details))
