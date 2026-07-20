from database.queries import DatabaseQueries

class AuditService:
    def __init__(self):
        self.db = DatabaseQueries()

    def log(self, user_id, action, target_type=None, target_id=None, details=None):
        self.db.log_audit(user_id, action, target_type, target_id, details)
