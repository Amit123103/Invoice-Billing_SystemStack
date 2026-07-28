############################################################
# Project : Smart ERP Billing System
#
# File    : invoice_page.py
#
# Team Member :Bhipender
# Team Member 4
#
# Module :
# Invoice & Reports
#
# Responsibilities :
# - Invoice Generation
# - Reports
# - Analytics
# - PDF Export
#
# Developed By :
# Team Member 4
############################################################
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
"""

###########################################################
# Team Member 4
# Module: Invoice & Reports
# Completed:
# - Invoice Generation
# - Reports
# - Analytics
# - PDF Export
###########################################################
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog

from matplotlib import style
from database.queries import DatabaseQueries
from services.billing_service import BillingService
from services.qr_service import QRService
from services.report_service import ReportService
import datetime
import os

# This class provides the Billing interface.
# It solves the problem of cashiers needing to manually calculate taxes and discounts
# by providing a dynamic, real-time "shopping cart" view.
# Its responsibility is to aggregate items into a cart, compute final totals, and dispatch to services.
# ---------------------------------------------
# Team Member 4
# Class: InvoicePage
# Purpose:
# GUI Frame for the Point of Sale / Invoice generation system.
# ---------------------------------------------
class InvoicePage(ctk.CTkFrame):
    """
    GUI Frame for the Point of Sale / Invoice generation system.
    """
    
    # ---------------------------------------------
    # Team Member 4
    # Function: __init__
    # Purpose:
    # Handles logic for   init  
    # ---------------------------------------------
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
        customer_frame = ctk.CTkFrame(row1, fg_color="transparent")
        customer_frame.pack(side="left", padx=10)

        ctk.CTkLabel(
            customer_frame,
    text="Customer",
    font=ctk.CTkFont(size=13, weight="bold")
).pack(anchor="w")

        self.customer_search_var = ctk.StringVar()

        self.customer_var = ctk.StringVar()

        customer_search = ctk.CTkEntry(
            customer_frame,
            textvariable=self.customer_search_var,
            placeholder_text="🔍 Search Customer...",
            width=250
        )
        customer_search.pack(pady=(0, 5))
        # Filter customers while typing
        self.customer_search_var.trace_add(
            "write",
            self.filter_customers
        )

        self.customer_dropdown = ctk.CTkOptionMenu(
    customer_frame,
    variable=self.customer_var,
    values=[],
    width=250,
    fg_color="#f9fafb",
    text_color="#111827"
)
        self.customer_dropdown.pack()
        
        # Dropdown to select how the customer is paying
        payment_frame = ctk.CTkFrame(row1, fg_color="transparent")
        payment_frame.pack(side="left", padx=30)

        ctk.CTkLabel(
    payment_frame,
    text="Payment Method",
    font=ctk.CTkFont(size=13, weight="bold")
    ).pack(anchor="w")

        self.payment_var = ctk.StringVar(value="Cash")

        self.payment_dropdown = ctk.CTkOptionMenu(
    payment_frame,
    variable=self.payment_var,
    values=["Cash", "Card", "UPI", "Bank Transfer"],
    width=200,
    fg_color="#f9fafb",
    text_color="#111827"
)
        self.payment_dropdown.pack()
        
        # ---------------------------------------------------------
        # Product Selection Card (Adding to Cart)
        # ---------------------------------------------------------
        prod_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        prod_card.pack(fill="x", padx=30, pady=10)
        
        row2 = ctk.CTkFrame(prod_card, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=20)
        
        # Dropdown to select which product to add to the cart
        product_frame = ctk.CTkFrame(row2, fg_color="transparent")
        product_frame.pack(side="left", padx=10)

        ctk.CTkLabel(
            product_frame,
            text="Product",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w")

        # Search Box
        self.search_var = ctk.StringVar()

        search_entry = ctk.CTkEntry(
            product_frame,
            textvariable=self.search_var,
            placeholder_text="🔍 Search Product...",
            width=250
        )
        search_entry.pack(pady=(0,5))

        # Update dropdown while typing
        self.search_var.trace_add("write", self.filter_products)

        # Product Dropdown
        self.product_var = ctk.StringVar()

        self.product_dropdown = ctk.CTkOptionMenu(
            product_frame,
            variable=self.product_var,
            values=[],
            width=250,
            fg_color="#f9fafb",
            text_color="#111827"
        )
        self.product_dropdown.pack()
        
        # Quantity input field
        qty_frame = ctk.CTkFrame(row2, fg_color="transparent")
        qty_frame.pack(side="left", padx=10)

        ctk.CTkLabel(
    qty_frame,
    text="Quantity",
    font=ctk.CTkFont(size=13, weight="bold")
).pack(anchor="w")

        self.qty_var = ctk.StringVar(value="1")

        ctk.CTkEntry(
    qty_frame,
    textvariable=self.qty_var,
    width=80
).pack()
        
        # Discount percentage input field (applied per item)
        discount_frame = ctk.CTkFrame(row2, fg_color="transparent")
        discount_frame.pack(side="left", padx=10)

        ctk.CTkLabel(
    discount_frame,
    text="Discount %",
    font=ctk.CTkFont(size=13, weight="bold")
).pack(anchor="w")

        self.discount_var = ctk.StringVar(value="0")

        ctk.CTkEntry(
    discount_frame,
    textvariable=self.discount_var,
    width=100
).pack()

        
        # Button to process the selection and push it into the cart
        ctk.CTkButton(
    row2,
    text="Add to Cart",
    command=self.add_to_cart,
    width=130,
    height=40,
    fg_color="#2563eb"
).pack(side="left", padx=8, pady=(20, 0))



        # Button to remove the currently selected item from the cart
        ctk.CTkButton(
    row2,
    text="Remove Selected item",
    command=self.remove_selected_item,
    width=130,
    height=40,
    fg_color="#dc2626",
    hover_color="#b91c1c"
).pack(side="left", padx=8, pady=(20, 0))
        
        # ---------------------------------------------------------
        # Shopping Cart Data Grid (Treeview)
        # ---------------------------------------------------------
        table_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=30, pady=5)
        
        cols = ("ID", "Name", "Qty", "Price", "Discount", "GST %", "Total")
        style = ttk.Style()

        style.theme_use("default")   # Important

        style.configure(
    "Treeview",
    background="white",
    foreground="black",
    fieldbackground="white",
    rowheight=35
)

        style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold")
)

        style.map(
    "Treeview",
    background=[("selected", "#BBDEFF")],
    foreground=[("selected", "black")]
)

        self.cart_tree = ttk.Treeview(
    table_card,
    columns=cols,
    show="headings",
    selectmode="browse"
)
        for c in cols:
         self.cart_tree.heading(c, text=c)
         self.cart_tree.column(c, width=120, anchor="center")

        self.cart_tree.pack(fill="both", expand=True, padx=20, pady=20)
        self.cart_tree.bind("<<TreeviewSelect>>", self.on_cart_select)
        
        # ---------------------------------------------------------
        # Footer / Totals Card
        # ---------------------------------------------------------
        totals_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        totals_card.pack(fill="x", padx=30, pady=10)
        
        row3 = ctk.CTkFrame(totals_card, fg_color="transparent")
        row3.pack(fill="x", padx=20, pady=20)
        
        # Subtotal display (Price before tax)
        self.lbl_subtotal = ctk.CTkLabel(row3, text="Subtotal: ₹0.00", font=ctk.CTkFont(size=12), text_color="#6b7280")
        self.lbl_subtotal.pack(side="left", padx=20)
        
        # Total Tax display
        self.lbl_tax = ctk.CTkLabel(row3, text="Total Tax: ₹0.00", font=ctk.CTkFont(size=12), text_color="#6b7280")
        self.lbl_tax.pack(side="left", padx=20)
        
        # Final Grand Total display
        self.lbl_total = ctk.CTkLabel(row3, text="Final Amount: ₹0.00", font=ctk.CTkFont(size=18, weight="bold"), text_color="#10b981")
        self.lbl_total.pack(side="left", padx=20)
        
        # Amount Paid Input
        paid_frame = ctk.CTkFrame(row3, fg_color="transparent")
        paid_frame.pack(side="left", padx=20)
        ctk.CTkLabel(paid_frame, text="Amount Paid: ₹", font=ctk.CTkFont(size=12), text_color="#6b7280").pack(side="left")
        self.amount_paid_var = ctk.StringVar(value="0")
        # Update paid and due amounts whenever the value changes
        self.amount_paid_var.trace_add(
            "write",
            self.update_payment_status
        )
        ctk.CTkEntry(paid_frame, textvariable=self.amount_paid_var, width=80).pack(side="left", padx=5)
        # Paid Amount Display
        self.lbl_paid = ctk.CTkLabel(
            row3,
            text="Paid: ₹0.00",
            font=ctk.CTkFont(size=12),
            text_color="#16a34a"
        )
        self.lbl_paid.pack(side="left", padx=20)

        # Due Amount Display
        self.lbl_due = ctk.CTkLabel(
            row3,
            text="Due: ₹0.00",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#dc2626"
        )
        self.lbl_due.pack(side="left", padx=20)
        
        # Button to finalize the transaction
        ctk.CTkButton(row3, text="Generate Invoice", command=self.generate_invoice, fg_color="#10b981", hover_color="#059669", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=10)
        # Button to wipe the cart empty
        ctk.CTkButton(row3, text="Clear", command=self.clear_cart, fg_color="transparent", border_width=1, text_color="#ef4444").pack(side="right", padx=10)
        
        # Pre-fill the Customer and Product dropdowns with data from the database
        self.load_dropdowns()

    # Purpose:
    # Populates the dropdown menus by querying the latest customers and products.
    # ---------------------------------------------
    # Team Member 4
    # Function: load_dropdowns
    # Purpose:
    # Fetches database records to populate the UI dropdown menus.
    # ---------------------------------------------
    def load_dropdowns(self):
        """
        Fetches database records to populate the UI dropdown menus.
        """
        try:
            # Query all customers and products
            customers = self.db.get_all("customers")
            products = self.db.get_all("products")
            # Store complete customer and product lists for searching
            self.all_customers = customers
            self.all_products = products
            
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

# ---------------------------------------------
# Team Member 4
# Function: filter_products
# Purpose:
# Dynamically filters the product dropdown based on
# the text entered in the search box.
# ---------------------------------------------

    def filter_products(self, *args):
        """Filters products as the user types."""

        search = self.search_var.get().lower().strip()

        filtered = []

        for product in self.all_products:

            product_text = f"{product['id']} - {product['name']}"

            if (
                search in product['name'].lower()
                or search in str(product['id'])
            ):
                filtered.append(product_text)

        if filtered:
            self.product_dropdown.configure(values=filtered)

            current = self.product_var.get()

            if current not in filtered:
                self.product_var.set(filtered[0])

        else:
            self.product_dropdown.configure(values=["No Product Found"])
            self.product_var.set("No Product Found")


# ---------------------------------------------
# Team Member 4
# Function: filter_customers
# Purpose:
# Dynamically filters the customer dropdown
# based on the text entered in the search box.
# ---------------------------------------------
    def filter_customers(self, *args):
        """
        Dynamically filters the customer dropdown
        according to the user's search input.
        """

        # Get the search text entered by the user
        search = self.customer_search_var.get().lower().strip()

        # Store matching customers
        filtered = []

        # Loop through all customers
        for customer in self.all_customers:

            customer_text = f"{customer['id']} - {customer['name']}"

            # Search by Customer ID or Customer Name
            if (
                search in customer["name"].lower()
                or search in str(customer["id"])
            ):
                filtered.append(customer_text)

        # Update the dropdown
        if filtered:

            self.customer_dropdown.configure(values=filtered)

            current = self.customer_var.get()

            if current not in filtered:
                self.customer_var.set(filtered[0])

        else:

            self.customer_dropdown.configure(values=["No Customer Found"])
            self.customer_var.set("No Customer Found")



    # Purpose:
    # Reads the currently selected product, applies quantity and discount, 
    # calculates item-level taxes, and adds it to the cart matrix.
    # ---------------------------------------------
    # Team Member 4
    # Function: add_to_cart
    # Purpose:
    # Calculates prices and adds the selected product to the shopping cart.
    # ---------------------------------------------
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
    # ---------------------------------------------
    # Team Member 4
    # Function: update_totals
    # Purpose:
    # Updates the footer UI labels with recalculated totals from all cart items.
    # ---------------------------------------------
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
        self.amount_paid_var.set(f"{self.final_amount:.2f}")
        self.update_payment_status()


    # ---------------------------------------------
    # Team Member 4
    # Function: update_payment_status
    # Purpose:
    # Calculates the paid amount, due amount,
    # or change amount whenever the user enters
    # a payment value.
    # ---------------------------------------------
    def update_payment_status(self, *args):
        """
        Updates the Paid and Due labels dynamically.
        """

        try:
            amount_paid = float(self.amount_paid_var.get())
        except ValueError:
            amount_paid = 0.0

        # Update Paid label
        self.lbl_paid.configure(text=f"Paid: ₹{amount_paid:.2f}")

        difference = amount_paid - self.final_amount

        if difference >= 0:
            # Customer has paid enough
            self.lbl_due.configure(
                text=f"Change: ₹{difference:.2f}",
                text_color="#16a34a"
            )
        else:
            # Customer still owes money
            self.lbl_due.configure(
                text=f"Due: ₹{-difference:.2f}",
                text_color="#dc2626"
            )

    # Purpose:
    # Empties the shopping basket and resets all totals to zero.
    # ---------------------------------------------
    # Team Member 4
    # Function: clear_cart
    # Purpose:
    # Wipes the cart data and clears the Treeview visually.
    # ---------------------------------------------
    def clear_cart(self):
        """
        Wipes the cart data and clears the Treeview visually.
        """
        # Empty internal memory array
        self.cart_items = []
        self.selected_cart_index = None
        
        # Empty visual rows
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
            
        # Re-trigger total math (which will now sum up to zero)
        self.update_totals()


    #Purpose:
    # Removes the currently selected item from the cart and updates totals.
    # ---------------------------------------------
    # Team Member 4
    # Function: remove_selected_item
    # Purpose:
    # Removes the selected product from the cart and updates the UI and totals.
    # ---------------------------------------------

    def remove_selected_item(self):
        """Removes the selected row from the shopping cart."""

    # Get selected row
        selected_item = self.cart_tree.selection()

        if not selected_item:
         messagebox.showwarning(
            "No Selection",
            "Please select a product to remove."
        )
         return

    # Get Treeview item ID
        item = selected_item[0]

    # Get index of selected row
        row_index = self.cart_tree.index(item)

    # Remove from cart_items list
        if 0 <= row_index < len(self.cart_items):
            self.cart_items.pop(row_index)

    # Remove from Treeview
        self.cart_tree.delete(item)

    # Update totals
        self.update_totals()
        # Purpose:
# Detects when the user selects a product from the shopping cart.
# It loads the selected item's details into the Product, Quantity,
# and Discount fields so the item can be edited.
# ---------------------------------------------
# Team Member 4
# Function: on_cart_select
# Purpose:
# Handles Treeview row selection and populates the input fields
# with the selected cart item's information for updating.
# ---------------------------------------------

    def on_cart_select(self, event):

        selected = self.cart_tree.selection()

        if not selected:
            return

        item = selected[0]

        self.selected_cart_index = self.cart_tree.index(item)

        values = self.cart_tree.item(item)["values"]

        product_id = values[0]
        quantity = values[2]

        # Set quantity
        self.qty_var.set(str(quantity))

    # Set discount
        discount = self.cart_items[self.selected_cart_index]["discount"]
        price = self.cart_items[self.selected_cart_index]["price"]

        if price > 0:
            discount_percent = (discount / (price * quantity)) * 100
        else:
                discount_percent = 0

        self.discount_var.set(f"{discount_percent:.0f}")

    # Select product in dropdown
        for value in self.product_dropdown.cget("values"):
         if value.startswith(f"{product_id} -"):
            self.product_var.set(value)
            break
    

    # Purpose:
    # Finalizes the checkout. It generates a QR code, saves data to SQLite, prints the PDF, and clears the cart.
    # ---------------------------------------------
    # Team Member 4
    # Function: generate_invoice
    # Purpose:
    # Finalizes the transaction, writes to the database, and creates the PDF.
    # ---------------------------------------------
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
        
        try:
            amount_paid = float(self.amount_paid_var.get())
        except ValueError:
            amount_paid = self.final_amount

        status = "Paid"
        if amount_paid < self.final_amount:
            status = "Partial"
            
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
            "status": status,
            "amount_paid": amount_paid, 
            "notes": "",
            # Check who is logged in via the master controller. Fallback to ID 1 if None.
            "created_by": self.controller.current_user['id'] if self.controller.current_user else 1,
            "qr_hash": qr_hash
        }
        
        try:
            # Phase 1: Save the invoice and its items to the SQLite Database (deducts stock internally)
            self.billing.generate_invoice(invoice_data, self.cart_items)
            
            # Phase 2: Paint the PDF Document and save it to disk
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=f"{inv_number}.pdf",
                title="Save Invoice PDF",
                filetypes=[("PDF Files", "*.pdf")]
            )
            
            if save_path:
                pdf_path = self.report_service.generate_invoice_pdf(invoice_data, self.cart_items, qr_path, save_path)
                # Phase 3: Notify cashier of success
                messagebox.showinfo("Success", f"Invoice {inv_number} generated successfully!\nSaved to: {save_path}")
                
                # Open PDF automatically
                if os.name == 'nt':
                    os.startfile(save_path)
                else:
                    import subprocess
                    subprocess.call(['open', save_path])
            else:
                pdf_path = self.report_service.generate_invoice_pdf(invoice_data, self.cart_items, qr_path)
                messagebox.showinfo("Success", f"Invoice {inv_number} generated successfully!")
            
            # Phase 4: Prepare the UI for the next customer
            self.clear_cart()
            self.load_dropdowns()
            
        except Exception as e:
            # If the database fails (e.g. locked file), show the error so the app doesn't crash silently
            messagebox.showerror("Error", str(e))
