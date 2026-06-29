import sqlite3
import os
from config import DATABASE_NAME, DATABASE_FOLDER


def create_database():

    # Create database folder if it doesn't exist
    os.makedirs(DATABASE_FOLDER, exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    # Create Backup Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS backups(
        backup_id INTEGER PRIMARY KEY AUTOINCREMENT,
        backup_date TEXT,
        source TEXT,
        destination TEXT,
        backup_size TEXT,
        status TEXT,
        version INTEGER
    )
    """)

    # Create Recovery Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recovery_logs(
        recovery_id INTEGER PRIMARY KEY AUTOINCREMENT,
        backup_id INTEGER,
        recovery_date TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully.")
def insert_backup(date, source, destination, size, status, version):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO backups
    (backup_date, source, destination, backup_size, status, version)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (date, source, destination, size, status, version))

    conn.commit()
    conn.close()


def get_all_backups():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM backups")

    data = cursor.fetchall()

    conn.close()
    return data
def get_next_version():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(version) FROM backups")

    result = cursor.fetchone()

    conn.close()

    if result[0] is None:
        return 1

    return result[0] + 1
if __name__ == "__main__":
    create_database()