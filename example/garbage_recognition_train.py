'''

example for training conv NN
(used for classifying if image/face from opencv is real face or garbage)
path1 - directories with images - representative faces (same image shape)
path2 - directories with images - representative garbage (same image shape as in path1)

'''
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from facextr import garbage_recognition as grb


path1 = [r'C:\Users\user\tensorflow\keras\face_detection\face_extractor\results\2019\01',
         r'C:\Users\user\tensorflow\keras\face_detection\face_extractor\results\2005\01',
         r'C:\Users\user\tensorflow\keras\face_detection\face_extractor\results\2006\01']

path2 = [r'C:\Users\user\tensorflow\keras\face_detection\face_extractor\results\2019\01_shit',
         r'C:\Users\user\tensorflow\keras\face_detection\face_extractor\results\2005\01_shit',
         r'C:\Users\user\tensorflow\keras\face_detection\face_extractor\results\2006\01_shit']

if __name__ == '__main__':

    grbRec = grb.GarbageRecognition()
    grbRec.load_images(path1, path2)
    grbRec.data_info()
    grbRec.fit()
    grbRec.save_model('../facextr/incl/modelXX.h5')
