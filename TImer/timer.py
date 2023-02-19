from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
Builder.load_string('''
<MainWidget>:
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
                text:"TIMER"
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
            Spinner:
                id:hours_spinner
                text: str(round(root.timer_hours))
                on_text:root.timer_hours_selected(int(hours_spinner.text))
                values:root.timer_drop_down
                font_name:"Lcd"
                font_size:"80dp"
                color:1,1,0,1
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
                text:"H :"
                font_name:"Lcd"
                font_size:"40dp"
                color:1,0,0,1
                halign: 'center'
                valign: 'middle'
                background_color:(0,0,0,1)
                canvas.before:
                    Color:
                        rgba:self.background_color
                    Rectangle:
                        size:self.size
                        pos:self.pos
            Spinner:
                id:minutes_spinner
                text: str(round(root.timer_minutes))
                on_text:root.timer_minutes_selected(int(minutes_spinner.text))
                values:root.timer_drop_down
                font_name:"Lcd"
                font_size:"80dp"
                color:1,1,0,1
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
                text:"M :"
                font_name:"Lcd"
                font_size:"40dp"
                color:1,0,0,1
                halign: 'center'
                valign: 'middle'
                background_color:(0,0,0,1)
                canvas.before:
                    Color:
                        rgba:self.background_color
                    Rectangle:
                        size:self.size
                        pos:self.pos
            Spinner:
                id:second_spinner
                text: str(round(root.timer_seconds))
                on_text:root.timer_second_selected(int(second_spinner.text))
                values:root.timer_drop_down
                font_name:"Lcd"
                font_size:"80dp"
                color:1,1,0,1
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
                text:"S"
                font_name:"Lcd"
                font_size:"40dp"
                color:1,0,0,1
                halign: 'center'
                valign: 'middle'
                background_color:(0,0,0,1)
                canvas.before:
                    Color:
                        rgba:self.background_color
                    Rectangle:
                        size:self.size
                        pos:self.pos   
        ProgressBar:
            max:root.timer_totseconds
            value:root.timer_bar_value
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
                text_color: 1, 1, 1, 1
                on_press: root.timer_start()
                size_hint:0.25,0.3
                pos_hint:{"x":0.06,"y":0.5}
            MDRectangleFlatButton:
                text: 'Stop'
                text_color: 1, 1, 1, 1
                on_press: root.timer_stop()
                size_hint:0.25,0.3
                pos_hint:{"x":0.7,"y":0.5}
            MDRectangleFlatButton:
                text: 'Reset'
                text_color: 1, 1, 1, 1
                on_press: root.timer_reset()
                size_hint:0.25,0.3
                pos_hint:{"x":0.375,"y":0.5}
''')

class MainWidget(BoxLayout):
    timer_seconds = NumericProperty(0)
    timer_minutes = NumericProperty(0)
    timer_hours = NumericProperty(0)
    timer_total=NumericProperty()
    timer_totseconds=NumericProperty(0)
    timer_bar_value=NumericProperty(0)
    timer_drop_down=ListProperty()
    timer_click_start=BooleanProperty(False)
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        for i in range(60):
            self.timer_drop_down.append(str(i))

    def timer_increment_time(self, interval):
        self.timer_bar_value+=1
        if self.timer_minutes ==0 and self.timer_hours>0:
            self.timer_hours -= 1
            self.timer_minutes =60
            self.timer_seconds=0
        if self.timer_seconds==0 and self.timer_minutes>0:
            self.timer_minutes -= 1
            self.timer_seconds=60
        if self.timer_seconds==0 and self.timer_minutes ==0 and self.timer_hours==0:
            self.timer_reset()
            layout = BoxLayout(orientation="vertical")
            popup = Popup(title='TIME UP!',content=layout,size_hint=(None,None),size=("400dp","400dp"),auto_dismiss=False)
            popup.open()
            closeButton = Button(text="CLOSE TIMER!",size_hint=(1,None),size=(1,"40dp"))
            layout.add_widget(closeButton)
            sound = SoundLoader.load('alarm.wav')
            sound.loop = True
            sound.play()
            def timer_closepopup(args):
                popup.dismiss()
                self.timer_reset()
                sound.stop()
            closeButton.bind(on_press=timer_closepopup)
        self.timer_seconds -= 1

    def timer_start(self):
        self.timer_click_start=True
        Clock.unschedule(self.timer_increment_time)
        Clock.schedule_interval(self.timer_increment_time,1)

    def timer_stop(self):
        Clock.unschedule(self.timer_increment_time)

    def timer_reset(self):
        Clock.unschedule(self.timer_increment_time)
        self.timer_seconds = 0
        self.timer_minutes = 0
        self.timer_hours = 0
        self.timer_totseconds=0
        self.timer_bar_value=0
        self.timer_click_start=False

    def timer_second_selected(self,value):
        self.timer_seconds=value
        if self.timer_click_start==False:
            self.timer_totseconds+=value
    def timer_minutes_selected(self,value):
        self.timer_minutes=value
        if self.timer_click_start==False:
            self.timer_totseconds+=value*60
    def timer_hours_selected(self,value):
        self.timer_hours=value
        if self.timer_click_start==False:
            self.timer_totseconds += value * 3600
class TimeApp(MDApp):
    def build(self):
        return MainWidget()
TimeApp().run()
