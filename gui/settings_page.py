import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        ctk.CTkLabel(self, text="Settings Page (Coming Soon)", font=ctk.CTkFont(size=24)).pack(pady=50)
