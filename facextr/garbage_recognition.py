import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import keras
import numpy as np
from random import randint
import cv2


class GarbageRecognition:
    '''
    object for categorising faces detected by opencv, if they are real faces or garbage
    default trained model = 02model_100x100.h5 trained on specific family photo album (93% accuracy)

    ACCURACY MAY VARY

    '''
    def __init__(self, img_shape = (100,100)):

        self.img_shape = img_shape
        self.normalizer = 255
        self.x = []
        self.y = []


    def _import_model(self):
        '''create keras model and compile'''
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Conv2D(64, (3, 3), input_shape=self.xdata.shape[1:]))
        self.model.add(keras.layers.Activation('relu'))
        self.model.add(keras.layers.MaxPool2D(pool_size=(2, 2)))

        self.model.add(keras.layers.Conv2D(64, (3, 3)))
        self.model.add(keras.layers.Activation('relu'))
        self.model.add(keras.layers.MaxPool2D(pool_size=(2, 2)))

        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(64, activation='relu'))

        self.model.add(keras.layers.Dense(1, activation='sigmoid'))
        self._compile_model(self.model)


    def _compile_model(self, model):
        '''compile keras model'''
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


    def _load_image(self, image_path):
        #TODO: edit for reading unicode filenames
        '''loading image (cannot read images with unicode filenames)- converting to grey, resizing'''
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dat = self._edit_image(img)
        return dat


    def _edit_image(self,img):
        '''normalizing image and resizing'''
        img = img / self.normalizer
        dat = cv2.resize(img, (self.img_shape[0], self.img_shape[1]))
        return dat


    def _process_images(self, dirs, label):
        '''loading image files and preparing data'''
        for dir in dirs:
            for file in os.listdir(dir):
                index = randint(0, len(self.x))
                dat = self._load_image(os.path.join(dir, file))
                self.x.insert(index, dat)
                self.y.insert(index, label)
        return self.x, self.y


    def load_images(self, data1, data2):
        '''
        load files and process/edit images

        :param data1: list of directories with real faces (must be same image shape)
        :param data2: list of directories with garbage (must be same image shape + same as data1)
        :return:
        '''
        if not isinstance(data1, list):
            data1 = [data1]
        if not isinstance(data2, list):
            data2 = [data2]

        self._process_images(data1, 0)
        self._process_images(data2, 1)
        self.x = np.asarray(self.x)
        self.xdata = self.x.reshape((self.x.shape[0], self.x.shape[1], self.x.shape[2], 1))
        self.ydata = np.asarray(self.y)


    def data_info(self):
        '''print info about data'''
        print('data : shape: {} ; min: {} ; max: {} ; mean: {} ;'.format(self.xdata.shape, self.xdata.min(), self.xdata.max(), self.xdata.mean()))
        print('labels : shape: {} ; min: {} ; max: {} ; mean: {} ;'.format(self.ydata.shape, self.ydata.min(), self.ydata.max(), self.ydata.mean()))


    def fit(self):
        '''train model'''
        self._import_model()
        self.model.fit(self.xdata, self.ydata, batch_size=10, epochs=20, validation_split=0.2)


    def save_model(self, path):
        '''save model'''
        self.model.save(path)


    def load_trained_model(self, path):
        '''load pretrained model'''
        self.trained_model = keras.models.load_model(path)
        self._compile_model(self.trained_model)


    def classify_as_shit(self, img):
        '''

        :param img: image (face from opencv) in array format
        :return: boolean (True= image is garbage, False = image is face)
        '''
        data = self._edit_image(img)
        data = np.asarray([data])
        data = data.reshape((data.shape[0], data.shape[1], data.shape[2], 1))
        prediction = self.trained_model.predict(data)
        if prediction >= 0.5:
            return True
        return False
