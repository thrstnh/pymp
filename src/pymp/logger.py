import logging

logger = None


def init_logger():
    global logger
    if logger:
        return logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)
    return logger


