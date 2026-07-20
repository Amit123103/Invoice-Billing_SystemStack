import customtkinter as ctk
import tkinter as tk
from gui.login_page import LoginPage
from gui.dashboard import Dashboard
from gui.customer_page import CustomerPage
from gui.inventory_page import InventoryPage
from gui.invoice_page import InvoicePage
from gui.reports_page import ReportsPage
from gui.settings_page import SettingsPage

ctk.set_appearance_mode("Light")  # Light mode as per screenshot
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class SmartERPApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart ERP Billing System")
        self.geometry("1200x800")
        self.minsize(1024, 768)
        
        self.current_user = None

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, Dashboard, CustomerPage, InventoryPage, InvoicePage, ReportsPage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        if page_name != "LoginPage" and not self.current_user:
            page_name = "LoginPage"
            
        frame = self.frames[page_name]
        
        if page_name in ["CustomerPage", "InventoryPage", "InvoicePage", "ReportsPage", "SettingsPage"]:
            dashboard = self.frames["Dashboard"]
            for widget in dashboard.content.winfo_children():
                widget.pack_forget()
            frame.pack(in_=dashboard.content, fill="both", expand=True)
            self.frames["Dashboard"].tkraise()
        else:
            frame.tkraise()

        if hasattr(frame, 'load_dropdowns'):
            frame.load_dropdowns()
        if hasattr(frame, 'load_customers'):
            frame.load_customers()
        if hasattr(frame, 'load_products'):
            frame.load_products()
        if hasattr(frame, 'load_settings'):
            frame.load_settings()

if __name__ == "__main__":
    app = SmartERPApp()
    app.mainloop()
