import sys

import logging
from logging.handlers import TimedRotatingFileHandler

import core.config as config


# get logger
logger = logging.getLogger("main")

# create handler
handler = TimedRotatingFileHandler(
    # filename=f'{config.LOG_DIR}/runtime.log',
    filename='./runtime.log',
    when='D',
    interval=1,
    backupCount=90,
    encoding='utf-8',
    delay=False
)
stream_handler = logging.StreamHandler(sys.stdout)

# create format
fmt = logging.Formatter('%(asctime)s - %(name)s - %(funcName)20s() - %(levelname)s - %(message)s')

# add format to handler
handler.setFormatter(fmt=fmt)
stream_handler.setFormatter(fmt=fmt)

# add the handler to named logger
logger.addHandler(handler)
logger.addHandler(stream_handler)

if config.APP_DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

logger.info("Start logger")
