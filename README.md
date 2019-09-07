# facextr
## v.0.0.1
### Introduction
library for extracting faces to separate images files from directory/directories of images
### Description
processes images and searches for faces in specific directory and its subdirectories. saves images in directory which is specified. also there is possibility to maintain structure of directories (same structure in dir, where images are saved and dir from where are images processed)

face extraction is composed of:
- [OpenCV](https://github.com/skvark/opencv-python) - find faces,
 the precession is bad (approximately 50% of found faces are garbage (parts of trees, cars, clothes,...))
- trained keras convolutional neural network -  checks if face from OpenCV is real face (precession 93%)

ACCURACY of this library MAY VARY (depends on images and types of people/faces)

| WARNING: a trained model can be discriminatory ! |
| --- |

there is possibility to train model - see documentation in code

### Install
```
git clone https://github.com/J77M/facextr.git
cd facextr
python setup.py
```
### Usage
for exampes see directory **examples**
```python
import facextr

# path where images are stored
path = r"C:\Users\user\tensorflow\keras\face_detection\face_extractor\images"
# path for saving results - faces
upload_path = r"C:\user\jurko\tensorflow\keras\face_detection\face_extractor\output"

face = facextr.FaceExtractor(path)
face.face_extract(upload_path)
```

JM