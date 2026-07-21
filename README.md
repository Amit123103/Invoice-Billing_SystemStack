# Smart ERP Billing System

## Overview
Smart ERP Billing System is a comprehensive desktop application designed to streamline billing, inventory management, and customer relations for businesses. Built with a modern Graphical User Interface (GUI) using Python and CustomTkinter, it provides a clean, user-friendly experience for day-to-day business operations.

## 📄 Project Documentation

Click below to view the complete project documentation.

📘 [Smart ERP Billing System Documentation](docs/billing.pdf)

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
# 🧾 Smart ERP Billing System

## 📌 About the Project

Smart ERP Billing System is a desktop application built using Python to help businesses manage their daily operations in one place. It provides an easy-to-use interface for handling customers, products, billing, and reports. The application is designed with CustomTkinter, making it simple, modern, and user-friendly.

This project is suitable for small businesses and shops that want to manage sales, inventory, and customer information efficiently.

---

## ✨ Features

- 🔐 Secure login system
- 📊 Simple dashboard with business overview
- 👥 Customer management
- 📦 Inventory and stock management
- 🧾 Invoice/Bill generation
- 📈 Sales and inventory reports
- ⚙️ Application settings
- 💾 Data stored using SQLite database

---

## 🛠️ Technologies Used

- **Python**
- **Tkinter**
- **CustomTkinter**
- **SQLite**

---

## 📂 Project Structure

```text
Smart-ERP-Billing-System/
│
├── main.py            # Starts the application
├── gui/               # All GUI screens
├── database/          # Database connection
├── models/            # Database models
├── services/          # Business logic
├── reports/           # Generated reports
├── qrcodes/           # Generated QR codes
└── requirements.txt   # Required Python packages
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone <repository-link>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the project

```bash
python main.py
```

---

## 🎯 Purpose

The main goal of this project is to simplify business management by providing a single application for billing, inventory, customer records, and reporting. It helps save time, reduce manual work, and organize business data efficiently.

---

## 👨‍💻 Developed By



Team Member 1 – Authentication & Dashboard Developer
Role

Frontend + Backend

Responsibilities
Login System
User Login
Secure Authentication
Password Validation
Forgot Password
Logout
Session Management
Dashboard
Dashboard UI
Statistics Cards
Quick Navigation
Recent Sales
Recent Customers
Revenue Summary
Low Stock Alerts
User Management
Add User
Edit User
Delete User
Roles (Admin, Cashier)
Settings
Business Information
Company Logo
GST Number
Currency
Theme Settings
Database Tables
users
settings
Deliverables
Login Page
Dashboard
User Module
Settings Module
Estimated Work
UI Screens: 5
Database Tables: 2
Backend Files: 6


Team Member 2 – Inventory Management Developer
Role

Inventory & Product Management

Responsibilities
Product Management
Add Product
Update Product
Delete Product
Search Product
Product Categories
Inventory
Stock In
Stock Out
Quantity Update
Low Stock Alert
Barcode Support
QR Code Generation
Supplier Module
Add Supplier
Edit Supplier
Delete Supplier
Purchase History
Purchase Module
Purchase Entry
Purchase Invoice
Purchase Return
Database Tables
products
categories
suppliers
purchases
Deliverables
Inventory Module
Supplier Module
Purchase Module
Estimated Work

UI Pages

6

Database Tables

4

Backend

8 Files



Team Member 3 – Customer & Billing Developer
Role

Customer Management + Billing

Responsibilities
Customer Module
Add Customer
Edit Customer
Delete Customer
Search Customer
Customer History
Billing Module
Product Selection
Shopping Cart
Quantity Update
Discount
GST
Grand Total
Payment Method
Cash Payment
UPI Payment
Card Payment
Bill Calculation
Tax
Discount
Total
Balance
Change Return
Database Tables
customers
bills
Deliverables
Customer Module
Billing Screen
Cart System
Estimated Work

UI Pages

5

Database

2 Tables

Backend

7 Files


Team Member 4 – Invoice, Reports & Printing Developer
Role

Invoice Management

Responsibilities
Invoice Module
Generate Invoice
Print Invoice
Save Invoice
Invoice History
Search Invoice
Download PDF
QR Code
Barcode
Reports

Daily Sales

Weekly Sales

Monthly Sales

Yearly Sales

Inventory Report

Customer Report

Product Report

Purchase Report

Profit Report

GST Report

Graphs

Sales Graph

Revenue Graph

Inventory Graph

Best Selling Products

Export

Excel

PDF

CSV

Database Tables
invoices
invoice_items
Deliverables

Invoice Module

Reporting Module

Printing Module

Estimated Work

UI

5 Pages

Database

2 Tables

Backend

9 Files

Team Member 5 – Database, Integration, Testing & Deployment
Role

Backend + Database + Final Integration

Responsibilities
Database

Design SQLite Database

Create Tables

Relationships

Indexes

Foreign Keys

Triggers

Backup

Restore

API / Service Layer

Database Connection

CRUD Operations

Validation

Logging

Exception Handling

Testing

Unit Testing

Integration Testing

System Testing

Bug Fixing

Performance Testing

Security Testing

Documentation

README

Installation Guide

User Manual

Developer Guide

SRS

Project Report

Deployment

Executable (.exe)

Packaging

Requirements

GitHub

Release

Deliverables

Database

Integration

Testing

Deployment

Documentation

Estimated Work

Database Tables

All Tables

Testing

Complete

Documentation

Complete

Deployment

Complete