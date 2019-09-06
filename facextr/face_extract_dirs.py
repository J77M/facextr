'''
functions to process directories independently
'''

import os
from .face_extract import FaceExtractor
from . import utils as utils


def dirs_files_count(list_of_dirs, no_dirs = [], log_handler = None):
    '''
    get number of files in list of directories

    :param list_of_dirs: list of directories
    :param no_dirs: list of subdirectories, which will not be processed
    :param log_handler: file handler for logger
    :return: numer of files
    '''
    if log_handler == None:
        log_handler = utils.create_log_handler(utils.LOG_FILE, mode='a')
    logger = utils.get_logger(__name__)
    logger = utils.set_handler(logger, log_handler)

    files_num = 0
    for dir in list_of_dirs:
        if not os.path.isdir(dir):
            logger.error('there is no directory {}'.format(dir))
            raise OSError('Error, there is no directory {}'.format(dir))
        _logger = utils.get_logger(dir)
        _logger = utils.set_handler(_logger, log_handler)
        facextr = FaceExtractor(dir, no_dirs, logger = _logger, console_info = False)
        files_num += facextr.count_image_files()
    return files_num


def face_extract_dirs(list_of_dirs, upload_path,  no_dirs = [], **kwargs):
    '''
    extracting faces from multiple independent directories and their subdirectories

    :param list_of_dirs: list of directories
    :param upload_path: path for uploading files with faces
    :param no_dirs: list of subdirectories, which will not be processed
    :param kwargs: parameters for face extract (see FaceExtractor.face_extract)
    '''

    utils.welcome()

    log_handler = utils.create_log_handler(utils.LOG_FILE, mode='a')
    logger = utils.get_logger(__name__)
    logger = utils.set_handler(logger, log_handler)

    if not os.path.isdir(upload_path):
        os.makedirs(upload_path)
        logger.info('path created {}'.format(upload_path))

    file_count = dirs_files_count(list_of_dirs, no_dirs = no_dirs, log_handler = log_handler, **kwargs)
    print('image files to process: {}'.format(file_count))
    progress = 0
    for dir in list_of_dirs:
        if not os.path.isdir(dir):
            logger.error('there is no directory {}'.format(dir))
            raise OSError('Error, there is no directory {}'.format(dir))

        last_dir = os.path.basename(dir)
        _upload_path = os.path.join(upload_path, last_dir)
        if not os.path.isdir(_upload_path):
            os.makedirs(_upload_path)
            logger.info('path created {}'.format(_upload_path))


        _logger = utils.get_logger(dir)
        _logger = utils.set_handler(_logger, log_handler)
        _facextr = FaceExtractor(dir, no_dirs, logger=_logger, console_info=False)
        _facextr.log_handler = log_handler

        _facextr.console_progress = True
        _facextr.progress = progress
        _facextr.file_count = file_count
        _facextr.face_extract(_upload_path, **kwargs)
        progress += _facextr.progress
