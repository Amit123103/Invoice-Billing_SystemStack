import shutil
import os
import datetime

class BackupService:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        self.backup_dir = os.path.join(self.root_dir, 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
        self.db_path = os.path.join(self.root_dir, 'smart_erp.db')

    def create_backup(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.db")
        if os.path.exists(self.db_path):
            shutil.copy2(self.db_path, backup_file)
        return backup_file
