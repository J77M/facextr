'''

example for extracting faces
extract all faces from images from path - directory (with all subdirectories)
upload_path - directory, where faces will be stored

'''

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import facextr


path = r'\\123tb\Media\Photo\Pictures\2019'
upload_path = r'\\123tb\Media\Photo\Pictures\2019-faces'

if __name__ == '__main__':
    face = facextr.FaceExtractor(path)

    face.face_extract(upload_path)