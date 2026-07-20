"""
File: main.py

Purpose:
The primary entry point of the Smart ERP application.
It initializes the GUI framework, configures the master visual theme, 
loads all internal pages into memory, and starts the event loop.

Dependencies:
- customtkinter (Theming and Window creation)
- tkinter (Underlying GUI engine)
- All the page classes from the gui/ folder.

Project: Smart ERP Billing System
"""

import customtkinter as ctk
import tkinter as tk

# Import all the GUI screens we have built
from gui.login_page import LoginPage
from gui.dashboard import Dashboard
from gui.customer_page import CustomerPage
from gui.inventory_page import InventoryPage
from gui.invoice_page import InvoicePage
from gui.reports_page import ReportsPage
from gui.settings_page import SettingsPage

# -------------------------------------------------------------------
# Global Application Styling
# -------------------------------------------------------------------
# Set the master theme to Light mode so we get the clean white aesthetics matching modern web apps.
ctk.set_appearance_mode("Light")  
# Set the default accent color to Blue (affects buttons, sliders, selections)
ctk.set_default_color_theme("blue")  

# This is the master application class that inherits from CTk (the main window).
# It solves the problem of how to navigate between multiple different screens.
# Its responsibility is keeping track of who is logged in and showing/hiding pages on demand.
class SmartERPApp(ctk.CTk):
    """
    The Root Window and Page Controller for the application.
    """
    
    def __init__(self):
        # Initialize the underlying Tkinter root window
        super().__init__()
        
        # Configure basic window properties
        self.title("Smart ERP Billing System")
        self.geometry("1200x800")
        self.minsize(1024, 768)
        
        # Tracks the logged-in employee. None means nobody is logged in yet.
        self.current_user = None

        # Create a massive container frame that fills the entire window.
        # This acts as a mounting point. We will place all our pages inside this container.
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="top", fill="both", expand=True)
        # Configure the grid so that whatever is placed in row 0, col 0 expands to fill all space.
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # A dictionary to hold instantiated pages in memory.
        # e.g. {"LoginPage": <LoginPage object>, "Dashboard": <Dashboard object>}
        self.frames = {}
        
        # Loop through a tuple of every class definition we imported
        for F in (LoginPage, Dashboard, CustomerPage, InventoryPage, InvoicePage, ReportsPage, SettingsPage):
            # Get the string name of the class (e.g. "LoginPage")
            page_name = F.__name__
            
            # Instantiate the page. 
            # We pass `self.container` as the parent widget where it will physically live.
            # We pass `self` as the controller so the page can call self.controller.show_frame() to navigate.
            frame = F(parent=self.container, controller=self)
            
            # Store it in our dictionary
            self.frames[page_name] = frame
            
            # Stack all frames precisely on top of each other at row 0, col 0.
            # They are all invisible right now because we haven't 'raised' any of them.
            frame.grid(row=0, column=0, sticky="nsew")

        # Kick off the application by forcing the Login screen to the top of the stack.
        self.show_frame("LoginPage")

    # Purpose:
    # The central navigation router of the application. It brings a requested page to the front.
    # It also handles nested routing (placing internal pages INSIDE the Dashboard).
    #
    # Parameters:
    # page_name (str): The exact class name of the page to navigate to.
    def show_frame(self, page_name):
        """
        Navigates the user to a different screen/page.
        """
        # Security Check: If they are trying to access a restricted page without logging in, force them to Login.
        if page_name != "LoginPage" and not self.current_user:
            page_name = "LoginPage"
            
        # Retrieve the requested frame object from our memory dictionary
        frame = self.frames[page_name]
        
        # -------------------------------------------------------------------
        # Nested Routing Logic
        # -------------------------------------------------------------------
        # If the user is trying to view an inner page (like Customers), we do NOT want to hide the Dashboard sidebar!
        # We must take the requested frame and shove it inside the Dashboard's inner `content` container.
        if page_name in ["CustomerPage", "InventoryPage", "InvoicePage", "ReportsPage", "SettingsPage"]:
            dashboard = self.frames["Dashboard"]
            
            # First, wipe whatever is currently displayed inside the Dashboard's content area
            for widget in dashboard.content.winfo_children():
                widget.pack_forget()
                
            # Second, pack the newly requested page directly inside the Dashboard
            frame.pack(in_=dashboard.content, fill="both", expand=True)
            
            # Third, bring the entire Dashboard to the absolute front of the main window stack
            self.frames["Dashboard"].tkraise()
        else:
            # If the page is "LoginPage" or "Dashboard" itself, just bring it to the absolute front.
            frame.tkraise()

        # -------------------------------------------------------------------
        # Dynamic Data Refreshing
        # -------------------------------------------------------------------
        # When we switch pages, the data shown on the screen might be stale.
        # We dynamically check if the newly loaded frame has specific refresh functions, and if so, call them.
        # hasattr() checks if the function exists on the object before calling it, preventing crash errors.
        if hasattr(frame, 'load_dropdowns'):
            frame.load_dropdowns()
        if hasattr(frame, 'load_customers'):
            frame.load_customers()
        if hasattr(frame, 'load_products'):
            frame.load_products()
        if hasattr(frame, 'load_settings'):
            frame.load_settings()

# Python idiom: This block only runs if you type `python main.py` in the console.
if __name__ == "__main__":
    # Create the application window object
    app = SmartERPApp()
    
    # Start the infinite GUI event loop that listens for mouse clicks and keyboard typing.
    # The application runs continuously until this loop is broken (when the user clicks the red X to close the app).
    app.mainloop()
