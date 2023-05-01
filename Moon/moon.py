from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
import requests
import bs4
import re
Builder.load_string('''

<MainWidget>:
    FloatLayout:
        BoxLayout:
            BoxLayout:
                orientation:"vertical"
                FloatLayout:
                    Image:
                        source:"title.jpg"
                        pos_hint:{"x":0,"y":0}
                        size_hint:1,1
                        keep_ratio:False
                        allow_stretch:True
                    Label:
                        text:"MOON"
                        size_hint:0.1,0.1
                        background_color:255,255,255,0
                        pos_hint:{"x":0.45,"y":0.55}
                        font_size:"60dp"
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
                FloatLayout:
                    Image:
                        source:"moon_phase.png"
                        pos_hint:{"x":0,"y":0.6}
                        size_hint:0.5,0.4
                        keep_ratio:False
                        allow_stretch:True
                    Image:
                        source:"telescope.jpg"
                        pos_hint:{"x":0,"y":0}
                        size_hint:0.5,0.6
                        keep_ratio:False
                        allow_stretch:True
                    Image:
                        source:root.background
                        size_hint:0.5,0.4
                        pos_hint:{"x":0.5,"y":0.6}
                        keep_ratio:False
                        allow_stretch:True
                    Image:
                        source:"black.png"
                        size_hint:0.5,0.6
                        pos_hint:{"x":0.5,"y":0.0}
                        keep_ratio:False
                        allow_stretch:True
                    Image:
                        source:"scroll.png"
                        size_hint:0.5,0.6
                        pos_hint:{"x":0.5,"y":0.0}
                        keep_ratio:False
                        allow_stretch:True
                    Label:
                        text:root.scroll_text
                        color:0,0,0,1
                        size_hint:0.1,0.1
                        pos_hint:{"x":0.7,"y":0.2}
                        background_color:255,255,255,0
                        font_size:"23dp"
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
        Image:
            id:av
            source:root.avatar
            size_hint:1,1
            pos_hint:{"x":0.37,"y":0}
        Image:
            id:av
            source:root.no_time
            size_hint:1,1
            pos_hint:{"x":0.37,"y":0}
        BubbleButton:
            text:root.tell
            font_size:20
            color:root.dialogue
            pos_hint:{"x":0.47,"y":0.6}
            size_hint:0.3,0.3
            background_color:root.dialogue_box
            canvas.before:
                Color:
                    rgba:self.background_color
                Rectangle:
                    size:self.size
                    pos:self.pos
        Image:
            source:root.triangle
            color:[1,1,0,1]
            size_hint:0.05,0.264
            pos_hint:{"x":0.76,"y":0.599}
            
        
''')
class MainWidget(BoxLayout):
    avatar = StringProperty("transparent.png")
    dialogue_box = ListProperty([0, 0, 0, 0])
    triangle = StringProperty("transparent.png")
    dialogue = ListProperty([0, 0, 0, 0])
    tell = StringProperty()
    no_time = StringProperty("transparent.png")
    background=StringProperty()
    percentage = NumericProperty()
    scroll_text=StringProperty("OFFLINE")
    full_moon=StringProperty()
    new_moon = StringProperty()
    months=ListProperty(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
     "December","Jan.","Feb.","Mar.","Apr.","May.","Jun.","Jul.","Aug.","Sep.","Oct.","Nov.","Dec."])
    moon_list=ListProperty(["First","Third","Full","New","Waning","Waxing","Last"])
    moon_names=ListProperty(["waxing gibbous","waxing crescent","waning crescent","full moon","first quarter","last quarter","new moon"])
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.moonShape(self.isOnline())

    def isOnline(self):
        url = "https://www.geeksforgeeks.org"
        timeout = 10
        try:
            request = requests.get(url, timeout=timeout)
            return True

        except (requests.ConnectionError, requests.Timeout) as exception:
            return False
    def moonShape(self,isonline):
        if isonline==False:
            self.background="offline.jpg"
        else:
            moon_url="https://www.google.com/search?q=what+is+moon+phase+today&rlz=1C1CHBF_enIN960IN960&oq=what+is+moon+phase+today&aqs=chrome..69i57.6324j0j1&sourceid=chrome&ie=UTF-8"
            moon_request=requests.get(moon_url)
            moon_soup = bs4.BeautifulSoup(moon_request.text , "html.parser" )
            moon_result= moon_soup.find( "div" , class_='BNeawe' ).text
            for i in moon_result.split():
                if i in self.moon_list:
                    self.moon_shape = i + " " + moon_result.split()[moon_result.split().index(i) + 1]
            percentage_url="https://www.google.com/search?q=percentage+of+moon+visible+today&rlz=1C1CHBF_enIN960IN960&oq=percentage+of+moon+visible+today&aqs=chrome..69i57.6405j0j1&sourceid=chrome&ie=UTF-8"
            percentage_request=requests.get(percentage_url)
            percentage_soup = bs4.BeautifulSoup(percentage_request.text, "html.parser")
            percentage_result =percentage_soup.find("div", class_='BNeawe').text
            percent =re.findall(r'\d+\.\d+', percentage_result)
            self.percentage=float(percent[0])
            self.display_image(self.moon_shape)
            for i in range(0,len(moon_result.split())):
                self.tell+=moon_result.split()[i]+" "
                if i%3==0:
                    self.tell+="\n"
            self.scroll_text ="Percentage of moon visible:\n"+str(self.percentage)
    def display_image(self,result):
        if result.lower() in self.moon_names:
            self.background = "moon_shapes/"+result.lower()+".jpg"
        else:
            self.background = "moon_shapes/error.jpg"


    def avatar_visible(self):
        self.avatar = "skedy_chloe_avatar/chloe_intelligent.png"
        self.triangle = "triangle.png"
        self.dialogue_box = [1, 1, 0, 1]
        self.dialogue = [0, 0, 0, 1]

    def avatar_invisible(self):
        self.avatar = "transparent.png"
        self.triangle = "transparent.png"
        self.dialogue_box = [0, 0, 0, 0]
        self.dialogue = [0, 0, 0, 0]

    def on_touch_down(self,touch):
        if touch.is_double_tap:
            if self.isOnline():
                self.avatar_visible()
            else:
                self.avatar="skedy_chloe_avatar/chloe_sad.png"
                self.tell="OFFLINE!"
                self.triangle = "triangle.png"
                self.dialogue_box = [1, 1, 0, 1]
                self.dialogue = [0, 0, 0, 1]
        else:
            self.avatar_invisible()
class TimeApp(MDApp):
    def build(self):
        return MainWidget()
TimeApp().run()
