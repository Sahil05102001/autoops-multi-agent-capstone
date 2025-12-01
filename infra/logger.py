# infra/logger.py
import logging
import os
from typing import Optional

def get_logger(name: str = "agent", level: Optional[str] = None) -> logging.Logger:
    """
    Return a configured logger.
    - Respects LOG_LEVEL env var (e.g. DEBUG, INFO, WARNING).
    - Avoids adding duplicate handlers (useful in notebooks).
    - Disables propagation to prevent duplicate logs.
    """
    logger = logging.getLogger(name)

    # Determine level: explicit param -> env var -> default INFO
    level_str = level or os.environ.get("LOG_LEVEL", "INFO")
    level_val = getattr(logging, level_str.upper(), logging.INFO)
    logger.setLevel(level_val)

    # Add a single StreamHandler if none exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)

    # Avoid double logging if root logger also configured
    logger.propagate = False

    return logger
