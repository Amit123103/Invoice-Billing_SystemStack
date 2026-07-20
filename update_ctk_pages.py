import os
gui_dir = 'c:/Users/amita/myprojects/invoice_billing/gui'

files = {
    "inventory_page.py": '''import customtkinter as ctk
from tkinter import ttk, messagebox
from database.queries import DatabaseQueries

class InventoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.db = DatabaseQueries()
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Inventory Management", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")
        
        # Form Card
        form_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        form_card.pack(fill="x", padx=30, pady=10)
        
        row1 = ctk.CTkFrame(form_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(20, 10))
        
        self.name_var = ctk.StringVar()
        ctk.CTkEntry(row1, textvariable=self.name_var, placeholder_text="Product Name", width=200).pack(side="left", padx=10)
        
        self.category_var = ctk.StringVar()
        ctk.CTkEntry(row1, textvariable=self.category_var, placeholder_text="Category", width=150).pack(side="left", padx=10)
        
        self.hsn_var = ctk.StringVar()
        ctk.CTkEntry(row1, textvariable=self.hsn_var, placeholder_text="HSN Code", width=150).pack(side="left", padx=10)
        
        row2 = ctk.CTkFrame(form_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 20))
        
        self.cost_var = ctk.StringVar()
        ctk.CTkEntry(row2, textvariable=self.cost_var, placeholder_text="Cost Price", width=120).pack(side="left", padx=10)
        
        self.selling_var = ctk.StringVar()
        ctk.CTkEntry(row2, textvariable=self.selling_var, placeholder_text="Selling Price", width=120).pack(side="left", padx=10)
        
        self.gst_var = ctk.StringVar()
        ctk.CTkEntry(row2, textvariable=self.gst_var, placeholder_text="GST %", width=120).pack(side="left", padx=10)
        
        self.stock_var = ctk.StringVar()
        ctk.CTkEntry(row2, textvariable=self.stock_var, placeholder_text="Stock Qty", width=120).pack(side="left", padx=10)
        
        ctk.CTkButton(row2, text="Add Product", command=self.add_product, fg_color="#2563eb", hover_color="#1d4ed8").pack(side="left", padx=20)
        
        # Table Card
        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)
        
        columns = ("ID", "Name", "Category", "HSN", "Cost", "Selling", "GST", "Stock")
        
        style = ttk.Style()
        style.configure("Treeview", background="#FFFFFF", foreground="#111827", rowheight=40, borderwidth=0)
        style.configure("Treeview.Heading", background="#f9fafb", foreground="#6b7280", font=('Helvetica', 10, 'bold'), borderwidth=0)
        
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")
            
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        self.load_products()

    def add_product(self):
        try:
            name = self.name_var.get()
            if not name: return
            self.db.add_product(
                name, self.category_var.get(), self.hsn_var.get(), 
                float(self.cost_var.get() or 0), float(self.selling_var.get() or 0), 
                float(self.gst_var.get() or 0), int(self.stock_var.get() or 0), None
            )
            self.name_var.set("")
            self.category_var.set("")
            self.hsn_var.set("")
            self.cost_var.set("")
            self.selling_var.set("")
            self.gst_var.set("")
            self.stock_var.set("")
            self.load_products()
        except ValueError:
            pass

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.db.get_all("products"):
            self.tree.insert("", "end", values=(p['id'], p['name'], p['category'], p['hsn_code'], p['cost_price'], p['selling_price'], p['gst_percentage'], p['stock_quantity']))
''',
    "invoice_page.py": '''import customtkinter as ctk
from tkinter import ttk, messagebox
from database.queries import DatabaseQueries
from services.billing_service import BillingService
from services.qr_service import QRService
from services.report_service import ReportService
import datetime

class InvoicePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.db = DatabaseQueries()
        self.billing = BillingService()
        self.qr_service = QRService()
        self.report_service = ReportService()
        
        self.cart_items = []
        self.total_subtotal = 0
        self.total_tax = 0
        self.final_amount = 0
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Create Invoice", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")
        
        # Settings Card
        settings_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        settings_card.pack(fill="x", padx=30, pady=5)
        
        row1 = ctk.CTkFrame(settings_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=20)
        
        self.customer_var = ctk.StringVar()
        self.customer_dropdown = ctk.CTkOptionMenu(row1, variable=self.customer_var, values=[], width=300, fg_color="#f9fafb", text_color="#111827")
        self.customer_dropdown.pack(side="left", padx=10)
        
        self.payment_var = ctk.StringVar(value="Cash")
        ctk.CTkOptionMenu(row1, variable=self.payment_var, values=["Cash", "Card", "UPI", "Bank Transfer"], width=200, fg_color="#f9fafb", text_color="#111827").pack(side="left", padx=10)
        
        # Product Selection Card
        prod_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        prod_card.pack(fill="x", padx=30, pady=10)
        
        row2 = ctk.CTkFrame(prod_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=20)
        
        self.product_var = ctk.StringVar()
        self.product_dropdown = ctk.CTkOptionMenu(row2, variable=self.product_var, values=[], width=300, fg_color="#f9fafb", text_color="#111827")
        self.product_dropdown.pack(side="left", padx=10)
        
        self.qty_var = ctk.StringVar(value="1")
        ctk.CTkEntry(row2, textvariable=self.qty_var, placeholder_text="Qty", width=80).pack(side="left", padx=10)
        
        self.discount_var = ctk.StringVar(value="0")
        ctk.CTkEntry(row2, textvariable=self.discount_var, placeholder_text="Discount %", width=100).pack(side="left", padx=10)
        
        ctk.CTkButton(row2, text="Add to Cart", command=self.add_to_cart, fg_color="#2563eb").pack(side="left", padx=20)
        
        # Cart Table
        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=30, pady=5)
        
        cols = ("ID", "Name", "Qty", "Price", "Discount", "GST %", "Total")
        style = ttk.Style()
        style.configure("Treeview", background="#FFFFFF", foreground="#111827", rowheight=40, borderwidth=0)
        self.cart_tree = ttk.Treeview(table_card, columns=cols, show="headings", style="Treeview", height=6)
        for c in cols:
            self.cart_tree.heading(c, text=c)
            self.cart_tree.column(c, width=100)
            
        self.cart_tree.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Totals Card
        totals_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        totals_card.pack(fill="x", padx=30, pady=10)
        
        row3 = ctk.CTkFrame(totals_card, fg_color="transparent")
        row3.pack(fill="x", padx=20, pady=20)
        
        self.lbl_subtotal = ctk.CTkLabel(row3, text="Subtotal: ₹0.00", font=ctk.CTkFont(size=14), text_color="#6b7280")
        self.lbl_subtotal.pack(side="left", padx=20)
        
        self.lbl_tax = ctk.CTkLabel(row3, text="Total Tax: ₹0.00", font=ctk.CTkFont(size=14), text_color="#6b7280")
        self.lbl_tax.pack(side="left", padx=20)
        
        self.lbl_total = ctk.CTkLabel(row3, text="Final Amount: ₹0.00", font=ctk.CTkFont(size=20, weight="bold"), text_color="#10b981")
        self.lbl_total.pack(side="left", padx=40)
        
        ctk.CTkButton(row3, text="Generate Invoice", command=self.generate_invoice, fg_color="#10b981", hover_color="#059669", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=10)
        ctk.CTkButton(row3, text="Clear", command=self.clear_cart, fg_color="transparent", border_width=1, text_color="#ef4444").pack(side="right", padx=10)
        
        self.load_dropdowns()

    def load_dropdowns(self):
        try:
            customers = self.db.get_all("customers")
            products = self.db.get_all("products")
            
            c_vals = [f"{c['id']} - {c['name']}" for c in customers]
            p_vals = [f"{p['id']} - {p['name']}" for p in products]
            
            if c_vals:
                self.customer_dropdown.configure(values=c_vals)
                self.customer_var.set(c_vals[0])
            if p_vals:
                self.product_dropdown.configure(values=p_vals)
                self.product_var.set(p_vals[0])
        except Exception:
            pass

    def add_to_cart(self):
        prod_val = self.product_var.get()
        if not prod_val: return
        prod_id = int(prod_val.split(" - ")[0])
        product = self.db.get_by_id("products", prod_id)
        
        try:
            qty = int(self.qty_var.get())
            discount_pct = float(self.discount_var.get())
            base_price = product['selling_price']
            discount_amt = base_price * (discount_pct / 100)
            price_after_discount = base_price - discount_amt
            gst_pct = product['gst_percentage']
            tax_amt = price_after_discount * (gst_pct / 100)
            item_total = (price_after_discount + tax_amt) * qty
            
            item_data = {
                "product_id": product['id'], "name": product['name'], "quantity": qty,
                "price": base_price, "discount": discount_amt * qty, "gst_percentage": gst_pct,
                "tax_amount": tax_amt * qty, "subtotal": price_after_discount * qty, "total": item_total
            }
            
            self.cart_items.append(item_data)
            self.cart_tree.insert("", "end", values=(item_data['product_id'], item_data['name'], item_data['quantity'], f"₹{item_data['price']:.2f}", f"₹{item_data['discount']:.2f}", f"{item_data['gst_percentage']}%", f"₹{item_data['total']:.2f}"))
            self.update_totals()
        except:
            pass

    def update_totals(self):
        self.total_subtotal = sum(item['subtotal'] for item in self.cart_items)
        self.total_tax = sum(item['tax_amount'] for item in self.cart_items)
        self.final_amount = sum(item['total'] for item in self.cart_items)
        self.lbl_subtotal.configure(text=f"Subtotal: ₹{self.total_subtotal:.2f}")
        self.lbl_tax.configure(text=f"Total Tax: ₹{self.total_tax:.2f}")
        self.lbl_total.configure(text=f"Final Amount: ₹{self.final_amount:.2f}")

    def clear_cart(self):
        self.cart_items = []
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        self.update_totals()

    def generate_invoice(self):
        if not self.cart_items: return
        cust_val = self.customer_var.get()
        cust_id = int(cust_val.split(" - ")[0]) if cust_val else None
        cust_name = cust_val.split(" - ")[1] if cust_val else "Walk-in Customer"
        inv_number = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        qr_path, qr_hash = self.qr_service.generate_qr(inv_number, cust_name, self.final_amount)
        invoice_data = {
            "invoice_number": inv_number, "customer_id": cust_id, "company_id": 1,
            "subtotal": self.total_subtotal, "discount": sum(item['discount'] for item in self.cart_items),
            "cgst": self.total_tax / 2, "sgst": self.total_tax / 2, "igst": 0,
            "total_tax": self.total_tax, "total_amount": self.final_amount,
            "payment_method": self.payment_var.get(), "status": "Paid",
            "amount_paid": self.final_amount, "notes": "",
            "created_by": self.controller.current_user['id'] if self.controller.current_user else 1,
            "qr_hash": qr_hash
        }
        try:
            self.billing.generate_invoice(invoice_data, self.cart_items)
            self.report_service.generate_invoice_pdf(invoice_data, self.cart_items, qr_path)
            messagebox.showinfo("Success", f"Invoice {inv_number} generated successfully!")
            self.clear_cart()
            self.load_dropdowns()
        except Exception as e:
            messagebox.showerror("Error", str(e))
''',
    "reports_page.py": '''import customtkinter as ctk

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        ctk.CTkLabel(self, text="Reports Page (Coming Soon)", font=ctk.CTkFont(size=24)).pack(pady=50)
''',
    "settings_page.py": '''import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        ctk.CTkLabel(self, text="Settings Page (Coming Soon)", font=ctk.CTkFont(size=24)).pack(pady=50)
'''
}

for name, content in files.items():
    with open(os.path.join(gui_dir, name), 'w', encoding='utf-8') as f:
        f.write(content)








