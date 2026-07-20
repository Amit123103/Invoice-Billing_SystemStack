import os
gui_dir = 'c:/Users/amita/myprojects/invoice_billing/gui'
os.makedirs(gui_dir, exist_ok=True)

gui_files = {
    "__init__.py": "",
    "login_page.py": '''import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import DatabaseQueries
from utils.auth import verify_password

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = DatabaseQueries()

        # Simple styling
        self.config(bg="#f0f2f5")
        
        frame = tk.Frame(self, bg="white", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Smart ERP Login", font=("Helvetica", 24, "bold"), bg="white").pack(pady=(0, 20))

        tk.Label(frame, text="Username", bg="white").pack(anchor="w")
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack(pady=(0, 15))

        tk.Label(frame, text="Password", bg="white").pack(anchor="w")
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.pack(pady=(0, 20))

        login_btn = ttk.Button(frame, text="Login", command=self.login)
        login_btn.pack(fill="x")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.db.get_user_by_username(username)
        if user and verify_password(password, user['password_hash']):
            self.controller.current_user = user
            self.controller.show_frame("Dashboard")
        else:
            messagebox.showerror("Error", "Invalid username or password")
''',
    "dashboard.py": '''import tkinter as tk
from tkinter import ttk

class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#ffffff")
        
        # Sidebar
        sidebar = tk.Frame(self, bg="#2c3e50", width=200)
        sidebar.pack(side="left", fill="y")


       
        
        # Main content
        self.content = tk.Frame(self, bg="#ecf0f1")
        self.content.pack(side="right", fill="both", expand=True)
        
        # Sidebar Buttons
        buttons = [
            ("Dashboard", self.show_home),
            ("Customers", lambda: self.controller.show_frame("CustomerPage")),
            ("Inventory", lambda: self.controller.show_frame("InventoryPage")),
            ("Invoices", lambda: self.controller.show_frame("InvoicePage")),
            ("Reports", lambda: self.controller.show_frame("ReportsPage")),
            ("Settings", lambda: self.controller.show_frame("SettingsPage")),
            ("Logout", self.logout)
        ]
        
        tk.Label(sidebar, text="SMART ERP", bg="#2c3e50", fg="white", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        for text, cmd in buttons:
            btn = tk.Button(sidebar, text=text, command=cmd, bg="#34495e", fg="white", bd=0, font=("Helvetica", 12), pady=10, anchor="w", padx=20)
            btn.pack(fill="x", pady=2)
            
        self.home_frame = tk.Frame(self.content, bg="#ecf0f1")
        tk.Label(self.home_frame, text="Welcome to Smart ERP", font=("Helvetica", 24), bg="#ecf0f1").pack(pady=20)
        self.show_home()

    def show_home(self):
        for widget in self.content.winfo_children():
            widget.pack_forget()
        self.home_frame.pack(fill="both", expand=True)

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage")
''',
    "customer_page.py": '''import tkinter as tk
from tkinter import ttk

class CustomerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Customer Management", font=("Helvetica", 18)).pack(pady=10)
        
        # Placeholder for treeview and form
        tk.Label(self, text="(Customer list and add form will go here)").pack(pady=50)
''',
    "inventory_page.py": '''import tkinter as tk

class InventoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Inventory Management", font=("Helvetica", 18)).pack(pady=10)
''',
    "invoice_page.py": '''import tkinter as tk

class InvoicePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Invoice Generation", font=("Helvetica", 18)).pack(pady=10)
''',
    "reports_page.py": '''import tkinter as tk

class ReportsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Reports", font=("Helvetica", 18)).pack(pady=10)
''',
    "settings_page.py": '''import tkinter as tk

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Settings & Company Info", font=("Helvetica", 18)).pack(pady=10)
'''
}

for name, content in gui_files.items():
    with open(os.path.join(gui_dir, name), 'w') as f:
        f.write(content)
