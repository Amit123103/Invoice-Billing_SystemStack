# Smart ERP Billing System

## Overview
Smart ERP Billing System is a comprehensive desktop application designed to streamline billing, inventory management, and customer relations for businesses. Built with a modern Graphical User Interface (GUI) using Python and CustomTkinter, it provides a clean, user-friendly experience for day-to-day business operations.

## Key Features
- **Secure Login:** Access control to ensure secure usage of the system.
- **Interactive Dashboard:** Get a quick overview of business metrics and navigate easily between different modules.
- **Customer Management:** Maintain a detailed database of customers, track their details, and manage relationships efficiently.
- **Inventory Management:** Keep track of products, stock levels, and pricing to avoid shortages or overstocking.
- **Invoice Generation:** Create, manage, and print professional invoices for customers seamlessly.
- **Comprehensive Reports:** Generate detailed reports on sales, inventory, and other key metrics to make informed business decisions.
- **Customizable Settings:** Adapt the application to your business needs through a dedicated settings module.

## Technology Stack
- **Language:** Python
- **GUI Framework:** CustomTkinter & Tkinter
- **Database:** SQLite

## Project Structure
- `main.py`: The primary entry point of the application handling navigation and initialization.
- `gui/`: Contains all the GUI screen classes (Login, Dashboard, Inventory, etc.).
- `models/`: Database models and schema definitions.
- `services/`: Business logic and backend services.
- `database/`: Database connection and query scripts.
- `reports/`: Generated report files.
- `qrcodes/`: Generated QR codes for products/invoices.

## Getting Started
1. Ensure Python 3.x is installed on your system.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```
