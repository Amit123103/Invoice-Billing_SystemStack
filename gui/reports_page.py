"""
File: reports_page.py

Purpose:
A UI screen for Analytical Reporting features.

Dependencies:
- customtkinter
- tkinter.ttk

"""

import customtkinter as ctk
from tkinter import ttk
from database.queries import DatabaseQueries

class ReportsPage(ctk.CTkFrame):
    """
    GUI Frame for Business Reports.
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.db = DatabaseQueries()
        
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Business Reports", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")
        
        # Refresh Button
        ctk.CTkButton(header, text="Refresh Data", command=self.load_data, fg_color="#2563eb", hover_color="#1d4ed8").pack(side="right")
        
        # Summary Cards Container
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30, pady=10)
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Create 4 cards
        self.sales_var = ctk.StringVar(value="₹0.00")
        self.invoices_var = ctk.StringVar(value="0")
        self.customers_var = ctk.StringVar(value="0")
        self.products_var = ctk.StringVar(value="0")
        
        self.create_summary_card(cards_frame, "Total Revenue", self.sales_var, 0, "#ecfdf5", "#059669")
        self.create_summary_card(cards_frame, "Total Invoices", self.invoices_var, 1, "#eff6ff", "#2563eb")
        self.create_summary_card(cards_frame, "Total Customers", self.customers_var, 2, "#fef2f2", "#dc2626")
        self.create_summary_card(cards_frame, "Products in Stock", self.products_var, 3, "#fffbeb", "#d97706")
        
        # Data Grid for Recent Invoices
        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)
        
        ctk.CTkLabel(table_card, text="Recent Transactions", font=ctk.CTkFont(size=16, weight="bold"), text_color="#111827").pack(anchor="w", padx=20, pady=(20, 0))
        
        columns = ("Date", "Invoice #", "Customer", "Amount", "Status")
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#FFFFFF", foreground="#111827", rowheight=40, fieldbackground="#FFFFFF", borderwidth=0)
        style.map('Treeview', background=[('selected', '#eff6ff')])
        style.configure("Treeview.Heading", background="#f9fafb", foreground="#6b7280", font=('Helvetica', 10, 'bold'), borderwidth=0)
        
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="w")
            
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Bind the frame to update whenever it's raised/shown
        self.bind("<Map>", lambda e: self.load_data())
        self.load_data()
        
    def create_summary_card(self, parent, title, variable, col, bg_color, text_color):
        card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=12)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color=text_color).pack(pady=(20, 5))
        ctk.CTkLabel(card, textvariable=variable, font=ctk.CTkFont(size=24, weight="bold"), text_color=text_color).pack(pady=(0, 20))
        
    def load_data(self):
        # Fetch data
        invoices = [dict(row) for row in self.db.get_all("invoices")]
        customers = [dict(row) for row in self.db.get_all("customers")]
        products = [dict(row) for row in self.db.get_all("products")]
        
        customer_map = {c['id']: c['name'] for c in customers}
        
        # Calculate metrics
        total_revenue = sum(inv.get('total_amount', 0) for inv in invoices if inv.get('status') in ('Paid', 'Pending', 'Partial'))
        total_invoices = len(invoices)
        total_customers = len(customers)
        total_products = len(products)
        
        self.sales_var.set(f"₹{total_revenue:,.2f}")
        self.invoices_var.set(str(total_invoices))
        self.customers_var.set(str(total_customers))
        self.products_var.set(str(total_products))
        
        # Clear treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Sort invoices by date descending
        sorted_invoices = sorted(invoices, key=lambda x: x.get('id', 0), reverse=True)
        
        for inv in sorted_invoices:
            cust_name = customer_map.get(inv.get('customer_id'), "Unknown")
            created_at = inv.get('created_at', 'N/A')
            date_str = str(created_at).split(" ")[0] if created_at else "N/A"
            amt_str = f"₹{inv.get('total_amount', 0):,.2f}"
            self.tree.insert("", "end", values=(
                date_str, 
                inv.get('invoice_number', 'N/A'), 
                cust_name, 
                amt_str, 
                inv.get('status', 'N/A')
            ))






