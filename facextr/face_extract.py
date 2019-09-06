'''

TODO: from opencv/self trained model to FACENET
'''

import os
import cv2
import numpy as np
from .garbage_recognition import GarbageRecognition
from . import utils as utils


IMAGE_FORMATS = ['.jpg', '.png', '.jpeg']


class FaceExtractor(object):
    '''
    extract faces from images in root directory

    :param root_path: directory with images and subdirectories with images, which will be processed
    :param no_dir_list: list of subdirectories in root directory, which will not be processed
    :param logger: logger object
    :param console_info: boolean for printing to console
    '''

    def __init__(self, root_path, no_dir_list=[], logger = None, console_info = True):

        self.root_path = root_path
        self.console_info = console_info
        # boolean for printing progress (also console_info)
        self.console_progress = False

        self._import_logger(logger)

        if not os.path.isdir(self.root_path):
            self.logger.error('there is no directory {}'.format(root_path))
            raise OSError('Error, there is no directory {}'.format(root_path))

        self.no_dir_list = no_dir_list

        #get number of files
        self.file_count = self.count_image_files()
        self._welcome()

        self.logger.info('files in directory {} : {}'.format(self.root_path, self.file_count))
        if self.console_info:
            print('image files to process: {}'.format(self.file_count))

        self.progress = 0

        self.haarcascade = os.path.join(os.path.dirname(__file__),'incl/haarcascade_frontalface_default.xml')
        self.faceCascade = cv2.CascadeClassifier(self.haarcascade)
        self.scaleFactor = 1.3
        self.minNeighbors = 5


    def _import_logger(self, logger):
        '''if logger not specified, import '''
        if logger == None:
            self.log_handler = utils.create_log_handler( utils.LOG_FILE, mode = 'w')
            self.logger = utils.get_logger(__name__)
            self.logger = utils.set_handler(self.logger, self.log_handler)
        else:
            self.logger = logger


    def _welcome(self):
        if self.console_info:
            utils.welcome()


    def _print_state(self):
        if self.console_info or self.console_progress:
            utils.print_state(self.progress, self.file_count)


    def _get_dir_structure(self, origin_path):
        '''create directory if dir_structure = True'''
        difference = os.path.relpath(origin_path, self.root_path)
        new_upload_path = os.path.join(self.upload_path,difference)
        path = os.path.dirname(new_upload_path)
        if not os.path.isdir(path):
            os.makedirs(path)
            self.logger.info('path created {}'.format(path))
        return path


    def _process_image(self, image_path):
        '''read image, find faces (with opencv), classify by keras classifier, save, print progress'''
        if os.path.splitext(image_path)[-1].lower() in IMAGE_FORMATS:
            try:
                image = self._load_image(image_path)
                img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                index = 0
                for (x, y, w, h) in self._find_faces(img):
                    face_image = image[y:y + h, x:x + w]
                    face_image = self._edit_image(face_image)

                    upload_path = self.upload_path
                    if self.dir_structure:
                        upload_path = self._get_dir_structure(image_path)
                    if self._classify_image(img[y:y + h, x:x + w]):
                        self._save_image(face_image,index, upload_path)
                        self.logger.info('face detected {}'.format(image_path))
                    else:
                        if self.shit_dir:
                            path, file = os.path.split(upload_path)
                            shit_path = os.path.join(path, file + '_shit')
                            if not os.path.isdir(shit_path):
                                os.makedirs(shit_path)
                                self.logger.info('shit dir created {}'.format(shit_path))
                            self._save_image(face_image,index, shit_path)
                    index += 1

            except:
                self.logger.error('FAIL: {}\nerror:\n'.format(image_path), exc_info=True)

            self.progress += 1
            self._print_state()

        else:
            self.logger.info('file not loaded : {}'.format(image_path))


    def _find_faces(self, img):
        '''opencv find faces with cascade'''
        faces = self.faceCascade.detectMultiScale(
            img,
            scaleFactor=self.scaleFactor,
            minNeighbors=self.minNeighbors,
        )
        for (x, y, w, h) in faces:
            yield  (x, y, w, h)


    def _load_image(self, image_path):
        '''load image (also read image when filename in unicode)'''
        try:
            stream = open(u'{}'.format(image_path), "rb")
            bytes = bytearray(stream.read())
            numpyarray = np.asarray(bytes, dtype=np.uint8)
            image = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)

            if self.gray:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return image

        except:
            self.logger.error('FAIL: {}\nerror:\n'.format(image_path), exc_info=True)


    def _edit_image(self, image):
        '''resizing image to specified shape'''
        face = cv2.resize(image, (self.img_shape[0], self.img_shape[1]))
        return face


    def _classify_image(self, image_path):
        '''classifying image with trained keras model'''
        prediction = self.classifier.classify_as_shit(image_path)
        return not prediction


    def _save_image(self, image, index, upload_path):
        '''save image in upload_path (with structure if dir_structure set)'''
        name = ''.join(['0' for i in range(len(str(self.file_count)) - len(str(self.progress)))]) + str(self.progress) + '_' + str(index)
        full_path = os.path.join(upload_path, '{}.{}'.format(name, self.img_format))
        cv2.imwrite(full_path, image)


    def count_image_files(self):
        '''walks through root directory and subdirectories and count number of files'''
        count = 0
        for root, dirs, files in os.walk(self.root_path, topdown=True):
            [dirs.remove(d) for d in list(dirs) if d in self.no_dir_list]
            count += len([file for file in files if os.path.splitext(file)[-1].lower() in IMAGE_FORMATS])
        return count


    def _face_extract(self, file_path):
        '''recursive func for face extraction'''
        full_path = os.path.join(self.root_path, file_path)
        if not os.path.isdir(full_path):
            self._process_image(full_path)
            return
        for i in os.listdir(full_path):
            if i not in self.no_dir_list:
                self._face_extract(os.path.join(full_path, i))


    def face_extract(self, upload_path, img_shape = (100,100), gray = False, img_format = 'jpg', dir_structure = False,
                     model_path = os.path.join(os.path.dirname(__file__), 'incl/02model_100x100.h5'), shit_dir = True):
        '''
        face extraction from root path

        :param upload_path: path for uploading files with faces
        :param img_shape: shape of required images (faces)
        :param gray: boolean for images in gray
        :param img_format: format of saved images
        :param dir_structure: same the structure of directories in upload path as in root path
        :param model_path: path for .h5 trained model, default = 02model_100x100
        :param shit_dir: there will be created directories for images classified as garbage
        '''

        self.upload_path = upload_path
        if not os.path.isdir(self.upload_path):
            os.makedirs(self.upload_path)
            self.logger.info('path created {}'.format(upload_path))

        self.img_shape = img_shape
        self.gray = gray
        self.img_format = img_format
        self.dir_structure = dir_structure
        self.model = model_path
        self.shit_dir = shit_dir

        self.classifier = GarbageRecognition()
        self.classifier.load_trained_model(self.model)
        self._face_extract(self.root_path)
