import customtkinter as ctk
from tkinter import messagebox
from database.queries import DatabaseQueries
from utils.auth import verify_password

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F3F4F6")
        self.controller = controller
        self.db = DatabaseQueries()

        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15, width=400, height=500)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="Smart ERP", font=ctk.CTkFont(size=28, weight="bold"), text_color="#1d4ed8").pack(pady=(40, 10))
        ctk.CTkLabel(card, text="Please login to your account", font=ctk.CTkFont(size=14), text_color="#6b7280").pack(pady=(0, 40))

        self.username_entry = ctk.CTkEntry(card, placeholder_text="Username", width=300, height=45, corner_radius=8, border_width=1)
        self.username_entry.pack(pady=(0, 20))

        self.password_entry = ctk.CTkEntry(card, placeholder_text="Password", show="*", width=300, height=45, corner_radius=8, border_width=1)
        self.password_entry.pack(pady=(0, 30))

        login_btn = ctk.CTkButton(card, text="Login", command=self.login, width=300, height=45, corner_radius=8, font=ctk.CTkFont(weight="bold"))
        login_btn.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.db.get_user_by_username(username)
        if user and verify_password(password, user['password_hash']):
            self.controller.current_user = user
            self.controller.show_frame("Dashboard")
        else:
            messagebox.showerror("Error", "Invalid username or password")
