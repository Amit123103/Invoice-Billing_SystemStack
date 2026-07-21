############################################################
# Project : Smart ERP Billing System
#
# File    : inventory_page.py
#
# Team Member :
# Team Member 2
#
# Module :
# Inventory Management
#
# Responsibilities :
# - Product CRUD
# - Inventory
# - Categories
# - Supplier Management
#
# Developed By :
# Team Member 2
############################################################
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

###########################################################
# Team Member 2
# Module: Inventory Management
# Completed:
# - Product CRUD
# - Inventory
# - Categories
# - Supplier Management
###########################################################
import customtkinter as ctk
from tkinter import ttk, messagebox
from database.queries import DatabaseQueries

# This class handles the Inventory Management screen.
# It solves the problem of allowing users to define what they are selling and set prices/taxes.
# Its responsibility is to provide a form for product creation and a table to view stock levels.
# ---------------------------------------------
# Team Member 2
# Class: InventoryPage
# Purpose:
# GUI Frame for managing Inventory Products.
# ---------------------------------------------
class InventoryPage(ctk.CTkFrame):
    """
    GUI Frame for managing Inventory Products.
    """
    
    # ---------------------------------------------
    # Team Member 2
    # Function: __init__
    # Purpose:
    # Handles logic for   init  
    # ---------------------------------------------
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
        
        # Helper function to create a labeled input field
        # ---------------------------------------------
        # Team Member 2
        # Function: create_input
        # Purpose:
        # Handles logic for create input
        # ---------------------------------------------
        def create_input(parent, label_text, width):
            wrapper = ctk.CTkFrame(parent, fg_color="transparent")
            wrapper.pack(side="left", padx=10)
            ctk.CTkLabel(wrapper, text=label_text, text_color="#374151", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=2)
            entry = ctk.CTkEntry(wrapper, placeholder_text=label_text, width=width)
            entry.pack(fill="x")
            return entry

        row1 = ctk.CTkFrame(form_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(15, 10))
        
        self.name_entry = create_input(row1, "Product Name", 200)
        self.category_entry = create_input(row1, "Category", 150)
        self.hsn_entry = create_input(row1, "HSN Code", 150)
        
        row2 = ctk.CTkFrame(form_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 20))
        
        self.cost_entry = create_input(row2, "Cost Price", 120)
        self.selling_entry = create_input(row2, "Selling Price", 120)
        self.gst_entry = create_input(row2, "GST %", 120)
        self.stock_entry = create_input(row2, "Stock Qty", 120)
        
        # Add a wrapper for the button to align it nicely at the bottom
        btn_wrapper = ctk.CTkFrame(row2, fg_color="transparent")
        btn_wrapper.pack(side="left", padx=20)
        # Empty label to match the height of the field labels so the button aligns with the text boxes
        ctk.CTkLabel(btn_wrapper, text="").pack()
        ctk.CTkButton(btn_wrapper, text="Add Product", command=self.add_product, fg_color="#2563eb", hover_color="#1d4ed8").pack()
        
        # ---------------------------------------------------------
        # Data Grid (Treeview) Card
        # ---------------------------------------------------------
        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)
        
        search_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.load_products(self.search_var.get()))
        
        ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search by Name, Category, HSN...", width=300).pack(side="left")
        
        columns = ("ID", "Name", "Category", "HSN", "Cost", "Selling", "GST", "Stock")
        
        # Apply modern CSS-like styling to the standard Tkinter Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#FFFFFF", foreground="#111827", rowheight=40, borderwidth=0)
        style.configure("Treeview.Heading", background="#f9fafb", foreground="#6b7280", font=('Helvetica', 10, 'bold'), borderwidth=0)
        
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", style="Treeview")
        self.tree.tag_configure('low_stock', foreground='#dc2626') # Red text for low stock
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")
            
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Populate the table when the frame loads
        self.load_products()

    # Purpose:
    # Reads the input fields, converts strings to floats/ints, and saves the new product.
    # ---------------------------------------------
    # Team Member 2
    # Function: add_product
    # Purpose:
    # Event handler for adding a new product.
    # ---------------------------------------------
    def add_product(self):
        """
        Event handler for adding a new product.
        """
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Validation Error", "Product Name is required.")
            return
            
        try:
            # We must wrap numerical inputs in float() or int() because UI fields return raw strings.
            # We use 'or 0' to prevent crashes if the user leaves the field totally blank.
            cost = float(self.cost_entry.get() or 0)
            selling = float(self.selling_entry.get() or 0)
            gst = float(self.gst_entry.get() or 0)
            stock = int(self.stock_entry.get() or 0)
        except ValueError:
            messagebox.showerror("Validation Error", "Cost Price, Selling Price, GST %, and Stock Qty must be numeric values.")
            return

        try:
            self.db.add_product(
                name, 
                self.category_entry.get(), 
                self.hsn_entry.get(), 
                cost, 
                selling, 
                gst, 
                stock, 
                None # Supplier ID is omitted for now in this simple version
            )
            
            # Clear UI fields on success
            self.name_entry.delete(0, 'end')
            self.category_entry.delete(0, 'end')
            self.hsn_entry.delete(0, 'end')
            self.cost_entry.delete(0, 'end')
            self.selling_entry.delete(0, 'end')
            self.gst_entry.delete(0, 'end')
            self.stock_entry.delete(0, 'end')
            
            # Refresh UI grid
            self.load_products()
            messagebox.showinfo("Success", "Product added successfully!")
            
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    # Purpose:
    # Fetches all products and updates the Treeview.
    # ---------------------------------------------
    # Team Member 2
    # Function: load_products
    # Purpose:
    # Refreshes the product data grid.
    # ---------------------------------------------
    def load_products(self, search_query=""):
        """
        Refreshes the product data grid.
        """
        # Wipe old rows
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        if search_query:
            products = self.db.search_products(search_query)
        else:
            products = self.db.get_all("products")
            
        # Fetch new data and insert rows
        for p in products:
            item_id = self.tree.insert("", "end", values=(p['id'], p['name'], p['category'], p['hsn_code'], p['cost_price'], p['selling_price'], p['gst_percentage'], p['stock_quantity']))
            if p['stock_quantity'] < 10:
                self.tree.item(item_id, tags=('low_stock',))




