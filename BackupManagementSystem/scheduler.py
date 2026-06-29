import schedule
import time
from backup import create_backup

# Schedule backup every day at 6:00 PM
schedule.every().day.at("18:00").do(create_backup)

print("Scheduler is running...")

while True:
    schedule.run_pending()
    time.sleep(1)