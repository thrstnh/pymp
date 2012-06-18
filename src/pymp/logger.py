import time
import logging
from os.path import expanduser, join

def now():
    return time.strftime(TIME_PATTERN)

logger = None
PATTERN = '%(asctime)s::%(levelname)s::%(message)s'
TIME_PATTERN = '%Y%m%d%H%M%S'
LOG_DIR = expanduser('~/.pymp/log')
LOG_FILE = join(LOG_DIR, 'pympsession{}.log'.format(now()))

def init_logger():
    global logger
    if logger:
        return logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    fh = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter(PATTERN)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)
    return logger

logger = init_logger()
logger.debug(':start {}'.format(now()))
logger.debug(':log {}'.format(LOG_FILE))
