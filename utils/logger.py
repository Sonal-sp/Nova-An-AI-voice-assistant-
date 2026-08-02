import os
import sys
import logging
from datetime import datetime


def setup_production_logger(name: str = "nova") -> logging.Logger:
    """
    Configures production-grade structured logger outputting to console and rotating log file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    # Console Handler
    c_handler = logging.StreamHandler(sys.stdout)
    c_format = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s")
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)

    # File Handler
    try:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        f_handler = logging.FileHandler(os.path.join(log_dir, "nova_production.log"), encoding="utf-8")
        f_format = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)
    except Exception as e:
        logger.warning(f"Could not initialize file log handler: {e}")

    return logger
