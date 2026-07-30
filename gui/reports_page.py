############################################################
# Project : Smart ERP Billing System
#
# File    : reports_page.py
#
# Team Member :Bhipender Singh
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
File: reports_page.py

Purpose:
A UI screen for Analytical Reporting features.

Dependencies:
- customtkinter
- tkinter.ttk

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
from tkinter import ttk, filedialog, messagebox
import os
from database.queries import DatabaseQueries
from services.report_service import ReportService
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import calendar


# Invoice Status Constants
STATUS_PAID = "Paid"
STATUS_PENDING = "Pending"
STATUS_PARTIAL = "Partial"
STATUS_UNKNOWN = "Unknown"

# ---------------------------------------------
# Team Member 4
# Class: ReportsPage
# Purpose:
# GUI Frame for Business Reports.
# ---------------------------------------------
class ReportsPage(ctk.CTkFrame):
    """
    GUI Frame for Business Reports.
    """
    
    # ---------------------------------------------
    # Team Member 4
    # Function: __init__
    # Purpose:
    # Handles logic for   init  
    # ---------------------------------------------
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True
        )
        self.controller = controller
        self.db = DatabaseQueries()
        self.report_service = ReportService()
        
        # Data storage for PDF generation
        self.last_metrics = {}
        self.last_invoices_data = []
        
        # Header Section
        header = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Business Reports", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")



        self.search_var = ctk.StringVar()
        
        # Refresh and Download Buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="Preview PDF", command=self.preview_pdf_report, fg_color="#8b5cf6", hover_color="#7c3aed").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Download PDF Report", command=self.generate_pdf_report, fg_color="#10b981", hover_color="#059669").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Refresh Data", command=self.load_data, fg_color="#2563eb", hover_color="#1d4ed8").pack(side="left")
        
        # Summary Cards Container
        cards_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
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
        table_card = ctk.CTkFrame(self.scroll_frame, fg_color="#FFFFFF", corner_radius=12)
        table_card.pack(fill="both", expand=True, padx=30, pady=10)
        
        top_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15,10))

        ctk.CTkLabel(
            top_frame,
            text="Recent Transactions",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#111827"
        ).pack(side="left")

        search_entry = ctk.CTkEntry(
            top_frame,
            width=320,
            placeholder_text="Search Invoice or Customer...",
            textvariable=self.search_var
        )

        search_entry.pack(side="right", padx=(10,0))

        self.filter_var = ctk.StringVar(value="All")

        filter_menu = ctk.CTkOptionMenu(
            top_frame,
            values=["All", "Paid", "Pending", "Partial"],
            variable=self.filter_var,
            width=120,
            command=lambda _: self.search_table()
        )

        filter_menu.pack(side="right", padx=(0,10))

        self.search_var.trace_add("write", self.search_table)

               
               
        columns = ("Date", "Invoice #", "Customer", "Amount", "Status")
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#FFFFFF", foreground="#111827", rowheight=40, fieldbackground="#FFFFFF", borderwidth=0)
        style.map('Treeview', background=[('selected', '#eff6ff')])
        style.configure("Treeview.Heading", background="#f9fafb", foreground="#6b7280", font=('Helvetica', 10, 'bold'), borderwidth=0)

        table_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Treeview"
    ) 

        scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=self.tree.yview
)

        self.tree.configure(yscrollcommand=scrollbar.set)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="w")
            
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar.pack(side="right", fill="y")
        
        # Action Buttons for the selected row
        action_frame = ctk.CTkFrame(table_card, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(action_frame, text="Mark as Paid", command=lambda: self.update_status(STATUS_PAID), fg_color="#10b981", hover_color="#059669").pack(side="right", padx=10)
        ctk.CTkButton(action_frame, text="Mark as Pending", command=lambda: self.update_status(STATUS_PENDING), fg_color="#f59e0b", hover_color="#d97706").pack(side="right", padx=10)


        analytics_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent"
        )
        analytics_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        analytics_frame.grid_columnconfigure(0, weight=1)
        analytics_frame.grid_columnconfigure(1, weight=1)


        self.revenue_chart_frame = ctk.CTkFrame(
            analytics_frame,
            fg_color="white",
            corner_radius=12
        )

        self.revenue_chart_frame.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="nsew"
        )

        self.status_chart_frame = ctk.CTkFrame(
            analytics_frame,
            fg_color="white",
            corner_radius=12
        )

        self.status_chart_frame.grid(
            row=0,
            column=1,
            padx=(10, 0),
            sticky="nsew"
        )

        ctk.CTkLabel(
            self.revenue_chart_frame,
            text="Monthly Revenue",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self.status_chart_frame,
            text="Invoice Status",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 5))


        self.revenue_canvas_frame = ctk.CTkFrame(
            self.revenue_chart_frame,
            fg_color="transparent"
        )
        self.revenue_canvas_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.status_canvas_frame = ctk.CTkFrame(
            self.status_chart_frame,
            fg_color="transparent"
        )
        self.status_canvas_frame.pack(fill="both", expand=True, padx=15, pady=15)


      
        # Bind the frame to update whenever it's raised/shown
        self.bind("<Map>", lambda e: self.load_data())
        self.load_data()
        
    # ---------------------------------------------
    # Team Member 4
    # Function: create_summary_card
    # Purpose:
    # Handles logic for create summary card
    # ---------------------------------------------
    def create_summary_card(self, parent, title, variable, col, bg_color, text_color):
        card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=12)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color=text_color).pack(pady=(20, 5))
        ctk.CTkLabel(card, textvariable=variable, font=ctk.CTkFont(size=24, weight="bold"), text_color=text_color).pack(pady=(0, 20))
        
    # ---------------------------------------------
    # Team Member 4
    # Function: load_data
    # Purpose:
    # Handles logic for load data
    # ---------------------------------------------
    def load_data(self):
        # Fetch data
        invoices = [dict(row) for row in self.db.get_all("invoices")]
        customers = [dict(row) for row in self.db.get_all("customers")]
        products = [dict(row) for row in self.db.get_all("products")]

        customer_map = {c["id"]: c["name"] for c in customers}

        self.update_summary_cards(invoices, customers, products)
        self.populate_tree(invoices, customer_map)

        self.create_revenue_chart(invoices)
        self.create_status_chart(invoices)

        # update the summary card


    def update_summary_cards(self, invoices, customers, products):
        total_revenue = sum(
    inv.get("total_amount", 0)
    for inv in invoices
    if inv.get("status") in (
        STATUS_PAID,
        STATUS_PENDING,
        STATUS_PARTIAL
    )
)
        

        total_invoices = len(invoices)
        total_customers = len(customers)
        total_products = len(products)

        self.sales_var.set(f"₹{total_revenue:,.2f}")
        self.invoices_var.set(str(total_invoices))
        self.customers_var.set(str(total_customers))
        self.products_var.set(str(total_products))

        self.last_metrics = {
            "revenue": f"₹{total_revenue:,.2f}",
            "invoices": str(total_invoices),
            "customers": str(total_customers),
            "products": str(total_products),
        }

    #fill the table and prepare the pdf data



    def populate_tree(self, invoices, customer_map):
        self.last_invoices_data = []

        # Clear Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        sorted_invoices = sorted(
            invoices,
            key=lambda x: x.get("id", 0),
            reverse=True
        )

        for inv in sorted_invoices:

            cust_name = customer_map.get(
                inv.get("customer_id"),
                STATUS_UNKNOWN
            )

            created_at = inv.get("created_at", "N/A")
            date_str = str(created_at).split(" ")[0] if created_at else "N/A"

            amount = f"₹{inv.get('total_amount', 0):,.2f}"

            self.tree.insert(
                "",
                "end",
                values=(
                    date_str,
                    inv.get("invoice_number", "N/A"),
                    cust_name,
                    amount,
                    inv.get("status", "N/A")
                )
            )

            self.last_invoices_data.append({
                "date": date_str,
                "number": inv.get("invoice_number", "N/A"),
                "customer": cust_name,
                "amount": amount,
                "status": inv.get("status", "N/A")
            })


    #search the table based on invoice number or customer name 

    def search_table(self, *args):

        search_text = self.search_var.get().lower().strip()
        selected_status = self.filter_var.get()

        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        for inv in self.last_invoices_data:

            invoice_match = (
                search_text in inv["number"].lower()
                or search_text in inv["customer"].lower()
            )

            status_match = (
                selected_status == "All"
                or inv["status"] == selected_status
            )

            if invoice_match and status_match:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        inv["date"],
                        inv["number"],
                        inv["customer"],
                        inv["amount"],
                        inv["status"]
                    )
                )


    # ---------------------------------------------
    # Team Member 4
    # Function: preview_pdf_report
    # Purpose:
    # Generates a temporary PDF and opens it for previewing.
    # ---------------------------------------------
    def preview_pdf_report(self):
        """Generates a temporary PDF and opens it for previewing."""
        if not self.last_invoices_data:
            messagebox.showwarning("Warning", "No data available to preview report.")
            return
            
        # Ensure reports directory exists
        os.makedirs("reports", exist_ok=True)
        temp_path = os.path.join(os.getcwd(), "reports", "preview_business_report.pdf")
        
        try:
            pdf_path = self.report_service.generate_business_report_pdf(self.last_metrics, self.last_invoices_data, temp_path)
            
            # Open PDF automatically for preview
            if os.name == 'nt':
                os.startfile(pdf_path)
            else:
                import subprocess
                subprocess.call(['open', pdf_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview report: {str(e)}")

    # ---------------------------------------------
    # Team Member 4
    # Function: generate_pdf_report
    # Purpose:
    # Generates and opens the business report PDF
    # ---------------------------------------------
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

    # ---------------------------------------------
    # Team Member 4
    # Function: update_status
    # Purpose:
    # Updates the status of the selected invoice in the Treeview.
    # ---------------------------------------------
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

    def create_status_chart(self, invoices):

        paid = 0
        pending = 0
        partial = 0

        for inv in invoices:
            status = inv.get("status", "")

            if status == STATUS_PAID:
                paid += 1

            elif status == STATUS_PENDING:
                pending += 1

            elif status == STATUS_PARTIAL:
                partial += 1

        # Remove old chart
        for widget in self.status_canvas_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(4, 3), dpi=100)

        ax = fig.add_subplot(111)

        ax.pie(
            [paid, pending, partial],
            labels=["Paid", "Pending", "Partial"],
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Invoice Status")

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.status_canvas_frame
        )
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_revenue_chart(self, invoices):
        # Group revenue by month
        monthly_revenue = defaultdict(float)

        for inv in invoices:
            status = inv.get("status")

            if status not in (STATUS_PAID, STATUS_PENDING, STATUS_PARTIAL):
                continue

            created_at = inv.get("created_at")

            if not created_at:
                continue

            # Example: "2026-07-30 12:45:20"
            year = str(created_at)[:4]
            month = str(created_at)[5:7]

            month_name = calendar.month_abbr[int(month)]

            monthly_revenue[f"{month_name} {year}"] += inv.get("total_amount", 0)

        # Remove old graph
        for widget in self.revenue_canvas_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6, 3.5), dpi=100)
        ax = fig.add_subplot(111)

        months = list(monthly_revenue.keys())
        revenue = list(monthly_revenue.values())

        sorted_data = sorted(monthly_revenue.items())

        months = [item[0] for item in sorted_data]
        revenue = [item[1] for item in sorted_data]

        ax.plot(
            months,
            revenue,
            marker="o",
            linewidth=3
        )

        ax.fill_between(months, revenue, alpha=0.2)

        ax.set_title("Monthly Revenue", fontsize=13, weight="bold")
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue (₹)")

        ax.grid(True, linestyle="--", alpha=0.4)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.revenue_canvas_frame
        )

        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


