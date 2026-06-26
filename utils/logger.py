import logging
import sys
from datetime import datetime
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

import config

class LogSignal(QObject):
    """Signal to emit log messages to the UI."""
    new_log = pyqtSignal(str, str) # message, level (info, warning, error, success)

class CustomFormatter(logging.Formatter):
    """Custom formatter for console output with colors."""
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "[%(asctime)s] %(levelname)-8s %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: grey + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)

class AppLogger:
    """Centralized logging utility for the application."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance

    def _setup(self):
        self.logger = logging.getLogger("HCL_Notes_Downloader")
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent adding handlers multiple times if instantiated again
        if self.logger.handlers:
            return

        # UI Signal
        self.signals = LogSignal()

        # File Handler (Daily logs)
        log_file = config.LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("[%(asctime)s] %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(CustomFormatter())
        self.logger.addHandler(console_handler)

    def info(self, message: str, to_ui: bool = True):
        self.logger.info(message)
        if to_ui:
            self.signals.new_log.emit(message, "info")

    def warning(self, message: str, to_ui: bool = True):
        self.logger.warning(message)
        if to_ui:
            self.signals.new_log.emit(message, "warning")

    def error(self, message: str, exc_info=False, to_ui: bool = True):
        self.logger.error(message, exc_info=exc_info)
        if to_ui:
            self.signals.new_log.emit(message, "error")
            
    def success(self, message: str, to_ui: bool = True):
        self.logger.info(message)
        if to_ui:
            self.signals.new_log.emit(message, "success")

    def debug(self, message: str):
        self.logger.debug(message)

# Global instance
logger = AppLogger()
