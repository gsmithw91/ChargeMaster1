import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Base logs directory
base_logs_dir = os.path.dirname(__file__)

# Function to create a specific logger
def create_logger(name, level, log_file_pattern, sub_folder):
    # Define the directory for log files
    logs_dir = os.path.join(base_logs_dir, sub_folder)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create a unique log file name with a timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = log_file_pattern.format(timestamp=timestamp)
    
    # Log file handler
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, log_file),
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=10
    )
    file_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Check if handlers are already added to avoid duplicate logs
    if not logger.handlers:
        # Adding the file handler to the logger
        logger.addHandler(file_handler)
    
    return logger

# API logger
def get_api_logger():
    return create_logger('api_logger', logging.INFO, 'api_activity_{timestamp}.log', 'api')

# Web routes logger
def get_web_logger():
    return create_logger('web_logger', logging.INFO, 'web_activity_{timestamp}.log', 'web')

# Error logger
def get_error_logger():
    return create_logger('error_logger', logging.ERROR, 'error_{timestamp}.log', 'error')
