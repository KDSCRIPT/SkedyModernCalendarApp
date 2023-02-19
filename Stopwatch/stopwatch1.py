from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.app import MDApp

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
                        text:"STOPWATCH"
                        size_hint:0.1,0.1
                        background_color:255,255,255,0
                        pos_hint:{"x":0.45,"y":0.5}
                        font_size:"60dp"
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
                BoxLayout:

                    Label:
                        text:str(round(root.stopwatch_minutes))
                        font_name:"Lcd"
                        font_size:"80dp"
                        color:1,.5,1,1
                        halign: 'center'
                        valign: 'middle'
                        background_color:(0,0,0,1)
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
                    Label:
                        text:"M:"
                        font_name:"Lcd"
                        font_size:"40dp"
                        color:1,165/255,0,1
                        halign: 'center'
                        valign: 'middle'
                        background_color:(0,0,0,1)
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
                    Label:
                        text:str(round(root.stopwatch_seconds))
                        font_name:"Lcd"
                        font_size:"80dp"
                        color:1,.5,1,1
                        halign: 'center'
                        valign: 'middle'
                        background_color:(0,0,0,1)
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
                    Label:
                        text:"S:" 
                        font_name:"Lcd"
                        font_size:"40dp"
                        color:1,165/255,0,1
                        halign: 'center'
                        valign: 'middle'
                        background_color:(0,0,0,1)
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
                    Label:
                        text:str(round(root.stopwatch_milli))
                        font_name:"Lcd"
                        font_size:"80dp"
                        color:1,.5,1,1
                        halign: 'center'
                        valign: 'middle'
                        background_color:(0,0,0,1)
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
                    Label:
                        text:"MS"
                        font_name:"Lcd"
                        font_size:"40dp"
                        color:1,165/255,0,1
                        halign: 'center'
                        valign: 'middle'
                        background_color:(0,0,0,1)
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
                FloatLayout:
                    Image:
                        source:"lap_box.jpg"
                        size_hint:1,1
                        pos_hint:{"x":0,"y":0}
                        keep_ratio:False
                        allow_stretch:True
                    Label:
                        text:root.stopwatch_lap_string
                        font_size:"14dp"
                        pos_hint:{"x":0.0,"y":0.0}
                        color:1,1,1,1
                FloatLayout:
                    Label:
                        pos_hint:{"x":0.0001,"y":0}
                        background_color:(0,0,0,1)
                        canvas.before:
                            Color:
                                rgba:self.background_color
                            Rectangle:
                                size:self.size
                                pos:self.pos
                    MDRectangleFlatButton:
                        text: 'Start'
                        on_press: root.stopwatch_start()
                        size_hint:0.4,0.4
                        pos_hint:{"x":0.06,"y":0.05}
                        
                    MDRectangleFlatButton:
                        text: 'Stop'
                        on_press: root.stopwatch_stop()
                        size_hint:0.4,0.4
                        pos_hint:{"x":0.54,"y":0.05}

                    MDRectangleFlatButton:
                        text: 'Reset'
                        on_press: root.stopwatch_reset()
                        size_hint:0.4,0.4
                        pos_hint:{"x":0.06,"y":0.5}
                    MDRectangleFlatButton:
                        text: 'Lap'
                        on_press: root.stopwatch_notelap()
                        size_hint:0.4,0.4
                        pos_hint:{"x":0.54,"y":0.5}
        Image:
            id:av
            source:root.stopwatch_avatar
            size_hint:1,1
            pos_hint:{"x":0.37,"y":0}
        BubbleButton:
            text:root.stopwatch_time_tell
            font_size:20
            color:root.stopwatch_dialogue
            pos_hint:{"x":0.47,"y":0.7}
            size_hint:0.3,0.3
            background_color:root.stopwatch_dialogue_box
            canvas.before:
                Color:
                    rgba:self.background_color
                Rectangle:
                    size:self.size
                    pos:self.pos
        Image:
            source:root.stopwatch_triangle
            color:[1,1,0,1]
            size_hint:0.05,0.264
            pos_hint:{"x":0.76,"y":0.599}
        
       
