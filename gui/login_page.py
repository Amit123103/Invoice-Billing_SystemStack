"""
File: login_page.py

Purpose:
Provides the Authentication user interface for the Smart ERP system.

Dependencies:
- customtkinter (For the modern UI widgets)
- tkinter.messagebox (For error popups)
- database.queries (To verify the user against the database)
- utils.auth (For hashing and verifying the password)

Author: Amit Kumar
Project: Smart ERP Billing System
"""

import customtkinter as ctk
from tkinter import messagebox
from database.queries import DatabaseQueries
from utils.auth import verify_password

# This class handles the graphical Login screen.
# It solves the problem of unauthorized access by forcing a user to authenticate before 
# seeing the Dashboard or performing any billing operations.
# Its responsibility is capturing credentials and switching to the main app if valid.
class LoginPage(ctk.CTkFrame):
    """
    GUI Frame for the Login Screen.
    """
    
    def __init__(self, parent, controller):
        # Initialize the base CTkFrame with a light gray background color
        super().__init__(parent, fg_color="#F3F4F6")
        
        # Save a reference to the main application controller so we can switch frames later
        self.controller = controller
        
        # Instantiate the database queries manager
        self.db = DatabaseQueries()

        # Create a centered white 'card' to hold the login form elements
        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15, width=400, height=500)
        # place() centers the card perfectly in the middle of the screen
        card.place(relx=0.5, rely=0.5, anchor="center")
        # Prevent the card from shrinking to fit its children; force it to remain 400x500
        card.pack_propagate(False)

        # Draw the main title text inside the card
        ctk.CTkLabel(card, text="Smart ERP", font=ctk.CTkFont(size=28, weight="bold"), text_color="#1d4ed8").pack(pady=(40, 10))
        # Draw the subtitle text
        ctk.CTkLabel(card, text="Please login to your account", font=ctk.CTkFont(size=14), text_color="#6b7280").pack(pady=(0, 40))

        # Create the username text input box
        self.username_entry = ctk.CTkEntry(card, placeholder_text="Username", width=300, height=45, corner_radius=8, border_width=1)
        self.username_entry.pack(pady=(0, 20))

        # Create the password text input box, hiding characters with '*'
        self.password_entry = ctk.CTkEntry(card, placeholder_text="Password", show="*", width=300, height=45, corner_radius=8, border_width=1)
        self.password_entry.pack(pady=(0, 30))

        # Create the login button and bind it to the self.login() method
        login_btn = ctk.CTkButton(card, text="Login", command=self.login, width=300, height=45, corner_radius=8, font=ctk.CTkFont(weight="bold"))
        login_btn.pack()

    # Purpose:
    # Reads the text inputs, queries the database for the user, and verifies the password hash.
    # If successful, navigates to the Dashboard. If failed, shows an error box.
    #
    # Returns:
    # None
    def login(self):
        """
        Executes the authentication sequence when the Login button is clicked.
        """
        # Retrieve the plain text from the UI entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Query the database to see if this username exists
        user = self.db.get_user_by_username(username)
        
        # Check if the user exists AND if the provided password's hash matches the stored hash
        if user and verify_password(password, user['password_hash']):
            # Authentication passed! Store the user data in the global controller
            self.controller.current_user = user
            
            # Switch the visible screen from LoginPage to Dashboard
            self.controller.show_frame("Dashboard")
        else:
            # Authentication failed! Show a native Windows error popup
            messagebox.showerror("Error", "Invalid username or password")
