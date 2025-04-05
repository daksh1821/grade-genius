import logging
from logging.handlers import RotatingFileHandler
import os
import colorlog

LOG_DIR = "logs"
LOG_FILE = "app.log"

os.makedirs(LOG_DIR, exist_ok=True)

# Regular formatter for file logs
file_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)

# Colored formatter for console logs
color_formatter = colorlog.ColoredFormatter(
    '%(log_color)s[%(levelname)s] %(message)s',
    log_colors={
        'DEBUG':    'blue',
        'INFO':     'white,bg_green',
        'WARNING':  'bold,yellow',
        'ERROR':    'bold,red',
        'CRITICAL': 'white,bg_red,bold',
    },
)

# Console handler (with colors)
console_handler = colorlog.StreamHandler()
console_handler.setFormatter(color_formatter)

# File handler (with rotation, no colors)
file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3
)
file_handler.setFormatter(file_formatter)

# Logger setup
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.DEBUG)  # set to DEBUG to capture all logs
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.propagate = False
