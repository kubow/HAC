from kivy.lang import Builder
Builder.load_file('H808E.kv')
#import kivy
#kivy.require('1.7.1')

from kivy.app import App
from kivy.properties import ObjectProperty

#from kiwi.uix.scatter import Scatter
from kivy.uix.listview import ListItemButton
#from kivy.adapters.listadapter import ListAdapter
from kivy.uix.boxlayout import BoxLayout
#from kiwi.uix.floatlayout import FloatLayout #good na 3d
from kivy.uix.gridlayout import GridLayout

from  kivy.properties import ListProperty, StringProperty

import os
from OS74 import FileSystemObject

class ShowEnc(GridLayout):
    main_text = ObjectProperty(None)
    folder_list = ListProperty([])
    folder_select = StringProperty('Select a folder')
    file_list = ListProperty([])
    file_select = StringProperty('Select a file')
    mlt_lib = FileSystemObject().object_read()
    print type(mlt_lib)
    
    def multimedia_content(self, directory=''):
        self.mlt_lib = FileSystemObject(directory).object_read()
        self.media_content = self.mlt_lib
    
    def folder_on_select(self, change_value):
        self.selected_value = "Selected: {0}".format(change_value.text)

    def file_on_select(self, change_value):
        self.selected_value = "Selected: {0}".format(change_value.text)
    
    def clear(self):
        self.main_text.text = ""
        self.main_text.focus = True


class MainApp(App):
    title = 'H808E'
    def build(self):
        return ShowEnc()
        
    
if __name__ == '__main__':
    MainApp().run()
