import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


base_logs_dir = os.path.join(os.path.dirname(__file__), 'logs')

def create_logger(name, level, log_filename, when='midnight', interval=1, backup_count=30):
    # Ensure the base log directory exists
    os.makedirs(base_logs_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Log file path
    log_file_path = os.path.join(base_logs_dir, log_filename)
    
    # Log file handler with rotation
    file_handler = TimedRotatingFileHandler(
        log_file_path, when=when, interval=interval, backupCount=backup_count
    )
    file_handler.setLevel(level)
    
    # Stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG if os.getenv('DEBUG', 'False') == 'True' else logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger




api_logger = create_logger('api_logger', logging.INFO, os.path.join('api', 'api_activity.log'))
web_logger = create_logger('web_logger', logging.INFO, os.path.join('web', 'web_activity.log'))
error_logger = create_logger('error_logger', logging.ERROR, os.path.join('error', 'error.log'))
