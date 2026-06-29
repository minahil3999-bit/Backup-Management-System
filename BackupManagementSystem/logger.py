import logging
import os
from config import LOG_FOLDER, LOG_FILE

# Create logs folder if it doesn't exist
os.makedirs(LOG_FOLDER, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_backup(message):
    logging.info(message)


def log_restore(message):
    logging.info(message)


def log_error(message):
    logging.error(message)