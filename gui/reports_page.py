"""
File: reports_page.py

Purpose:
A placeholder UI screen for future Analytical Reporting features.

Dependencies:
- customtkinter

Project: Smart ERP Billing System
"""

import customtkinter as ctk

# This class provides the scaffold for the Reports page.
# It exists so the navigation sidebar has a valid target when the user clicks 'Reports'.
class ReportsPage(ctk.CTkFrame):
    """
    GUI Frame for Business Reports (Placeholder).
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Simple placeholder label
        ctk.CTkLabel(self, text="Reports Page (Coming Soon)", font=ctk.CTkFont(size=24)).pack(pady=50)
