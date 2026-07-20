"""
File: inventory_page.py

Purpose:
Provides the graphical interface for managing Products and Inventory Stock.

Dependencies:
- customtkinter
- tkinter.ttk (Treeview)
- tkinter.messagebox
- database.queries

"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from database.queries import DatabaseQueries

# This class handles the Inventory Management screen.
# It solves the problem of allowing users to define what they are selling and set prices/taxes.
# Its responsibility is to provide a form for product creation and a table to view stock levels.
class InventoryPage(ctk.CTkFrame):
    """
    GUI Frame for managing Inventory Products.
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Instantiate Database manager
        self.db = DatabaseQueries()
        
        # ---------------------------------------------------------
        # Header
        # ---------------------------------------------------------
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Inventory Management", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")
        
        # ---------------------------------------------------------
        # Product Entry Form Card
        # ---------------------------------------------------------
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
        
        # ---------------------------------------------------------
        # Data Grid (Treeview) Card
        # ---------------------------------------------------------
        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)
        
        columns = ("ID", "Name", "Category", "HSN", "Cost", "Selling", "GST", "Stock")
        
        # Apply modern CSS-like styling to the standard Tkinter Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#FFFFFF", foreground="#111827", rowheight=40, borderwidth=0)
        style.configure("Treeview.Heading", background="#f9fafb", foreground="#6b7280", font=('Helvetica', 10, 'bold'), borderwidth=0)
        
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")
            
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Populate the table when the frame loads
        self.load_products()

    # Purpose:
    # Reads the input fields, converts strings to floats/ints, and saves the new product.
    def add_product(self):
        """
        Event handler for adding a new product.
        """
        try:
            name = self.name_var.get()
            if not name: return
            
            # We must wrap numerical inputs in float() or int() because UI fields return raw strings.
            # We use 'or 0' to prevent crashes if the user leaves the field totally blank.
            self.db.add_product(
                name, 
                self.category_var.get(), 
                self.hsn_var.get(), 
                float(self.cost_var.get() or 0), 
                float(self.selling_var.get() or 0), 
                float(self.gst_var.get() or 0), 
                int(self.stock_var.get() or 0), 
                None # Supplier ID is omitted for now in this simple version
            )
            
            # Clear UI fields on success
            self.name_var.set("")
            self.category_var.set("")
            self.hsn_var.set("")
            self.cost_var.set("")
            self.selling_var.set("")
            self.gst_var.set("")
            self.stock_var.set("")
            
            # Refresh UI grid
            self.load_products()
        except ValueError:
            # If the user types "abc" into the Price field, float() will throw a ValueError.
            # In a production app, we would show a messagebox error here.
            pass

    # Purpose:
    # Fetches all products and updates the Treeview.
    def load_products(self):
        """
        Refreshes the product data grid.
        """
        # Wipe old rows
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Fetch new data and insert rows
        for p in self.db.get_all("products"):
            self.tree.insert("", "end", values=(p['id'], p['name'], p['category'], p['hsn_code'], p['cost_price'], p['selling_price'], p['gst_percentage'], p['stock_quantity']))




