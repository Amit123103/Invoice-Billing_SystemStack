"""
File: settings_page.py

Purpose:
A UI screen for Application Configuration features (like Company Profile, Tax Rates).

Dependencies:
- customtkinter
- tkinter.messagebox
- tkinter.filedialog

"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from database.queries import DatabaseQueries

class SettingsPage(ctk.CTkFrame):
    """
    GUI Frame for System Settings.
    """
    
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
        save_btn.grid(row=4, column=0, columnspan=2, pady=40)
        
        # Bind mapping event to dynamically load data when shown
        self.bind("<Map>", lambda e: self.load_settings())
        self.load_settings()

    def create_input(self, parent, label, variable, row, col, colspan=1, width=280):
        """Helper to create consistent input fields."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, columnspan=colspan, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(frame, text=label, text_color="#4b5563", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        ctk.CTkEntry(frame, textvariable=variable, width=width, height=35, fg_color="#f9fafb", text_color="#111827", border_color="#d1d5db").pack(anchor="w", pady=(5,0))

    def browse_logo(self):
        """Opens a file dialog to select a logo image."""
        filename = filedialog.askopenfilename(title="Select Logo", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if filename:
            self.logo_var.set(filename)

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
