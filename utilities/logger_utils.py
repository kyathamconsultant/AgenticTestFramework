"""
Logger utility for the framework
"""
import logging
import sys
from pathlib import Path
from config.config import Config


class LoggerSetup:
    """Setup logger for the framework"""

    _loggers = {}

    @staticmethod
    def get_logger(name):
        """Get or create a logger"""
        if name in LoggerSetup._loggers:
            return LoggerSetup._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(Config.LOG_LEVEL)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(Config.LOG_LEVEL)

        # File handler
        log_file = Config.LOGS_DIR / f"{name}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(Config.LOG_LEVEL)

        # Formatter
        formatter = logging.Formatter(Config.LOG_FORMAT)
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        LoggerSetup._loggers[name] = logger
        return logger


def get_logger(name):
    """Convenience function to get logger"""
    return LoggerSetup.get_logger(name)
