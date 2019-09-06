'''
uttils - logging handling
default log file = facextr_info.log
'''

import logging


LOG_FILE = 'facextr_info.log'


def create_log_handler(filename, mode):
        open(filename, 'w').close()
        file_handler = logging.FileHandler(filename, mode=mode)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%d-%b-%y %H:%M:%S')
        file_handler.setFormatter(formatter)
        return file_handler


def get_logger(logger):
        logger = logging.getLogger(logger)
        logger.setLevel(logging.INFO)

        return logger


def set_handler(logger, handler):
        logger.addHandler(handler)

        return logger