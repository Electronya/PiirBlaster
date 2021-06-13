import logging
import os


def initLogger():
    """
    Initialize the logger.
    """
    logger_level = logging.INFO

    if 'APP_ENV' in os.environ:
        if os.environ['APP_ENV'] == 'dev':
            logger_level = logging.DEBUG

    logging.basicConfig(level=logger_level,
                        format='%(asctime)s %(levelname)s:'
                        '%(name)s:%(message)s')

    return logging
