"""
Logging utilities for the application.
This module provides a set of functions to log messages at different levels.
"""

import logging
import sentry_sdk
from functools import wraps

# Configure the logger
logger = logging.getLogger(__name__)


def log_info(message):
    """
    Log a message at INFO level.

    Args:
        message (str): The message to log
    """
    logger.info(message)


def log_warning(message):
    """
    Log a message at WARNING level.

    Args:
        message (str): The message to log
    """
    logger.warning(message)


def log_error(message, exc_info=None):
    """
    Log a message at ERROR level and capture it with Sentry.

    Args:
        message (str): The message to log
        exc_info: Optional exception information to include
    """
    logger.error(message, exc_info=exc_info)
    sentry_sdk.capture_message(message, level="error")


def log_exception(message, exception=None):
    """
    Log an exception and capture it with Sentry.

    Args:
        message (str): Description of the exception context
        exception: The exception object to log
    """
    logger.exception(message)
    if exception:
        sentry_sdk.capture_exception(exception)


def log_function_call(func):
    """
    Decorator to log function calls with parameters and return values.

    Args:
        func: The function to decorate

    Returns:
        The decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        log_info(f"Calling {func_name} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            log_info(f"{func_name} executed successfully")
            return result
        except Exception as e:
            log_exception(f"Exception in {func_name}", e)
            raise

    return wrapper
