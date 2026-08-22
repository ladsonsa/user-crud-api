import logging


def get_logger(name: str) -> logging.Logger:
    """Configures and retrieves a named logger instance.

    Ensures that handlers are attached only once to prevent duplicate log outputs
    across modules.

    Args:
        name (str): The name of the logger instance, typically `__name__` of the calling module.

    Returns:
        logging.Logger: A configured instance of `logging.Logger`.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
