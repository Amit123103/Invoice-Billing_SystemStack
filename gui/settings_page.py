############################################################
# Project : Smart ERP Billing System
#
# File    : settings_page.py
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
File: settings_page.py

Purpose:
A UI screen for Application Configuration features (like Company Profile, Tax Rates).

Dependencies:
- customtkinter
- tkinter.messagebox
- tkinter.filedialog

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
from tkinter import messagebox, filedialog
from database.queries import DatabaseQueries
import shutil

# ---------------------------------------------
# Team Member 1
# Class: SettingsPage
# Purpose:
# GUI Frame for System Settings.
# ---------------------------------------------
class SettingsPage(ctk.CTkFrame):
    """
    GUI Frame for System Settings.
    """
    
    # ---------------------------------------------
    # Team Member 1
    # Function: __init__
    # Purpose:
    # Handles logic for   init  
    # ---------------------------------------------
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.db = DatabaseQueries()
        
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="Company Settings", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111827").pack(side="left")
        
        # Form Card
        form_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        form_card.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Grid config for form layout
        form_card.grid_columnconfigure(0, weight=1)
        form_card.grid_columnconfigure(1, weight=1)
        
        # Form Variables
        self.name_var = ctk.StringVar()
        self.gst_var = ctk.StringVar()
        self.phone_var = ctk.StringVar()
        self.email_var = ctk.StringVar()
        self.address_var = ctk.StringVar()
        self.logo_var = ctk.StringVar()
        
        # Create form fields
        self.create_input(form_card, "Company Name", self.name_var, 0, 0)
        self.create_input(form_card, "GST Number", self.gst_var, 0, 1)
        self.create_input(form_card, "Phone Number", self.phone_var, 1, 0)
        self.create_input(form_card, "Email Address", self.email_var, 1, 1)
        self.create_input(form_card, "Address", self.address_var, 2, 0, colspan=2, width=600)
        
        # Logo Picker Row
        logo_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        logo_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=15, sticky="w")
        
        ctk.CTkLabel(logo_frame, text="Logo Path", text_color="#4b5563", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
        ctk.CTkEntry(logo_frame, textvariable=self.logo_var, width=400, height=35).pack(side="left", padx=(0, 10))
        ctk.CTkButton(logo_frame, text="Browse", command=self.browse_logo, width=100, height=35, fg_color="#6b7280", hover_color="#4b5563").pack(side="left")
        
        # Save Button
        save_btn = ctk.CTkButton(form_card, text="Save Settings", command=self.save_settings, font=ctk.CTkFont(weight="bold"), fg_color="#059669", hover_color="#047857", height=45, width=200)
        save_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Advanced Settings Section
        adv_header = ctk.CTkFrame(self, fg_color="transparent")
        adv_header.pack(fill="x", padx=30, pady=(10, 5))
        ctk.CTkLabel(adv_header, text="Advanced Settings", font=ctk.CTkFont(size=20, weight="bold"), text_color="#111827").pack(side="left")
        
        adv_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12)
        adv_card.pack(fill="x", padx=30, pady=5)
        
        # Theme Toggle
        theme_frame = ctk.CTkFrame(adv_card, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=15)
        ctk.CTkLabel(theme_frame, text="Application Theme", text_color="#4b5563", font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        theme_menu = ctk.CTkOptionMenu(theme_frame, values=["Light", "Dark"], variable=self.theme_var, command=self.change_theme)
        theme_menu.pack(side="right")
        
        # Backup Database
        backup_frame = ctk.CTkFrame(adv_card, fg_color="transparent")
        backup_frame.pack(fill="x", padx=20, pady=(0, 15))
        ctk.CTkLabel(backup_frame, text="Data Management", text_color="#4b5563", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkButton(backup_frame, text="Backup Database", command=self.backup_database, fg_color="#2563eb", hover_color="#1d4ed8").pack(side="right")
        
        # Bind mapping event to dynamically load data when shown
        self.bind("<Map>", lambda e: self.load_settings())
        self.load_settings()

    # ---------------------------------------------
    # Team Member 1
    # Function: create_input
    # Purpose:
    # Helper to create consistent input fields.
    # ---------------------------------------------
    def create_input(self, parent, label, variable, row, col, colspan=1, width=280):
        """Helper to create consistent input fields."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, columnspan=colspan, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(frame, text=label, text_color="#4b5563", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        ctk.CTkEntry(frame, textvariable=variable, width=width, height=35, fg_color="#f9fafb", text_color="#111827", border_color="#d1d5db").pack(anchor="w", pady=(5,0))

    # ---------------------------------------------
    # Team Member 1
    # Function: browse_logo
    # Purpose:
    # Opens a file dialog to select a logo image.
    # ---------------------------------------------
    def browse_logo(self):
        """Opens a file dialog to select a logo image."""
        filename = filedialog.askopenfilename(title="Select Logo", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if filename:
            self.logo_var.set(filename)

    # ---------------------------------------------
    # Team Member 1
    # Function: load_settings
    # Purpose:
    # Fetches the company data from the database and updates the UI.
    # ---------------------------------------------
    def load_settings(self):
        """Fetches the company data from the database and updates the UI."""
        company = self.db.get_company()
        if company:
            company_dict = dict(company)
            self.name_var.set(company_dict.get('name', ''))
            self.gst_var.set(company_dict.get('gst_number', ''))
            self.phone_var.set(company_dict.get('phone', ''))
            self.email_var.set(company_dict.get('email', ''))
            self.address_var.set(company_dict.get('address', ''))
            self.logo_var.set(company_dict.get('logo_path', ''))

    # ---------------------------------------------
    # Team Member 1
    # Function: save_settings
    # Purpose:
    # Saves the form data to the database.
    # ---------------------------------------------
    def save_settings(self):
        """Saves the form data to the database."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Company Name is required.")
            return
            
        self.db.save_company(
            name=name,
            gst_number=self.gst_var.get().strip(),
            address=self.address_var.get().strip(),
            phone=self.phone_var.get().strip(),
            email=self.email_var.get().strip(),
            logo_path=self.logo_var.get().strip()
        )
        
        messagebox.showinfo("Success", "Company settings saved successfully!")

    # ---------------------------------------------
    # Team Member 1
    # Function: change_theme
    # Purpose:
    # Switches between Light and Dark mode.
    # ---------------------------------------------
    def change_theme(self, choice):
        """Switches between Light and Dark mode."""
        ctk.set_appearance_mode(choice)
        
    # ---------------------------------------------
    # Team Member 1
    # Function: backup_database
    # Purpose:
    # Creates a backup copy of the database.
    # ---------------------------------------------
    def backup_database(self):
        """Creates a backup copy of the database."""
        save_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            initialfile="smart_erp_backup.db",
            title="Save Database Backup",
            filetypes=[("SQLite Database", "*.db")]
        )
        if save_path:
            try:
                shutil.copy2("smart_erp.db", save_path)
                messagebox.showinfo("Success", f"Database backed up successfully to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to backup database: {str(e)}")







