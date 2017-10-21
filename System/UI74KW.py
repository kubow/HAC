from kivy.lang import Builder
Builder.load_file('UI74KW.kv')
#import kivy
#kivy.require('1.7.1')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

#from kiwi.uix.scatter import Scatter
#from kiwi.uix.floatlayout import FloatLayout #good na 3d

class ShowEnc(BoxLayout):
    main_text = ObjectProperty(None)
    
    def clear(self):
        self.main_text.text = ""
        self.main_text.focus = True


class MainApp(App):
    def build(self):
        return ShowEnc()
    
    
if __name__ == '__main__':
    MainApp().run()
