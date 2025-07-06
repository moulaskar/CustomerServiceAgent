import logging
import sys
import os
# logger_util.py

import logging
import sys
import os

class ColorFormatter(logging.Formatter):
    GREY = "\x1b[38;20m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    format_str = "%(asctime)s - %(levelname)-8s - %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + format_str + RESET,
        logging.INFO: GREEN + format_str + RESET,
        logging.WARNING: YELLOW + format_str + RESET,
        logging.ERROR: RED + format_str + RESET,
        logging.CRITICAL: BOLD_RED + format_str + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.format_str)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_logger(session_id: str):
    """Initializes the logger for the app with both console and file output."""
    logger = logging.getLogger('adk_app')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    # Create logs directory
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Console Handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter())
    logger.addHandler(console_handler)

    # File Handler
    log_path = os.path.join(log_dir, f"{session_id}_app.log")
    file_handler = logging.FileHandler(log_path, mode="a")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

def get_logger():
    """Returns the configured logger."""
    return logging.getLogger("adk_app")
'''
class ColorFormatter(logging.Formatter):
    """A custom formatter to add colors to console log messages."""
    GREY = "\x1b[38;20m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    # The format string for the log message
    format_str = "%(asctime)s - %(levelname)-8s - %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + format_str + RESET,
        logging.INFO: GREEN + format_str + RESET,
        logging.WARNING: YELLOW + format_str + RESET,
        logging.ERROR: RED + format_str + RESET,
        logging.CRITICAL: BOLD_RED + format_str + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_logger(session_id: str):
    """Configures the logger with console and a session-specific file handler."""
    logger = logging.getLogger('adk_app')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Clear existing handlers to avoid duplicates if re-configuring
    if logger.hasHandlers():
        logger.handlers.clear()

    # Console Handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter())
    logger.addHandler(console_handler)

    # File Handler for the specific session
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{session_id}_app.log")

    file_handler = logging.FileHandler(log_file, mode='a')
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

def get_logger():
    """Gets the application logger instance."""
    return logging.getLogger('adk_app')
'''