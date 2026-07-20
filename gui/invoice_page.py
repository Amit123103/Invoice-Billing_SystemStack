"""
File: invoice_page.py

Purpose:
Provides the Point of Sale (POS) and Billing interface where cashiers create invoices.
It handles product selection, dynamic cart calculations (tax/discount), and triggers 
the final invoice creation + PDF generation.

Dependencies:
- customtkinter
- tkinter.ttk (Treeview)
- tkinter.messagebox
- database.queries (For fetching customers/products)
- services.billing_service (To save the final invoice)
- services.qr_service (To generate the verification QR code)
- services.report_service (To print the PDF)
- datetime (For generating unique invoice numbers based on timestamps)

Project: Smart ERP Billing System
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from database.queries import DatabaseQueries
from services.billing_service import BillingService
from services.qr_service import QRService
from services.report_service import ReportService
import datetime

# This class provides the Billing interface.
# It solves the problem of cashiers needing to manually calculate taxes and discounts
# by providing a dynamic, real-time "shopping cart" view.
# Its responsibility is to aggregate items into a cart, compute final totals, and dispatch to services.
class InvoicePage(ctk.CTkFrame):
    """
    GUI Frame for the Point of Sale / Invoice generation system.
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Instantiate necessary backend services
        self.db = DatabaseQueries()
        self.billing = BillingService()
        self.qr_service = QRService()
        self.report_service = ReportService()
        
        # ---------------------------------------------------------
        # State Variables
        # ---------------------------------------------------------
        # self.cart_items holds a list of dictionaries representing the products currently in the basket
        self.cart_items = []
        
        # Running totals
        self.total_subtotal = 0
        self.total_tax = 0
        self.final_amount = 0
        
        # ---------------------------------------------------------
        # Header Area
        # ---------------------------------------------------------
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Create Invoice", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")
        
        # ---------------------------------------------------------
        # Settings Card (Customer & Payment Selection)
        # ---------------------------------------------------------
        settings_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        settings_card.pack(fill="x", padx=30, pady=5)
        
        row1 = ctk.CTkFrame(settings_card, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=20)
        
        # Dropdown to select the customer being billed
        self.customer_var = ctk.StringVar()
        self.customer_dropdown = ctk.CTkOptionMenu(row1, variable=self.customer_var, values=[], width=300, fg_color="#f9fafb", text_color="#111827")
        self.customer_dropdown.pack(side="left", padx=10)
        
        # Dropdown to select how the customer is paying
        self.payment_var = ctk.StringVar(value="Cash")
        ctk.CTkOptionMenu(row1, variable=self.payment_var, values=["Cash", "Card", "UPI", "Bank Transfer"], width=200, fg_color="#f9fafb", text_color="#111827").pack(side="left", padx=10)
        
        # ---------------------------------------------------------
        # Product Selection Card (Adding to Cart)
        # ---------------------------------------------------------
        prod_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        prod_card.pack(fill="x", padx=30, pady=10)
        
        row2 = ctk.CTkFrame(prod_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=20)
        
        # Dropdown to select which product to add to the cart
        self.product_var = ctk.StringVar()
        self.product_dropdown = ctk.CTkOptionMenu(row2, variable=self.product_var, values=[], width=300, fg_color="#f9fafb", text_color="#111827")
        self.product_dropdown.pack(side="left", padx=10)
        
        # Quantity input field
        self.qty_var = ctk.StringVar(value="1")
        ctk.CTkEntry(row2, textvariable=self.qty_var, placeholder_text="Qty", width=80).pack(side="left", padx=10)
        
        # Discount percentage input field (applied per item)
        self.discount_var = ctk.StringVar(value="0")
        ctk.CTkEntry(row2, textvariable=self.discount_var, placeholder_text="Discount %", width=100).pack(side="left", padx=10)
        
        # Button to process the selection and push it into the cart
        ctk.CTkButton(row2, text="Add to Cart", command=self.add_to_cart, fg_color="#2563eb").pack(side="left", padx=20)
        
        # ---------------------------------------------------------
        # Shopping Cart Data Grid (Treeview)
        # ---------------------------------------------------------
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
        
        # ---------------------------------------------------------
        # Footer / Totals Card
        # ---------------------------------------------------------
        totals_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        totals_card.pack(fill="x", padx=30, pady=10)
        
        row3 = ctk.CTkFrame(totals_card, fg_color="transparent")
        row3.pack(fill="x", padx=20, pady=20)
        
        # Subtotal display (Price before tax)
        self.lbl_subtotal = ctk.CTkLabel(row3, text="Subtotal: ₹0.00", font=ctk.CTkFont(size=14), text_color="#6b7280")
        self.lbl_subtotal.pack(side="left", padx=20)
        
        # Total Tax display
        self.lbl_tax = ctk.CTkLabel(row3, text="Total Tax: ₹0.00", font=ctk.CTkFont(size=14), text_color="#6b7280")
        self.lbl_tax.pack(side="left", padx=20)
        
        # Final Grand Total display
        self.lbl_total = ctk.CTkLabel(row3, text="Final Amount: ₹0.00", font=ctk.CTkFont(size=20, weight="bold"), text_color="#10b981")
        self.lbl_total.pack(side="left", padx=40)
        
        # Button to finalize the transaction
        ctk.CTkButton(row3, text="Generate Invoice", command=self.generate_invoice, fg_color="#10b981", hover_color="#059669", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=10)
        # Button to wipe the cart empty
        ctk.CTkButton(row3, text="Clear", command=self.clear_cart, fg_color="transparent", border_width=1, text_color="#ef4444").pack(side="right", padx=10)
        
        # Pre-fill the Customer and Product dropdowns with data from the database
        self.load_dropdowns()

    # Purpose:
    # Populates the dropdown menus by querying the latest customers and products.
    def load_dropdowns(self):
        """
        Fetches database records to populate the UI dropdown menus.
        """
        try:
            # Query all customers and products
            customers = self.db.get_all("customers")
            products = self.db.get_all("products")
            
            # Format the data into lists of strings like "1 - John Doe" so the user can see both ID and Name
            c_vals = [f"{c['id']} - {c['name']}" for c in customers]
            p_vals = [f"{p['id']} - {p['name']}" for p in products]
            
            # If the database isn't empty, inject the values into the UI dropdowns
            if c_vals:
                self.customer_dropdown.configure(values=c_vals)
                self.customer_var.set(c_vals[0]) # Default to the first customer
            if p_vals:
                self.product_dropdown.configure(values=p_vals)
                self.product_var.set(p_vals[0])
        except Exception:
            # If the database is missing or empty, ignore it gracefully
            pass

    # Purpose:
    # Reads the currently selected product, applies quantity and discount, 
    # calculates item-level taxes, and adds it to the cart matrix.
    def add_to_cart(self):
        """
        Calculates prices and adds the selected product to the shopping cart.
        """
        # Get the string value from the dropdown (e.g., "14 - Apple iPhone")
        prod_val = self.product_var.get()
        if not prod_val: return
        
        # Extract just the numeric ID by splitting the string at " - "
        prod_id = int(prod_val.split(" - ")[0])
        
        # Fetch the complete product details from the database so we have its price and tax bracket
        product = self.db.get_by_id("products", prod_id)
        
        try:
            # Convert user inputs from strings to numerical types
            qty = int(self.qty_var.get())
            discount_pct = float(self.discount_var.get())
            
            # Financial Mathematics:
            # 1. Base price of one unit
            base_price = product['selling_price']
            
            # 2. How much monetary value is the discount percentage worth?
            discount_amt = base_price * (discount_pct / 100)
            
            # 3. New price per unit after subtracting the discount
            price_after_discount = base_price - discount_amt
            
            # 4. What is the GST percentage?
            gst_pct = product['gst_percentage']
            
            # 5. How much monetary tax applies to the discounted unit price?
            tax_amt = price_after_discount * (gst_pct / 100)
            
            # 6. Final grand total for this specific item row (Qty * (Unit + Tax))
            item_total = (price_after_discount + tax_amt) * qty
            
            # Bundle all these calculations into a clean dictionary
            item_data = {
                "product_id": product['id'], 
                "name": product['name'], 
                "quantity": qty,
                "price": base_price, 
                "discount": discount_amt * qty, 
                "gst_percentage": gst_pct,
                "tax_amount": tax_amt * qty, 
                # Subtotal is the total WITHOUT tax
                "subtotal": price_after_discount * qty, 
                # Total is the total WITH tax
                "total": item_total
            }
            
            # Append to our internal state list
            self.cart_items.append(item_data)
            
            # Visually append a new row to the Treeview so the cashier sees it
            self.cart_tree.insert("", "end", values=(
                item_data['product_id'], item_data['name'], item_data['quantity'], 
                f"₹{item_data['price']:.2f}", f"₹{item_data['discount']:.2f}", 
                f"{item_data['gst_percentage']}%", f"₹{item_data['total']:.2f}"
            ))
            
            # Recalculate the master totals at the bottom of the screen
            self.update_totals()
        except Exception:
            # Ignore invalid float/int casting errors
            pass

    # Purpose:
    # Recalculates the master Subtotal, Tax, and Grand Total by summing up everything in the cart.
    def update_totals(self):
        """
        Updates the footer UI labels with recalculated totals from all cart items.
        """
        # A list comprehension sum() allows us to add up a specific dictionary key across all items efficiently
        self.total_subtotal = sum(item['subtotal'] for item in self.cart_items)
        self.total_tax = sum(item['tax_amount'] for item in self.cart_items)
        self.final_amount = sum(item['total'] for item in self.cart_items)
        
        # Update the text labels in the UI, formatting the floats to 2 decimal places (e.g. ₹10.50)
        self.lbl_subtotal.configure(text=f"Subtotal: ₹{self.total_subtotal:.2f}")
        self.lbl_tax.configure(text=f"Total Tax: ₹{self.total_tax:.2f}")
        self.lbl_total.configure(text=f"Final Amount: ₹{self.final_amount:.2f}")

    # Purpose:
    # Empties the shopping basket and resets all totals to zero.
    def clear_cart(self):
        """
        Wipes the cart data and clears the Treeview visually.
        """
        # Empty internal memory array
        self.cart_items = []
        
        # Empty visual rows
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
            
        # Re-trigger total math (which will now sum up to zero)
        self.update_totals()

    # Purpose:
    # Finalizes the checkout. It generates a QR code, saves data to SQLite, prints the PDF, and clears the cart.
    def generate_invoice(self):
        """
        Finalizes the transaction, writes to the database, and creates the PDF.
        """
        # Validation: Don't generate an empty invoice
        if not self.cart_items: return
        
        # Determine the selected customer's ID
        cust_val = self.customer_var.get()
        cust_id = int(cust_val.split(" - ")[0]) if cust_val else None
        cust_name = cust_val.split(" - ")[1] if cust_val else "Walk-in Customer"
        
        # Generate a unique, time-based invoice number (e.g. INV-20231024153000)
        inv_number = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # First, generate the cryptographic QR code image
        qr_path, qr_hash = self.qr_service.generate_qr(inv_number, cust_name, self.final_amount)
        
        # Package the master invoice header details into a dictionary expected by BillingService
        invoice_data = {
            "invoice_number": inv_number, 
            "customer_id": cust_id, 
            "company_id": 1, # Default company ID
            "subtotal": self.total_subtotal, 
            "discount": sum(item['discount'] for item in self.cart_items),
            "cgst": self.total_tax / 2, # Assuming Intra-state 50/50 split for this demo
            "sgst": self.total_tax / 2, 
            "igst": 0,
            "total_tax": self.total_tax, 
            "total_amount": self.final_amount,
            "payment_method": self.payment_var.get(), 
            "status": "Paid",
            "amount_paid": self.final_amount, 
            "notes": "",
            # Check who is logged in via the master controller. Fallback to ID 1 if None.
            "created_by": self.controller.current_user['id'] if self.controller.current_user else 1,
            "qr_hash": qr_hash
        }
        
        try:
            # Phase 1: Save the invoice and its items to the SQLite Database (deducts stock internally)
            self.billing.generate_invoice(invoice_data, self.cart_items)
            
            # Phase 2: Paint the PDF Document and save it to disk
            self.report_service.generate_invoice_pdf(invoice_data, self.cart_items, qr_path)
            
            # Phase 3: Notify cashier of success
            messagebox.showinfo("Success", f"Invoice {inv_number} generated successfully!")
            
            # Phase 4: Prepare the UI for the next customer
            self.clear_cart()
            self.load_dropdowns()
            
        except Exception as e:
            # If the database fails (e.g. locked file), show the error so the app doesn't crash silently
            messagebox.showerror("Error", str(e))
