from datetime import datetime
from kivy.core.audio import SoundLoader
from kivy.core.image import Image
from kivymd.uix.button import MDRaisedButton
from kivy.uix.popup import Popup
from pytz import timezone, all_timezones
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from kivymd.uix.pickers import MDTimePicker

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
                        text:"ALARM"
                        color:[1,1,1,1]
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
                MDLabel:
                    text: str(root.show(root.hours))+":"+str(root.minutes)+":"+str(root.seconds)+" "+str(root.meridian)
                    size_hint:1,0.2
                    font_name:"Lcd"
                    font_size:"40dp"
                    color:1,.5,1,1
                    halign: 'center'
                    valign: 'middle'
                BoxLayout:
                    MDLabel:
                        markup:True
                        id: time_label
                        text:str(root.show(root.set_hours))+"[size=50][color=#0000FF]h[/color][/size] : " +str(root.set_minutes)+"[size=50][color=#0000FF]m[/color][/size] : " +str(root.meridian)
                        font_name:"Lcd"
                        font_size:"80dp"
                        color:root.alarm_color
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
                        text: 'START'
                        text_color: 1, 1, 1, 1
                        on_press: root.start()
                        size_hint:0.25,0.3
                        pos_hint:{"x":0.06,"y":0.5}
                        
                    MDRectangleFlatButton:
                        text: 'STOP'
                        text_color: 1, 1, 1, 1
                        size_hint:0.25,0.3
                        on_press: root.stop()
                        pos_hint:{"x":0.7,"y":0.5}

                    MDRectangleFlatButton:
                        text: 'SET'
                        text_color: 1, 1, 1, 1
                        size_hint:0.25,0.3
                        on_release:root.show_time_picker()
                        pos_hint:{"x":0.375,"y":0.5}
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
            text:root.time_tell
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
    t = datetime.now(timezone(all_timezones[282]))
    meridian = StringProperty("AM")
    seconds = NumericProperty(t.second)
    minutes = NumericProperty(t.minute)
    hours = NumericProperty(t.hour)
    set_minutes = NumericProperty(t.minute)
    set_hours = NumericProperty(t.hour)
    set_meridian = StringProperty("AM")
    drop_down_hours = ListProperty()
    drop_down_minutes = ListProperty()
    alarm_color = ListProperty([1, 0, 0, 1])
    alarm_ring = BooleanProperty(False)
    sound = SoundLoader.load('alarm.wav')
    sound.loop = True
    avatar = StringProperty("transparent.png")
    dialogue_box = ListProperty([0, 0, 0, 0])
    triangle = StringProperty("transparent.png")
    dialogue = ListProperty([0, 0, 0, 0])
    time_tell = StringProperty("PLEASE SET THE\nALARM FIRST!")
    no_time=StringProperty("transparent.png")





    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        if self.set_hours >= 12:
            self.set_meridian = "PM"
        Clock.schedule_interval(self.increment_time, 1)
        for i in range(60):
            self.drop_down_minutes.append(str(i))
        for i in range(12):
            self.drop_down_hours.append(str(i + 1))

    def show(self,hr):
        if hr==0 or hr==12:
            t=12
        else:
            t=hr%12
        return t
    def increment_time(self, interval):
        if self.hours >= 12:
            self.meridian = "PM"
        else:
            self.meridian = "AM"
        self.seconds += 1
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
        if self.minutes == 60:
            self.hours += 1
            self.minutes = 0

    def start(self):
        self.alarm_ring=False
        self.time_tell = "alarm set to " + str(self.show(self.set_hours)) + ":" + str(
            self.set_minutes) + " " + self.set_meridian
        self.avatar_visible()
        self.conversion()
        Clock.schedule_interval(self.check_time, 1)
        self.alarm_color = [0, 1, 0, 1]
        Clock.schedule_once(self.avatar_invisible, 5)

    def check_time(self, args):
        if self.hours == self.set_hours and self.minutes == self.set_minutes and not self.alarm_ring:
            self.alarm_ring = True
            layout = BoxLayout(orientation="vertical")
            popup = Popup(title='TIME UP!', content=layout, size_hint=(None, None), size=("400dp", "400dp"),
                          auto_dismiss=False)
            popup.open()
            closeButton = MDRaisedButton(text="CLOSE ALARM!", size_hint=(1, None), size=(1, "40dp"))
            snoozeButton = MDRaisedButton(text="SNOOZE ALARM!", size_hint=(1, None), size=(1, "40dp"))
            layout.add_widget(closeButton)
            layout.add_widget(snoozeButton)
            sound = SoundLoader.load('alarm.wav')
            sound.loop = True
            sound.play()

            def closepopup(args):
                popup.dismiss()
                sound.stop()
                self.stop()

            def snooze(args):
                self.set_minutes += 10
                self.conversion()
                self.alarm_ring = False
                popup.dismiss()
                sound.stop()

            closeButton.bind(on_press=closepopup)
            snoozeButton.bind(on_press=snooze)

    def stop(self):
        self.alarm_ring = False
        Clock.unschedule(self.check_time)
        self.alarm_color = [1, 0, 0, 1]
        self.time_tell="alarm stopped!"

    def conversion(self):
        if self.set_minutes >= 60:
            self.set_hours += int(self.set_minutes / 60)
            self.set_minutes %= 60
        if self.set_meridian == "AM" and self.set_hours >= 12:
            self.set_hours -= 12
        if self.set_meridian == "PM" and self.set_hours < 12:
            self.set_hours += 12

    def get_time(self, instance, time):
        try:
            s = str(time)
            self.set_hours = int(s[:2])
            self.set_minutes = int(s[3:5])
            if self.set_hours >= 12:
                self.set_meridian = "PM"
            else:
                self.set_meridian = "AM"
            self.ids.time_label.text = str(self.show(self.set_hours)) + "[size=50][color=#0000FF]h[/color][/size] : " + str(self.set_minutes) + "[size=50][color=#0000FF]m[/color][/size] " + self.set_meridian
        except:
            pass

    def on_cancel(self, instance, time):
        pass

    def show_time_picker(self):
        args=1
        self.avatar_invisible(args)
        default_time = datetime.strptime("4:20:00", '%H:%M:%S').time()
        time_dialog = MDTimePicker()
        time_dialog.set_time(default_time)
        time_dialog.bind(on_cancel=self.on_cancel, time=self.get_time)
        time_dialog.open()
        self.alarm_color=[1,0,0,1]
    def avatar_visible(self):
        self.avatar = "skedy_chloe_avatar/chloe_default.png"
        self.triangle = "triangle.png"
        self.dialogue_box = [1, 1, 0, 1]
        self.dialogue = [0, 0, 0, 1]
    def avatar_invisible(self,args):
        self.avatar = "transparent.png"
        self.triangle = "transparent.png"
        self.dialogue_box = [0, 0, 0, 0]
        self.dialogue = [0, 0, 0, 0]

class TimeApp(MDApp):
    def build(self):
        return MainWidget()


TimeApp().run()
