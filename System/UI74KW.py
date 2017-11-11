import os.path
from kivy.resources import resource_add_path

KV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
resource_add_path(KV_PATH)
print KV_PATH
#import kivy
#kivy.require('1.7.1')
from kivy.lang import Builder
Builder.load_file('H808E.kv')


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
    fldr_lib, file_lib = FileSystemObject().object_read_split()
    actual_location = FileSystemObject().path
    
    def multimedia_content(self):
        print self.actual_location
        directory = FileSystemObject(self.actual_location).one_dir_up()
        self.fldr_lib, self.file_lib = FileSystemObject(directory).object_read_split()
        # self.do_layout()
        print dir(self)
        print '-'*20
        print dir(self.file_list)
        print '-'*20
        print dir(self.folder_list)
        self.file_list.append(self.file_lib)
        self.folder_list.append(self.fldr_lib)
    
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
