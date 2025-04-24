# logger.py
import os
from datetime import datetime

# Путь к лог-файлу
LOG_FILE = os.path.join(os.path.dirname(__file__), "log.txt")

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    print(full_message)  # В консоль
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_message + "\n")
