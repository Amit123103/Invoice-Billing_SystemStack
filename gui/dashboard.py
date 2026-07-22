############################################################
# Project : Smart ERP Billing System
#
# File    : dashboard.py
#
# Team Member :
# Team Member 1
#
# Module :
# Authentication & Dashboard
#
# Responsibilities :
# - Login Authentication
# - Dashboard
# - User Management
# - Settings
#
# Developed By :
# Team Member 1
############################################################
"""
File: dashboard.py

Purpose:
Provides the primary navigation interface and high-level KPIs for the system.

Dependencies:
- customtkinter
- random (Used temporarily for mock chart generation)

"""

###########################################################
# Team Member 1
# Module: Authentication & Dashboard
# Completed:
# - Login Authentication
# - Dashboard
# - User Management
# - Settings
###########################################################
import customtkinter as ctk
from database.queries import DatabaseQueries
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta

# This class defines the main Dashboard frame that wraps around all other pages.
# It solves the problem of navigation by providing a persistent left-side menu and top header.
# Its responsibility is to act as the master layout and show summary analytics on the home screen.
# ---------------------------------------------
# Team Member 1
# Class: Dashboard
# Purpose:
# GUI Frame for the Main Dashboard and persistent Navigation Menu.
# ---------------------------------------------
class Dashboard(ctk.CTkFrame):
    """
    GUI Frame for the Main Dashboard and persistent Navigation Menu.
    """
    
    # ---------------------------------------------
    # Team Member 1
    # Function: __init__
    # Purpose:
    # Handles logic for   init  
    # ---------------------------------------------
    def __init__(self, parent, controller):
        # Set the entire background to a modern light gray
        super().__init__(parent, fg_color="#F3F4F6")
        self.controller = controller
        self.db = DatabaseQueries()
        
        # ---------------------------------------------------------
        # Persistent Left Sidebar Navigation
        # ---------------------------------------------------------
        # Create a white sidebar that sticks to the left
        self.sidebar = ctk.CTkFrame(self, fg_color="#FFFFFF", width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        # Create a transparent container on the right where the actual pages will be loaded
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True)
        
        # Draw the application branding in the sidebar
        logo_label = ctk.CTkLabel(self.sidebar, text="Smart ERP", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1d4ed8")
        logo_label.pack(pady=(30, 40), padx=20)
        
        self.buttons = []
        
        # Define the navigation menu items and the commands they trigger
        nav_items = [
            ("Dashboard", self.show_home),
            ("Customers", lambda: self.controller.show_frame("CustomerPage")),
            ("Products", lambda: self.controller.show_frame("InventoryPage")),
            ("Invoices", lambda: self.controller.show_frame("InvoicePage")),
            ("Reports", lambda: self.controller.show_frame("ReportsPage")),
            ("Settings", lambda: self.controller.show_frame("SettingsPage")),
        ]
        
        # Loop over the list and dynamically generate the buttons
        for text, cmd in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                command=cmd, 
                fg_color="transparent", 
                text_color="#4b5563",
                hover_color="#eff6ff",
                anchor="w",
                font=ctk.CTkFont(size=14),
                height=40
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.buttons.append(btn)
            
        # Create a distinct, red logout button anchored to the bottom of the sidebar
        logout_btn = ctk.CTkButton(
            self.sidebar, 
            text="Logout", 
            command=self.logout, 
            fg_color="transparent", 
            text_color="#ef4444",
            hover_color="#fef2f2",
            anchor="w",
            font=ctk.CTkFont(size=14),
            height=40
        )
        logout_btn.pack(side="bottom", fill="x", padx=10, pady=20)
            
        # ---------------------------------------------------------
        # Dashboard Home Page Content
        # ---------------------------------------------------------
        self.home_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        
        # Build the top header with a search bar and a quick-action button
        header = ctk.CTkFrame(self.home_frame, fg_color="transparent", height=60)
        header.pack(fill="x", padx=20, pady=10)
        
        search_entry = ctk.CTkEntry(header, placeholder_text="Search invoices, customers, or reports...", width=400, height=40, corner_radius=20, fg_color="#FFFFFF", border_width=0)
        search_entry.pack(side="left", padx=10)
        
        new_inv_btn = ctk.CTkButton(header, text="+ New Invoice", command=lambda: self.controller.show_frame("InvoicePage"), height=40, corner_radius=8, font=ctk.CTkFont(weight="bold"))
        new_inv_btn.pack(side="right", padx=10)
        
        # KPI Cards (Key Performance Indicators) Container
        kpi_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=20, pady=10)
        
        self.sales_var = ctk.StringVar(value="0")
        self.revenue_var = ctk.StringVar(value="₹0.00")
        self.customers_var = ctk.StringVar(value="0")
        self.products_var = ctk.StringVar(value="0")
        
        # Render 4 summary cards showing business health metrics
        self.create_kpi_card(kpi_frame, "Total Sales", self.sales_var, "+12.5%").pack(side="left", fill="both", expand=True, padx=10)
        self.create_kpi_card(kpi_frame, "Total Revenue", self.revenue_var, "+8.2%").pack(side="left", fill="both", expand=True, padx=10)
        self.create_kpi_card(kpi_frame, "Total Customers", self.customers_var, "+24").pack(side="left", fill="both", expand=True, padx=10)
        self.create_kpi_card(kpi_frame, "Total Products", self.products_var, "Active").pack(side="left", fill="both", expand=True, padx=10)
        
        # Build a placeholder for a large visual analytics chart
        self.chart_frame = ctk.CTkFrame(self.home_frame, fg_color="#FFFFFF", corner_radius=12)
        self.chart_frame.pack(fill="both", expand=True, padx=30, pady=20)
        ctk.CTkLabel(self.chart_frame, text="Recent Revenue Analytics", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111827").pack(anchor="nw", padx=20, pady=10)
        
        self.chart_canvas_wrapper = ctk.CTkFrame(self.chart_frame, fg_color="transparent")
        self.chart_canvas_wrapper.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.canvas_widget = None

        # Set the home screen as the default view
        self.show_home()

    # Purpose:
    # A reusable helper function to generate a styled KPI (Key Performance Indicator) card.
    #
    # Parameters:
    # parent (CTkFrame): The widget this card will be placed inside.
    # title (str): The label of the metric (e.g., "Total Revenue").
    # variable (ctk.StringVar): The variable holding the primary large number string.
    # badge (str): A small green indicator text (e.g., "+10%").
    #
    # Returns:
    # CTkFrame: The fully built card widget ready to be packed/gridded.
    # ---------------------------------------------
    # Team Member 1
    # Function: create_kpi_card
    # Purpose:
    # Creates a modern KPI metric card.
    # ---------------------------------------------
    def create_kpi_card(self, parent, title, variable, badge):
        """
        Creates a modern KPI metric card.
        """
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=12, height=120)
        
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=15, pady=(15, 5))
        
        icon = ctk.CTkLabel(top_row, text="📈", font=ctk.CTkFont(size=20))
        icon.pack(side="left")
        
        badge_lbl = ctk.CTkLabel(top_row, text=badge, text_color="#10b981", font=ctk.CTkFont(size=12, weight="bold"))
        badge_lbl.pack(side="right")
        
        title_lbl = ctk.CTkLabel(card, text=title, text_color="#6b7280", font=ctk.CTkFont(size=13))
        title_lbl.pack(anchor="w", padx=15)
        
        val_lbl = ctk.CTkLabel(card, textvariable=variable, text_color="#111827", font=ctk.CTkFont(size=24, weight="bold"))
        val_lbl.pack(anchor="w", padx=15, pady=(0, 15))
        
        return card

    # ---------------------------------------------
    # Team Member 1
    # Function: load_dashboard_data
    # Purpose:
    # Handles logic for load dashboard data
    # ---------------------------------------------
    def load_dashboard_data(self):
        invoices = [dict(row) for row in self.db.get_all("invoices")]
        customers = self.db.get_all("customers")
        products = self.db.get_all("products")

        total_sales = len(invoices)
        total_revenue = sum(inv.get('total_amount', 0) for inv in invoices if inv.get('status') in ('Paid', 'Pending', 'Partial'))
        
        self.sales_var.set(str(total_sales))
        self.revenue_var.set(f"₹{total_revenue:,.2f}")
        self.customers_var.set(str(len(customers)))
        self.products_var.set(str(len(products)))

        # Update Chart
        self.update_chart(invoices)

    # ---------------------------------------------
    # Team Member 1
    # Function: update_chart
    # Purpose:
    # Handles logic for update chart
    # ---------------------------------------------
    def update_chart(self, invoices):
        if self.canvas_widget:
            self.canvas_widget.destroy()

        # Group invoices by date for the last 7 days
        daily_revenue = {}
        for i in range(7):
            date_str = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            daily_revenue[date_str] = 0

        for inv in invoices:
            created_at = inv.get('created_at', '')
            if created_at and inv.get('status') in ('Paid', 'Pending', 'Partial'):
                date_str = str(created_at).split(" ")[0]
                if date_str in daily_revenue:
                    daily_revenue[date_str] += inv.get('total_amount', 0)

        dates = list(reversed(list(daily_revenue.keys())))
        revenues = list(reversed(list(daily_revenue.values())))
        # Use short format for x-axis (e.g. "Jul 21")
        short_dates = [datetime.strptime(d, '%Y-%m-%d').strftime('%b %d') for d in dates]

        # Create Matplotlib Figure
        fig = Figure(figsize=(6, 3), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.plot(short_dates, revenues, color="#2563eb", marker="o", linewidth=2)
        ax.fill_between(short_dates, revenues, alpha=0.1, color="#2563eb")
        ax.set_ylabel("Revenue (₹)")
        
        # Styling the plot to match the modern dashboard
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#d1d5db')
        ax.spines['bottom'].set_color('#d1d5db')
        ax.tick_params(colors='#4b5563')
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        fig.tight_layout()

        # Embed into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas_wrapper)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    # Purpose:
    # Swaps the content area back to the home analytics view.
    # ---------------------------------------------
    # Team Member 1
    # Function: show_home
    # Purpose:
    # Displays the main dashboard analytics view.
    # ---------------------------------------------
    def show_home(self):
        """
        Displays the main dashboard analytics view.
        """
        self.load_dashboard_data()
        
        # Hide any currently visible inner page (like CustomerPage or InventoryPage)
        for widget in self.content.winfo_children():
            widget.pack_forget()
            
        # Re-pack the home frame
        self.home_frame.pack(fill="both", expand=True)

    # Purpose:
    # Clears the active session and returns the user to the login screen.
    # ---------------------------------------------
    # Team Member 1
    # Function: logout
    # Purpose:
    # Logs the user out of the application.
    # ---------------------------------------------
    def logout(self):
        """
        Logs the user out of the application.
        """
        # Wipe the currently logged-in user from memory
        self.controller.current_user = None
        
        # Navigate back to the login screen
        self.controller.show_frame("LoginPage")





