import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Define the directory for log files
logs_dir = os.path.join(os.path.dirname(__file__), 'api')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Function to create a specific logger
def create_logger(name, level, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Log file handler with rotation
    file_handler = TimedRotatingFileHandler(
        os.path.join(logs_dir, log_file),
        when='midnight',
        interval=1,
        backupCount=10
    )
    file_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Adding the file handler to the logger
    logger.addHandler(file_handler)
    
    return logger

# API logger
def get_api_logger():
    return create_logger('api_logger', logging.INFO, 'api_activity.log')

# Web routes logger
def get_web_logger():
    return create_logger('web_logger', logging.INFO, 'web_activity.log')

# Error logger
def get_error_logger():
    return create_logger('error_logger', logging.ERROR, 'error.log')
