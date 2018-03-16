import os, sys
try:
    from PIL import Image
    image_able = True
except ImportError:
    print('cannot work with images! ...')
    image_able = False
try:
    import pygame
    multi_able = True
except ImportError:
    print('cannot work with music and other! ...')
    multi_able = False 

def play_sound(sound_file_location):
    # sound_file_location must be a wav file
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file_location)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def play_sound_external_app(sound_file_location, app_name='mplayer'):
    if not sound_file_location:
        print('please submit a file to play...')
    player = cpc(app_name).run_stream(sound_file_location, "-ss", "30")
    # player.stdin.write("q")  # terminate player
    
def mirror_images_dir(path, to_dir):
    final_directory = FileSystemObject(to_dir)
    for root, directories, files in os.walk(path):
        append = FileSystemObject(root).extra_path_from(path)
        FileSystemObject(final_directory.append_objects(file=append)).object_create_neccesary()
        for filename in files:
            if '.jp' in filename.lower() or '.gi' in filename.lower():
                try:
                    fr = root + final_directory.separator + filename
                    ex = FileSystemObject(fr).extra_path_from(path)
                    to = final_directory.append_objects(file=ex)
                    img = Image.open(fr)
                    print(fr + ' >> ' + to)
                    img.save(open(to, 'w'))
                except:
                    print(str(sys.exc_info()[2]))
            else:
                print(filename + ' skipping ....')
                pass

if __name__ == '__main__':
    from OS74 import FileSystemObject, CurrentPlatformControl as cpc