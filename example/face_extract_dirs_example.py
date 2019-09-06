'''

example for extracting faces from multiple directories and their subdirectories
extract all faces from images from paths in list - dirs
upload_path - directory, where faces will be stored

this code doesn't process face extraction if number of files is more then 10000

'''

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import facextr


upload_path = r"C:\Users\user\tensorflow\keras\face_detection\face_extractor\results\dirs"

dirs = [r'\\123tb\Media\Photo\Pictures\2019', r'\\123tb\Media\Photo\Pictures\2018',
        r'\\123tb\Media\Photo\Pictures\2017', r'\\123tb\Media\Photo\Pictures\2016',
        r'\\123tb\Media\Photo\Pictures\2015', r'\\123tb\Media\Photo\Pictures\2014',
        r'\\123tb\Media\Photo\Pictures\2013', r'\\123tb\Media\Photo\Pictures\2012',
        r'\\123tb\Media\Photo\Pictures\2011', r'\\123tb\Media\Photo\Pictures\2010',
        r'\\123tb\Media\Photo\Pictures\2009', r'\\123tb\Media\Photo\Pictures\2008',
        r'\\123tb\Media\Photo\Pictures\2007', r'\\123tb\Media\Photo\Pictures\2006',
        r'\\123tb\Media\Photo\Pictures\2005']



if __name__ == '__main__':

    files = facextr.dirs_files_count(dirs)
    print('number of image files : {}'.format(files))
    if files < 10000:
        facextr.face_extract_dirs(dirs, upload_path, dir_structure = True)
    else:
        print('too much files to process, may take more then 6 hours')