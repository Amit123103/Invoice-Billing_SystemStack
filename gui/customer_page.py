import customtkinter as ctk
from tkinter import ttk, messagebox
from database.queries import DatabaseQueries

class CustomerPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.db = DatabaseQueries()
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Customer Directory", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")
        
        # Form Card
        form_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        form_card.pack(fill="x", padx=30, pady=10)
        
        row1 = ctk.CTkFrame(form_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(20, 10))
        
        self.name_var = ctk.StringVar()
        ctk.CTkEntry(row1, textvariable=self.name_var, placeholder_text="Customer Name", width=200).pack(side="left", padx=10)
        
        self.phone_var = ctk.StringVar()
        ctk.CTkEntry(row1, textvariable=self.phone_var, placeholder_text="Phone Number", width=200).pack(side="left", padx=10)
        
        self.email_var = ctk.StringVar()
        ctk.CTkEntry(row1, textvariable=self.email_var, placeholder_text="Email Address", width=200).pack(side="left", padx=10)
        
        self.gst_var = ctk.StringVar()
        ctk.CTkEntry(row1, textvariable=self.gst_var, placeholder_text="GST Number", width=200).pack(side="left", padx=10)
        
        row2 = ctk.CTkFrame(form_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 20))
        
        self.address_var = ctk.StringVar()
        ctk.CTkEntry(row2, textvariable=self.address_var, placeholder_text="Address", width=640).pack(side="left", padx=10)
        
        ctk.CTkButton(row2, text="Add Customer", command=self.add_customer, fg_color="#2563eb", hover_color="#1d4ed8").pack(side="left", padx=20)
        
        # Table Card
        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)
        
        columns = ("ID", "Name", "Phone", "Email", "GST Number", "Address")
        
        # Create a style for ttk.Treeview to look modern
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
        
        self.load_customers()

    def add_customer(self):
        name = self.name_var.get()
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
            
        self.db.add_customer(
            name, 
            self.phone_var.get(), 
            self.email_var.get(), 
            self.gst_var.get(), 
            self.address_var.get()
        )
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.gst_var.set("")
        self.address_var.set("")
        
        self.load_customers()
        
    def load_customers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        customers = self.db.get_all("customers")
        for c in customers:
            self.tree.insert("", "end", values=(c['id'], c['name'], c['phone'], c['email'], c['gst_number'], c['address']))
