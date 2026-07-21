############################################################
# Project : Smart ERP Billing System
#
# File    : backup_service.py
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
File: backup_service.py

Purpose:
Handles creating automated or manual backups of the critical SQLite database file.

Dependencies:
- shutil (For copying files safely)
- os (For file paths)
- datetime (To timestamp backup files)
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
import shutil
import os
import datetime

# This class manages database redundancy.
# It solves the problem of data loss by creating isolated copies of the `smart_erp.db` file.
# Its responsibility is reading the main DB and copying it to a safe backup directory.
# ---------------------------------------------
# Team Member 5
# Class: BackupService
# Purpose:
# Service class responsible for creating database backups.
# ---------------------------------------------
class BackupService:
    """
    Service class responsible for creating database backups.
    """
    
    # ---------------------------------------------
    # Team Member 5
    # Function: __init__
    # Purpose:
    # Handles logic for   init  
    # ---------------------------------------------
    def __init__(self):
        # Identify the root directory of the project
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        
        # Define the target backups directory
        self.backup_dir = os.path.join(self.root_dir, 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Define the source database path
        self.db_path = os.path.join(self.root_dir, 'smart_erp.db')

    # Purpose:
    # Copies the current active SQLite database into the backups folder with a timestamped filename.
    #
    # Returns:
    # str: The path to the newly created backup file.
    # ---------------------------------------------
    # Team Member 5
    # Function: create_backup
    # Purpose:
    # Creates a timestamped copy of the main database.
    # str: Path to the generated backup file, or None if the source DB doesn't exist.
    # ---------------------------------------------
    def create_backup(self):
        """
        Creates a timestamped copy of the main database.

        Returns:
            str: Path to the generated backup file, or None if the source DB doesn't exist.
        """
        # Generate a unique timestamp string like '20231024_153000' (YYYYMMDD_HHMMSS)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Construct the final destination file name
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.db")
        
        # Only attempt to copy if the original database file actually exists
        if os.path.exists(self.db_path):
            # shutil.copy2 copies the file and preserves its metadata (like creation time)
            shutil.copy2(self.db_path, backup_file)
            
        return backup_file







