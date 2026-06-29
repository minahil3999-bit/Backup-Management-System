import os
import shutil
from datetime import datetime

from config import SOURCE_FOLDER, BACKUP_FOLDER
from database import insert_backup, get_next_version
from logger import log_backup, log_error


def create_backup():
    try:
        # Check if source folder exists
        if not os.path.exists(SOURCE_FOLDER):
            print("Source folder does not exist.")
            log_error("Source folder not found.")
            return

        # Create backup folder if it doesn't exist
        os.makedirs(BACKUP_FOLDER, exist_ok=True)

        # Create unique backup folder name
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"Backup_{current_time}"

        destination = os.path.join(BACKUP_FOLDER, backup_name)

        # Copy source folder
        shutil.copytree(SOURCE_FOLDER, destination)

        # Calculate backup size
        total_size = 0

        for folder, subfolders, files in os.walk(destination):
            for file in files:
                file_path = os.path.join(folder, file)
                total_size += os.path.getsize(file_path)

        size_mb = round(total_size / (1024 * 1024), 2)
        version = get_next_version()
        # Save backup information
        insert_backup(
            current_time,
            SOURCE_FOLDER,
            destination,
            f"{size_mb} MB",
            "Success",
            version
        )

        # Write log
        log_backup(f"Backup {backup_name} created successfully.")

        print("Backup completed successfully!")

    except Exception as e:
        print("Error:", e)
        log_error(str(e))