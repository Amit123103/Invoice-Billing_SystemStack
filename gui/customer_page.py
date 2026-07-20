"""
File: customer_page.py

Purpose:
Provides the graphical interface for managing Customer records (Adding, Viewing).

Dependencies:
- customtkinter
- tkinter.ttk (For the Treeview table component)
- tkinter.messagebox (For error/success popups)
- database.queries

"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from database.queries import DatabaseQueries

# This class manages the Customer Directory UI.
# It solves the problem of needing a user-friendly way for cashiers/managers to input 
# and view client details without touching raw databases.
# Its responsibility is capturing customer data via a form and displaying it in a data grid.
class CustomerPage(ctk.CTkFrame):
    """
    GUI Frame for managing Customers.
    """
    
    def __init__(self, parent, controller):
        # Set background to transparent so it inherits the Dashboard's gray background
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Instantiate the database DAO
        self.db = DatabaseQueries()
        
        # ---------------------------------------------------------
        # Header Section
        # ---------------------------------------------------------
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Customer Directory", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")
        
        # ---------------------------------------------------------
        # Customer Entry Form Card
        # ---------------------------------------------------------
        form_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        form_card.pack(fill="x", padx=30, pady=10)
        
        # Row 1 of inputs (Name, Phone, Email, GST)
        row1 = ctk.CTkFrame(form_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(20, 10))
        
        self.name_entry = ctk.CTkEntry(row1, placeholder_text="Customer Name", width=200)
        self.name_entry.pack(side="left", padx=10)
        
        self.phone_entry = ctk.CTkEntry(row1, placeholder_text="Phone Number", width=200)
        self.phone_entry.pack(side="left", padx=10)
        
        self.email_entry = ctk.CTkEntry(row1, placeholder_text="Email Address", width=200)
        self.email_entry.pack(side="left", padx=10)
        
        self.gst_entry = ctk.CTkEntry(row1, placeholder_text="GST Number", width=200)
        self.gst_entry.pack(side="left", padx=10)
        
        # Row 2 of inputs (Address and Submit Button)
        row2 = ctk.CTkFrame(form_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 20))
        
        self.address_entry = ctk.CTkEntry(row2, placeholder_text="Address", width=640)
        self.address_entry.pack(side="left", padx=10)
        
        # Connect the button click to self.add_customer()
        ctk.CTkButton(row2, text="Add Customer", command=self.add_customer, fg_color="#2563eb", hover_color="#1d4ed8").pack(side="left", padx=20)
        
        # ---------------------------------------------------------
        # Data Grid (Treeview) Card
        # ---------------------------------------------------------
        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)
        
        search_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.load_customers(self.search_var.get()))
        
        ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search by Name, Phone, Email...", width=300).pack(side="left")
        
        # Define the columns that will appear in the table
        columns = ("ID", "Name", "Phone", "Email", "GST Number", "Address")
        
        # Standard Tkinter Treeviews look outdated, so we manually restyle them using ttk.Style
        # to match the modern web aesthetic (white background, flat borders, tall rows)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#FFFFFF", foreground="#111827", rowheight=40, fieldbackground="#FFFFFF", borderwidth=0)
        style.map('Treeview', background=[('selected', '#eff6ff')])
        style.configure("Treeview.Heading", background="#f9fafb", foreground="#6b7280", font=('Helvetica', 10, 'bold'), borderwidth=0)
        
        # Create the Treeview widget
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            # Make the columns slightly wider and left-aligned
            self.tree.column(col, width=150, anchor="w")
            
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Automatically fetch and display customers on page load
        self.load_customers()

    # Purpose:
    # Validates input and saves a new customer to the database when the Add button is clicked.
    def add_customer(self):
        """
        Event handler for adding a new customer.
        """
        name = self.name_entry.get()
        
        # Basic data validation: Name is mandatory
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
            
        # Execute the database insertion
        self.db.add_customer(
            name, 
            self.phone_entry.get(), 
            self.email_entry.get(), 
            self.gst_entry.get(), 
            self.address_entry.get()
        )
        
        # Clear the input fields so the user can quickly type the next customer
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.gst_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
        
        # Refresh the table grid to show the newly added customer immediately
        self.load_customers()
        
    # Purpose:
    # Pulls all customer records from the database and populates the Treeview table.
    def load_customers(self, search_query=""):
        """
        Refreshes the customer data grid.
        """
        # Step 1: Wipe existing rows in the table to prevent duplicates
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Step 2: Fetch fresh data from DB
        if search_query:
            customers = self.db.search_customers(search_query)
        else:
            customers = self.db.get_all("customers")
        
        # Step 3: Insert each record as a new row in the Treeview
        for c in customers:
            self.tree.insert("", "end", values=(c['id'], c['name'], c['phone'], c['email'], c['gst_number'], c['address']))




