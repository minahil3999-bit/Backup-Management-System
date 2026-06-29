import os
import shutil

from logger import log_restore, log_error


def restore_backup(backup_path, restore_path):
    try:
        # Check if backup exists
        if not os.path.exists(backup_path):
            print("Backup folder not found.")
            log_error("Backup folder not found.")
            return

        # Create restore folder if it doesn't exist
        os.makedirs(restore_path, exist_ok=True)

        # Copy all files from backup to restore folder
        for item in os.listdir(backup_path):
            source = os.path.join(backup_path, item)
            destination = os.path.join(restore_path, item)

            if os.path.isdir(source):
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination)

        print("Restore completed successfully.")
        log_restore("Backup restored successfully.")

    except Exception as e:
        print("Error:", e)