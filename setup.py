from setuptools import setup, find_packages

setup(name='facextr',
      version='0.0.1',
      description='A lib for extracting faces from images',
      author='JM',
      author_email='juro.marusic@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy'],
      url='https://github.com/J77M/facextr',
      keywords=['face detection', 'face extraction', 'opencv', 'keras', 'machine learning'])