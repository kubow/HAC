import os
try:
    from PIL import Image
    image_able = True
except ImportError:
    print('cannot work with images! ...')
    image_able = False
from OS74 import FileSystemObject

    
def mirror_images_dir(path, to_dir):
    final_directory = 
    for root, directories, files in os.walk(path):
        print(root)
        for filename in files:
            print(filename)