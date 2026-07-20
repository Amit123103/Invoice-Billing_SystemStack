"""
File: reports_page.py

Purpose:
A UI screen for Analytical Reporting features.

Dependencies:
- customtkinter
- tkinter.ttk

"""

import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import os
from database.queries import DatabaseQueries
from services.report_service import ReportService

class ReportsPage(ctk.CTkFrame):
    """
    GUI Frame for Business Reports.
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.db = DatabaseQueries()
        self.report_service = ReportService()
        
        # Data storage for PDF generation
        self.last_metrics = {}
        self.last_invoices_data = []
        
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Business Reports", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")
        
        # Refresh and Download Buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="Download PDF Report", command=self.generate_pdf_report, fg_color="#10b981", hover_color="#059669").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Refresh Data", command=self.load_data, fg_color="#2563eb", hover_color="#1d4ed8").pack(side="left")
        
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
        
        # Action Buttons for the selected row
        action_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(action_frame, text="Mark as Paid", command=lambda: self.update_status("Paid"), fg_color="#10b981", hover_color="#059669").pack(side="right", padx=10)
        ctk.CTkButton(action_frame, text="Mark as Pending", command=lambda: self.update_status("Pending"), fg_color="#f59e0b", hover_color="#d97706").pack(side="right", padx=10)
        
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
        
        self.last_metrics = {
            'revenue': f"₹{total_revenue:,.2f}",
            'invoices': str(total_invoices),
            'customers': str(total_customers),
            'products': str(total_products)
        }
        self.last_invoices_data = []
        
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
            self.last_invoices_data.append({
                'date': date_str,
                'number': inv.get('invoice_number', 'N/A'),
                'customer': cust_name,
                'amount': amt_str,
                'status': inv.get('status', 'N/A')
            })

    def generate_pdf_report(self):
        """Generates and opens the business report PDF"""
        if not self.last_invoices_data:
            messagebox.showwarning("Warning", "No data available to generate report.")
            return
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile="Business_Report.pdf",
            title="Save Business Report",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if save_path:
            try:
                pdf_path = self.report_service.generate_business_report_pdf(self.last_metrics, self.last_invoices_data, save_path)
                messagebox.showinfo("Success", f"Report generated successfully!\nSaved to: {pdf_path}")
                
                # Open PDF automatically
                if os.name == 'nt':
                    os.startfile(pdf_path)
                else:
                    import subprocess
                    subprocess.call(['open', pdf_path])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def update_status(self, new_status):
        """Updates the status of the selected invoice in the Treeview."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select an invoice from the table first.")
            return
            
        # Get the invoice number from the selected row (column index 1)
        item_values = self.tree.item(selected_item[0], "values")
        if not item_values:
            return
            
        invoice_number = item_values[1]
        
        # Update database
        try:
            self.db.update_invoice_status(invoice_number, new_status)
            messagebox.showinfo("Success", f"Invoice {invoice_number} marked as {new_status}.")
            # Reload to reflect changes
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")






