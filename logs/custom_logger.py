import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Base directory for logs - same level as custom_logger.py
base_logs_dir = os.path.dirname(__file__)

def create_logger(name, level, log_subdir, log_filename, when='midnight', interval=1, backup_count=30):
    # Path for the log subdirectory
    log_dir_path = os.path.join(base_logs_dir, log_subdir)
    os.makedirs(log_dir_path, exist_ok=True)

    # Full path for the log file
    log_file_path = os.path.join(log_dir_path, log_filename)

    # Create the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create the file handler for logging
    file_handler = TimedRotatingFileHandler(log_file_path, when=when, interval=interval, backupCount=backup_count)
    file_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Optionally add a stream handler to output logs to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

# Create loggers
api_logger = create_logger('api_logger', logging.INFO, 'api', 'api_activity.log')
web_logger = create_logger('web_logger', logging.INFO, 'web', 'web_activity.log')
error_logger = create_logger('error_logger', logging.ERROR, 'error', 'error.log')
