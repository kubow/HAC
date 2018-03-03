import os, sys
try:
    from PIL import Image
    image_able = True
except ImportError:
    print('cannot work with images! ...')
    image_able = False
from OS74 import FileSystemObject

    
def mirror_images_dir(path, to_dir):
    final_directory = FileSystemObject(to_dir)
    for root, directories, files in os.walk(path):
        append = FileSystemObject(root).extra_path_from(path)
        FileSystemObject(final_directory.append_file(append)).object_create_neccesary()
        for filename in files:
            if '.jp' in filename.lower() or '.gi' in filename.lower():
                try:
                    fr = root + final_directory.separator + filename
                    ex = FileSystemObject(fr).extra_path_from(path)
                    to = final_directory.append_file(ex)
                    img = Image.open(fr)
                    print(fr + ' >> ' + to)
                    img.save(open(to, 'w'))
                except:
                    print(str(sys.exc_info()[2]))
            else:
                print(filename + ' skipping ....')
                pass