from kivy.core.image import Image
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
import requests
import bs4

Builder.load_string('''

<MainWidget>:
    FloatLayout:
        BoxLayout:
            Image:
                source:"weather/weather_left.png"
                pos_hint:{"x":0.0,"y":0.0}
                size_hint:0.2,1
                keep_ratio:False
                allow_stretch:True
            BoxLayout:
                orientation:"vertical"
                FloatLayout:
                    Image:
                        source:root.background
                        size_hint:1,2
                        pos_hint:{"x":0,"y":-0.5}
                        keep_ratio:False
                        allow_stretch:True
                    

            Image:
                source:"weather/weather_right.png"
                size_hint:0.2,1
                keep_ratio:False
                allow_stretch:True
                pos_hint:{"x":0.0,"y":0.0}
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
        Label:
            text:root.weather_display
            font_size:"50dp"
            font_name:"Lcd"
            color:1,0,0,1
            pos_hint:{"y":-0.4}
            background_color:0,0,0,0
            canvas.before:
                Color:
                    rgba:self.background_color
                Rectangle:
                    size:self.size
                    pos:self.pos
        Label:
            text:root.temp
            font_size:"50dp"
            pos_hint:{"y":0.45}
            color:1,0.5,1,1
            background_color:0,0,0,0
            canvas.before:
                Color:
                    rgba:self.background_color
                Rectangle:
                    size:self.size
                    pos:self.pos

''')


class MainWidget(BoxLayout):
    avatar = StringProperty("transparent.png")
    dialogue_box = ListProperty([0, 0, 0, 0])
    triangle = StringProperty("transparent.png")
    dialogue = ListProperty([0, 0, 0, 0])
    tell = StringProperty()
    no_time = StringProperty("transparent.png")
    background = StringProperty()
    weather_list= ListProperty(["Partly Sunny","Scattered Thunderstorms","Showers","Scattered Showers","Rain and Snow","Overcast","Light Snow","Freezing Drizzle","Chance of Rain","Sunny","Clear","Mostly Sunny","Partly Cloudy","Mostly Cloudy","Chance of Storm","Rain","Chance of Snow","Cloudy","Mist","Storm","Thunderstorm","Chance of TStorm","Sleet","Snow","Icy","Dust","Fog","Smoke","Haze","Flurries","Light Rain","Snow Showers","Hail"])
    moon_list = ListProperty(["First", "Third", "Full", "New", "Waning", "Waxing", "Last"])
    weather_display=StringProperty()
    temp=StringProperty()
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.weather(self.isOnline())

    def isOnline(self):
        url = "https://www.geeksforgeeks.org"
        timeout = 10
        try:
            request = requests.get(url, timeout=timeout)
            return True

        except (requests.ConnectionError, requests.Timeout) as exception:
            return False

    def weather(self, isonline):
        if isonline == False:
            self.background = "offline.jpg"
        else:
            weather_url = "https://www.google.com/search?q=weather+forecast&rlz=1C1CHBF_enIN960IN960&oq=weather+forecast&aqs=chrome..69i57j0i271l2.2915j0j1&sourceid=chrome&ie=UTF-8"
            weather_request = requests.get(weather_url)
            weather_soup = bs4.BeautifulSoup(weather_request.text, "html.parser")
            string = weather_soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
            data = string.split('\n')
            time = data[0]
            sky =  data[1]
            self.weather_display=sky.upper()
            self.display_image(sky)
            temperature = weather_soup.find("div", class_='BNeawe').text
            self.temp=temperature.split()[len(temperature.split())-1]
            listdiv = weather_soup.findAll("div", attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
            strd=""
            for i in listdiv:
                strd+=(i.text)
            humidity_start= strd.find('Humidity')
            humidity= strd[humidity_start+9:humidity_start+13]
            for i in self.weather_list:
                if sky.lower()==i.lower():
                    self.tell="This is Chloe\nReporting weather\n"+time+"\n"+"Temperature is "+self.temp+"\n"+"Sky: "+sky+"\n"+"Humidity: "+humidity
                    break
                else:
                    self.tell="Oops! we ran into an error!"

    def display_image(self, result):
        for i in self.weather_list:
            if result.lower()==i.lower():
                self.background = "weather/"+result.lower()+".png"
                break
        else:
            self.background = "weather/error.png"

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

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            if self.isOnline():
                self.avatar_visible()
            else:
                self.avatar = "skedy_chloe_avatar/chloe_sad.png"
                self.tell = "OFFLINE!"
                self.triangle = "triangle.png"
                self.dialogue_box = [1, 1, 0, 1]
                self.dialogue = [0, 0, 0, 1]
        else:
            self.avatar_invisible()
        if touch.is_triple_tap:
            weather_alamanac = Carousel(direction='right')
            for i in range(33):
                src = "weather_book/weather_book_" + str(i + 1) + ".png"
                image = AsyncImage(source=src, keep_ratio=False, allow_stretch=True)
                weather_alamanac.add_widget(image)
            layout = BoxLayout(orientation="vertical")
            layout.add_widget(weather_alamanac)
            popup = Popup(title='WEATHER ALMANAC', content=layout, size_hint=(None, None), size=("400dp", "400dp"))
            popup.open()

    def full_new(self, s):
        for i in s.split()[1]:
            if i != ",":
                new_number = str(int(i) + 15)
        if s.split()[0] in ["January", "March", "May", "July", "August", "October", "December"]:
            days = 31
        if s.split()[0] == "February":
            days = 28
        else:
            days = 30
        if days >= int(new_number):
            self.new_moon = self.months[self.months.index(s.split()[0]) + 1] + " " + str(new_number)


class TimeApp(MDApp):
    def build(self):
        return MainWidget()


TimeApp().run()