import logging
import os

LOG_PATH = "C:/Users/Никита/PycharmProjects/TamSyam/log/app.log"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logger = logging.getLogger("flask_app_logger")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_PATH, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "🔹 %(asctime)s | %(levelname)s | %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
