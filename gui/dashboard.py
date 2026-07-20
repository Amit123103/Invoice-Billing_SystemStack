import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F3F4F6") # Light gray background like modern web
        self.controller = controller
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color="#FFFFFF", width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        # Main content
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="right", fill="both", expand=True)
        
        # Sidebar Logo area
        logo_label = ctk.CTkLabel(self.sidebar, text="Smart ERP", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1d4ed8")
        logo_label.pack(pady=(30, 40), padx=20)
        
        # Sidebar Navigation Buttons
        self.buttons = []
        nav_items = [
            ("Dashboard", self.show_home),
            ("Customers", lambda: self.controller.show_frame("CustomerPage")),
            ("Products", lambda: self.controller.show_frame("InventoryPage")),
            ("Invoices", lambda: self.controller.show_frame("InvoicePage")),
            ("Reports", lambda: self.controller.show_frame("ReportsPage")),
            ("Settings", lambda: self.controller.show_frame("SettingsPage")),
        ]
        
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
            
        # Logout at bottom
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
            
        self.home_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        
        # Top Header (Search, Company, Avatar)
        header = ctk.CTkFrame(self.home_frame, fg_color="transparent", height=60)
        header.pack(fill="x", padx=20, pady=10)
        
        search_entry = ctk.CTkEntry(header, placeholder_text="Search invoices, customers, or reports...", width=400, height=40, corner_radius=20, fg_color="#FFFFFF", border_width=0)
        search_entry.pack(side="left", padx=10)
        
        new_inv_btn = ctk.CTkButton(header, text="+ New Invoice", command=lambda: self.controller.show_frame("InvoicePage"), height=40, corner_radius=8, font=ctk.CTkFont(weight="bold"))
        new_inv_btn.pack(side="right", padx=10)
        
        # KPI Cards Frame
        kpi_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=20, pady=10)
        
        self.create_kpi_card(kpi_frame, "Total Sales", "1,284", "+12.5%").pack(side="left", fill="both", expand=True, padx=10)
        self.create_kpi_card(kpi_frame, "Total Revenue", "$142,500", "+8.2%").pack(side="left", fill="both", expand=True, padx=10)
        self.create_kpi_card(kpi_frame, "Total Customers", "856", "+24").pack(side="left", fill="both", expand=True, padx=10)
        self.create_kpi_card(kpi_frame, "Total Products", "412", "Active").pack(side="left", fill="both", expand=True, padx=10)
        
        # Analytics Chart Area (Placeholder for visual aesthetic)
        chart_frame = ctk.CTkFrame(self.home_frame, fg_color="#FFFFFF", corner_radius=12)
        chart_frame.pack(fill="both", expand=True, padx=30, pady=20)
        ctk.CTkLabel(chart_frame, text="Monthly Sales Analytics (Visual Placeholder)", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111827").pack(anchor="nw", padx=20, pady=20)
        
        # Placeholder Bars to simulate chart
        bars_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        bars_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        for _ in range(12):
            import random
            h = random.randint(50, 200)
            bar = ctk.CTkFrame(bars_frame, fg_color="#bfdbfe", width=40, height=h, corner_radius=6)
            bar.pack(side="left", padx=10, side="bottom")

        self.show_home()

    def create_kpi_card(self, parent, title, value, badge):
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

    def show_home(self):
        for widget in self.content.winfo_children():
            widget.pack_forget()
        self.home_frame.pack(fill="both", expand=True)

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage")
