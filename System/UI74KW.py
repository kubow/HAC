from kivy.lang import Builder
Builder.load_file('H808E.kv')
#import kivy
#kivy.require('1.7.1')

from kivy.app import App
from kivy.properties import ObjectProperty

#from kiwi.uix.scatter import Scatter
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.boxlayout import BoxLayout
#from kiwi.uix.floatlayout import FloatLayout #good na 3d
from kivy.uix.gridlayout import GridLayout

import os
from OS74 import FileSystemObject

class ShowEnc(GridLayout):
    main_text = ObjectProperty(None)
    
    def multimedia_content(self, directory=''):
        self.mlt_lib = FileSystemObject(directory)
        self.media_content = self.mlt_lib
    
    def clear(self):
        self.main_text.text = ""
        self.main_text.focus = True


class MainApp(App):
    title = 'H808E'
    def build(self):
        return ShowEnc()


def get_directory_content(path_to):
    """return multimedia library in format:
    mlt_lib = {'filename': '/path/to/filename'}
    mlt_lib = {'/dirname': '/path/to/dir'}
    """
    # path_to = get_proper_dir_path(path_to)
    mlt_lib = {}
    for mlt_file in os.listdir(path_to):
        if os.path.isdir(path_to + mlt_file):
            mlt_lib[mlt_file] = path_to + mlt_file
        else:
            mlt_lib[mlt_file] = path_to + mlt_file
    print mlt_lib
    return mlt_lib

        
    
if __name__ == '__main__':
    MainApp().run()