''')


class MainWidget(BoxLayout):
    stopwatch_lap_count = NumericProperty()
    stopwatch_milli = NumericProperty()
    stopwatch_seconds = NumericProperty()
    stopwatch_minutes = NumericProperty()
    stopwatch_laps = ListProperty()
    stopwatch_lap_string = StringProperty()
    stopwatch_avatar = StringProperty("transparent.png")
    stopwatch_dialogue_box = ListProperty([0, 0, 0, 0])
    stopwatch_dialogue = ListProperty([0, 0, 0, 0])
    stopwatch_triangle = StringProperty("transparent.png")
    stopwatch_lap_list = BoxLayout(orientation="vertical")
    stopwatch_time_tell=StringProperty()
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
    def stopwatch_increment_time(self, interval):
        self.stopwatch_milli += 1
        if self.stopwatch_milli == 100:
            self.stopwatch_seconds += 1
            self.stopwatch_milli = 0
        if self.stopwatch_seconds == 60:
            self.stopwatch_minutes += 1
            self.stopwatch_seconds = 0

    def stopwatch_start(self):
        Clock.unschedule(self.stopwatch_increment_time)
        Clock.schedule_interval(self.stopwatch_increment_time, 0.01)

    def stopwatch_stop(self):
        self.stopwatch_avatar = "skedy_chloe_avatar/chloe_default.png"
        self.stopwatch_triangle = "triangle.png"
        self.stopwatch_dialogue_box = [1, 1, 0, 1]
        self.stopwatch_dialogue = [0, 0, 0, 1]
        if self.stopwatch_minutes==0:
            if self.stopwatch_seconds==0:
                self.stopwatch_time_tell = str(self.stopwatch_milli) + " milliseconds"
            else:
                self.stopwatch_time_tell =str(self.stopwatch_seconds) + " seconds, \n" + str(self.stopwatch_milli) + " milliseconds"
        else:
            self.stopwatch_time_tell=str(self.stopwatch_minutes)+" minutes, \n"+str(self.stopwatch_seconds)+" seconds, \n"+str(self.stopwatch_milli)+" milliseconds"
        Clock.unschedule(self.stopwatch_increment_time)


    def stopwatch_reset(self):
        Clock.unschedule(self.stopwatch_increment_time)
        self.stopwatch_milli = 0
        self.stopwatch_seconds = 0
        self.stopwatch_minutes = 0
        self.stopwatch_laps = []
        self.stopwatch_lap_string = ""
        self.stopwatch_lap_count = 0
        self.stopwatch_avatar = "transparent.png"
        self.stopwatch_triangle = "transparent.png"
        self.stopwatch_dialogue_box = [0, 0, 0, 0]
        self.stopwatch_dialogue = [0, 0, 0, 0]

    def stopwatch_lap(self):
        self.stopwatch_laps.append(str(self.stopwatch_minutes) + ":" + str(self.stopwatch_seconds) + ":" + str(self.stopwatch_milli))

    def stopwatch_notelap(self):
        self.stopwatch_lap()
        if self.stopwatch_lap_count >= 5:
            self.stopwatch_lap_string = ""
            for i in range(len(self.stopwatch_laps) - 5, len(self.stopwatch_laps)):
                self.stopwatch_lap_string += "\n" + "LAP " + str(6 - len(self.stopwatch_laps) + i) + "   " + self.stopwatch_laps[i] + "\n"
        else:
            self.stopwatch_lap_string += "\n" + "LAP " + str(self.stopwatch_lap_count + 1) + "   " + self.stopwatch_laps[-1] + "\n"
        self.stopwatch_lap_count += 1

    def stopwatch_instructions(self):
        self.avatar = "skedy_chloe_avatar/chloe_default.png"
        self.triangle = "triangle.png"
        self.dialogue_box = [1, 1, 0, 1]
        self.dialogue = [0, 0, 0, 1]

class TimeApp(MDApp):
    def build(self):
        return MainWidget()


TimeApp().run()
