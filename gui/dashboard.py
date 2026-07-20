"""
File: dashboard.py

Purpose:
Provides the primary navigation interface and high-level KPIs for the system.

Dependencies:
- customtkinter
- random (Used temporarily for mock chart generation)

Author: Amit Kumar
Project: Smart ERP Billing System
"""

import customtkinter as ctk

# This class defines the main Dashboard frame that wraps around all other pages.
# It solves the problem of navigation by providing a persistent left-side menu and top header.
# Its responsibility is to act as the master layout and show summary analytics on the home screen.
class Dashboard(ctk.CTkFrame):
    """
    GUI Frame for the Main Dashboard and persistent Navigation Menu.
    """
    
    def __init__(self, parent, controller):
        # Set the entire background to a modern light gray
        super().__init__(parent, fg_color="#F3F4F6")
        self.controller = controller
        
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
        
        # Render 4 summary cards showing business health metrics
        self.create_kpi_card(kpi_frame, "Total Sales", "1,284", "+12.5%").pack(side="left", fill="both", expand=True, padx=10)
        self.create_kpi_card(kpi_frame, "Total Revenue", "$142,500", "+8.2%").pack(side="left", fill="both", expand=True, padx=10)
        self.create_kpi_card(kpi_frame, "Total Customers", "856", "+24").pack(side="left", fill="both", expand=True, padx=10)
        self.create_kpi_card(kpi_frame, "Total Products", "412", "Active").pack(side="left", fill="both", expand=True, padx=10)
        
        # Build a placeholder for a large visual analytics chart
        chart_frame = ctk.CTkFrame(self.home_frame, fg_color="#FFFFFF", corner_radius=12)
        chart_frame.pack(fill="both", expand=True, padx=30, pady=20)
        ctk.CTkLabel(chart_frame, text="Monthly Sales Analytics (Visual Placeholder)", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111827").pack(anchor="nw", padx=20, pady=20)
        
        # Generate random vertical bars to simulate a modern bar chart UI
        bars_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        bars_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        for _ in range(12):
            import random
            h = random.randint(50, 200)
            bar = ctk.CTkFrame(bars_frame, fg_color="#bfdbfe", width=40, height=h, corner_radius=6)
            # pack(side="bottom") ensures the bars grow upwards like a real chart
            bar.pack(side="left", padx=10)

        # Set the home screen as the default view
        self.show_home()

    # Purpose:
    # A reusable helper function to generate a styled KPI (Key Performance Indicator) card.
    #
    # Parameters:
    # parent (CTkFrame): The widget this card will be placed inside.
    # title (str): The label of the metric (e.g., "Total Revenue").
    # value (str): The primary large number string.
    # badge (str): A small green indicator text (e.g., "+10%").
    #
    # Returns:
    # CTkFrame: The fully built card widget ready to be packed/gridded.
    def create_kpi_card(self, parent, title, value, badge):
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
        
        val_lbl = ctk.CTkLabel(card, text=value, text_color="#111827", font=ctk.CTkFont(size=24, weight="bold"))
        val_lbl.pack(anchor="w", padx=15, pady=(0, 15))
        
        return card

    # Purpose:
    # Swaps the content area back to the home analytics view.
    def show_home(self):
        """
        Displays the main dashboard analytics view.
        """
        # Hide any currently visible inner page (like CustomerPage or InventoryPage)
        for widget in self.content.winfo_children():
            widget.pack_forget()
            
        # Re-pack the home frame
        self.home_frame.pack(fill="both", expand=True)

    # Purpose:
    # Clears the active session and returns the user to the login screen.
    def logout(self):
        """
        Logs the user out of the application.
        """
        # Wipe the currently logged-in user from memory
        self.controller.current_user = None
        
        # Navigate back to the login screen
        self.controller.show_frame("LoginPage")
