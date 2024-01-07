import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Base directory for logs - same level as custom_logger.py
base_logs_dir = os.path.dirname(__file__)

# Logger instances dictionary
_loggers = {}

def create_logger(name, log_subdir, log_filename, when='midnight', interval=1, backup_count=30):
    global _loggers

    if _loggers.get(name):
        # Return existing logger
        return _loggers[name]

    try:
        # Path for the log subdirectory
        log_dir_path = os.path.join(base_logs_dir, log_subdir)
        os.makedirs(log_dir_path, exist_ok=True)

        # Full path for the log file
        log_file_path = os.path.join(log_dir_path, log_filename)

        # Create the logger
        logger = logging.getLogger(name)

        # Set level from environment variable, default to INFO
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        logger.setLevel(getattr(logging, log_level))

        # Create the file handler for logging
        file_handler = TimedRotatingFileHandler(log_file_path, when=when, interval=interval, backupCount=backup_count)
        file_handler.setLevel(getattr(logging, log_level))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Optionally add a stream handler to output logs to console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(getattr(logging, log_level))
        stream_handler.setFormatter(formatter)

        # Add handlers to the logger if they don't already exist
        if not any(isinstance(h, TimedRotatingFileHandler) for h in logger.handlers):
            logger.addHandler(file_handler)
        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            logger.addHandler(stream_handler)

        # Store the logger in the dictionary
        _loggers[name] = logger

        return logger
    except Exception as e:
        print(f"Error setting up logger: {e}")
        return logging.getLogger(name)  # Return a default logger in case of failure

# Create loggers
api_logger = create_logger('api_logger', 'api', 'api_activity.log')
web_logger = create_logger('web_logger', 'web', 'web_activity.log')
error_logger = create_logger('error_logger', 'error', 'error.log')
