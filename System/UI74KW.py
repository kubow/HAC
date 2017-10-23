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


class ShowEnc(GridLayout):
    main_text = ObjectProperty(None)
    
    def clear(self):
        self.main_text.text = ""
        self.main_text.focus = True


class MainApp(App):
    title = 'H808E'
    def build(self):
        return ShowEnc()
    
    
if __name__ == '__main__':
    MainApp().run()
