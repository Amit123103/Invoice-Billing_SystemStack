"""
File: audit_service.py

Purpose:
Handles the logging of user actions across the system for security and auditing purposes.

Dependencies:
- database.queries (To execute the log insert)

Author: Amit Kumar
Project: Smart ERP Billing System
"""

from database.queries import DatabaseQueries

# This class manages the Audit Log.
# It solves the problem of tracking "Who did What and When" in an enterprise system.
# Its responsibility is strictly passing log strings to the database.
class AuditService:
    """
    Service class responsible for logging user actions.
    """
    
    def __init__(self):
        self.db = DatabaseQueries()

    # Purpose:
    # Inserts a new security log entry into the database.
    #
    # Parameters:
    # user_id (int): ID of the user performing the action.
    # action (str): Brief description of the action (e.g., 'Deleted Product').
    # target_type (str, optional): The type of object affected (e.g., 'Product').
    # target_id (int, optional): The ID of the affected object.
    # details (str, optional): Any extra JSON or string data explaining the change.
    def log(self, user_id, action, target_type=None, target_id=None, details=None):
        """
        Records an action into the audit_logs table.

        Args:
            user_id (int): The user's ID.
            action (str): Description of what happened.
            target_type (str, optional): The category of the affected entity.
            target_id (int, optional): The ID of the affected entity.
            details (str, optional): Additional context.
        """
        # Call the underlying database query wrapper to insert the row
        self.db.log_audit(user_id, action, target_type, target_id, details)
