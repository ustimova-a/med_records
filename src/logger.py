import os
import sys
import yaml
import logging

from src.models.model_singleton import Singleton


class NotSetEnvException(Exception):
    def __init__(self, message="Not found MED_RECORDS_CONFIG in env"):
        super().__init__(message)


class Logger(metaclass=Singleton):
    def __init__(self):
        # if os.getenv('MED_RECORDS_CONFIG', None) is None:
        #     raise NotSetEnvException()

        # config = configparser.ConfigParser(config_path=os.getenv('MED_RECORDS_CONFIG', None))
        with open("config.yaml", "r") as file_object:
            config = yaml.load(file_object, Loader=yaml.SafeLoader)

        logger = logging.getLogger("main")

# create handler
        handler = logging.TimedRotatingFileHandler(
            filename=f'{config.get("Application", "logdir")}/runtime.log',
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

        if config['Application'].get('debug', False) == 'debug':
            logger.setLevel(logging.DEBUG)
        else:

            logger.setLevel(logging.INFO)
        logger.info("Started logging")

        self.logger = logger

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)
