"""
File: settings_page.py

Purpose:
A placeholder UI screen for future Application Configuration features (like Company Profile, Tax Rates).

Dependencies:
- customtkinter

Project: Smart ERP Billing System
"""

import customtkinter as ctk

# This class provides the scaffold for the Settings page.
# It exists so the navigation sidebar has a valid target when the user clicks 'Settings'.
class SettingsPage(ctk.CTkFrame):
    """
    GUI Frame for System Settings (Placeholder).
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Simple placeholder label
        ctk.CTkLabel(self, text="Settings Page (Coming Soon)", font=ctk.CTkFont(size=24)).pack(pady=50)
