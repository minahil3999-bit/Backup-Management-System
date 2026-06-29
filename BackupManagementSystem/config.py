import os

# Project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Project folders
SOURCE_FOLDER = os.path.join(BASE_DIR, "source_files")
BACKUP_FOLDER = os.path.join(BASE_DIR, "backup_storage")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")
DATABASE_FOLDER = os.path.join(BASE_DIR, "database")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")
CONFIG_FOLDER = os.path.join(BASE_DIR, "config")

# Database file
DATABASE_NAME = os.path.join(DATABASE_FOLDER, "backup.db")

# Log file
LOG_FILE = os.path.join(LOG_FOLDER, "system.log")