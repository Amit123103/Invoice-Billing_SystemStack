############################################################
# Project : Smart ERP Billing System
#
# File    : connection.py
#
# Team Member :
# Team Member 5
#
# Module :
# Database & Integration
#
# Responsibilities :
# - SQLite
# - CRUD Operations
# - Database Integration
# - Validation
# - Testing
#
# Developed By :
# Team Member 5
############################################################
"""
File: connection.py

Purpose:
Manages the SQLite database connection using a Singleton pattern.
Ensures that only one connection pool/instance is created and shared across threads.

Dependencies:
- sqlite3 (Standard library DB engine)
- os (For resolving file paths)
- threading (To ensure thread-safety during instance creation)
project

"""


###########################################################
# Team Member 5
# Module: Database & Integration
# Completed:
# - SQLite
# - CRUD Operations
# - Database Integration
# - Validation
# - Testing
###########################################################
import sqlite3
import os
import threading

# This class manages all direct connectivity to the local SQLite database file.
# It solves the problem of multiple modules opening separate database connections,
# which can lead to file locking errors (database is locked) in SQLite.
# Its responsibility is to provide a unified, safe way to execute queries.
# ---------------------------------------------
# Team Member 5
# Class: DatabaseConnection
# Purpose:
# Singleton class for managing SQLite database connections securely.
# ---------------------------------------------
class DatabaseConnection:
    """
    Singleton class for managing SQLite database connections securely.
    """
    # Stores the single active instance of the class
    _instance = None
    
    # Threading lock prevents race conditions if two threads try to initialize simultaneously
    _lock = threading.Lock()
    
    # Purpose:
    # Overrides the default object creation to return the exact same instance every time.
    #
    # Returns:
    # DatabaseConnection: The singleton instance.
    def __new__(cls):
        """
        Creates or returns the existing singleton instance.
        """
        # Block other threads from entering this block until the current thread finishes
        with cls._lock:
            # If no instance exists yet, create one
            if cls._instance is None:
                # Call the parent class __new__ to actually allocate memory for the object
                cls._instance = super(DatabaseConnection, cls).__new__(cls)
                
                # Dynamically resolve the absolute path to the root directory where smart_erp.db will live
                # __file__ is connection.py, dirname(__file__) is database/, dirname(dirname) is root/
                cls._instance.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'smart_erp.db')
            
            # Return the single global instance
            return cls._instance

    # Purpose:
    # Creates and configures a fresh connection object to the database.
    #
    # Returns:
    # sqlite3.Connection: The configured connection object.
    # ---------------------------------------------
    # Team Member 5
    # Function: get_connection
    # Purpose:
    # Retrieves a configured SQLite connection.
    # ---------------------------------------------
    def get_connection(self):
        """
        Retrieves a configured SQLite connection.
        """
        # Connect to the SQLite file. check_same_thread=False allows GUI threads to access the DB
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        
        # Configure the connection to return rows as dictionaries rather than plain tuples
        # This allows us to access data like user['username'] instead of user[1]
        conn.row_factory = sqlite3.Row
        
        # SQLite disables foreign key constraints by default for backwards compatibility.
        # We explicitly turn them ON to enforce referential integrity (e.g. cascaded deletes)
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Return the ready-to-use connection
        return conn

    # Purpose:
    # Executes an INSERT, UPDATE, or DELETE SQL statement and commits it.
    #
    # Parameters:
    # query (str): The SQL statement to run.
    # params (tuple): The parameters to substitute into the query safely.
    #
    # Returns:
    # sqlite3.Cursor: The cursor after execution, useful for retrieving lastrowid.
    # ---------------------------------------------
    # Team Member 5
    # Function: execute
    # Purpose:
    # Executes a modifying query and commits the transaction.
    # ---------------------------------------------
    def execute(self, query, params=()):
        """
        Executes a modifying query and commits the transaction.
        """
        # Use context manager so the connection automatically closes when the block ends
        with self.get_connection() as conn:
            # Create a cursor, which is an object used to traverse records from a result set
            cursor = conn.cursor()
            
            # Execute the query securely. Using params prevents SQL Injection attacks!
            cursor.execute(query, params)
            
            # Commit the transaction to write changes to disk permanently
            conn.commit()
            
            # Return the cursor so the caller can check things like cursor.lastrowid
            return cursor

    # Purpose:
    # Executes a SELECT SQL statement and retrieves all matching rows.
    #
    # Parameters:
    # query (str): The SELECT SQL statement.
    # params (tuple): The parameters to substitute safely.
    #
    # Returns:
    # list: A list of sqlite3.Row objects representing the results.
    # ---------------------------------------------
    # Team Member 5
    # Function: fetchall
    # Purpose:
    # Executes a query and returns all resulting rows.
    # ---------------------------------------------
    def fetchall(self, query, params=()):
        """
        Executes a query and returns all resulting rows.
        """
        # Open connection
        with self.get_connection() as conn:
            # Create cursor
            cursor = conn.cursor()
            
            # Execute SELECT query
            cursor.execute(query, params)
            
            # fetchall() retrieves all rows returned by the database query and returns them as a list
            return cursor.fetchall()

    # Purpose:
    # Executes a SELECT SQL statement and retrieves only the very first matching row.
    #
    # Parameters:
    # query (str): The SELECT SQL statement.
    # params (tuple): The parameters to substitute safely.
    #
    # Returns:
    # sqlite3.Row or None: The single matching row, or None if no match found.
    # ---------------------------------------------
    # Team Member 5
    # Function: fetchone
    # Purpose:
    # Executes a query and returns only the first resulting row.
    # ---------------------------------------------
    def fetchone(self, query, params=()):
        """
        Executes a query and returns only the first resulting row.
        """
        # Open connection
        with self.get_connection() as conn:
            # Create cursor
            cursor = conn.cursor()
            
            # Execute SELECT query
            cursor.execute(query, params)
            
            # fetchone() retrieves just the first row. It is faster than fetchall() when we only need one record (like finding a user by ID)
            return cursor.fetchone()
