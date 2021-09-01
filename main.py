import kivy
from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label

from kivy.properties import StringProperty
from kivy.properties import  ObjectProperty

from kivy.loader import Loader

from kivy.clock import Clock

import time
import urllib.request
import numpy
import os

from kivy.network.urlrequest import UrlRequest
from functools import partial

# capUrl = 'http://192.168.1.189/capture'
capUrl = 'https://image.shutterstock.com/image-vector/default-word-digital-style-glowing-600w-1668796114.jpg'
capimg = Image(source="images/capture.png")

times = []
cap_avg = 0
cap_cnt = 0


class ButtonTest(Widget):
    pass


def imagegrabhandler(self, *args):
    start = time.time()
    imagegrab(self, start)
    update(self)


def imagegrab(self, start, *args):
    global cap_cnt
    global cap_avg

    urllib.request.urlretrieve(
        capUrl, "images\capture.png")

    times.append(time.time() - start)
    print("--- %s seconds ---" % (times[-1]))

    cap_cnt += 1
    cap_avg = numpy.mean(times)


def update(self):
    capimg.reload()


class LayoutTest(BoxLayout):
    your_time = StringProperty()
    img = ObjectProperty()

    count = StringProperty()
    capavg = StringProperty()

    def __init__(self, **kwargs):
        super(LayoutTest, self).__init__(**kwargs)

        self.orientation = "vertical"

        self.padding = 10

        self.img.source = "images\default.png"

        Clock.schedule_interval(self.set_time, 0.1)
        Clock.schedule_interval(self.stat, 0.5)

    def start_capture(self):
        imagegrabhandler(self)
        Clock.schedule_interval(imagegrabhandler, 0.5)
        Clock.schedule_once(self.switch, 0.6)
        Clock.schedule_interval(self.refresh, 0.5)

    def stop_capture(self):
        self.switch(0)
        # WOOOOOEE THERE, maybe don't use these slow methods
        Clock.unschedule(imagegrabhandler)
        Clock.unschedule(self.refresh)

    def stat(self, dt):
        self.count = str(cap_cnt)
        self.capavg = str(cap_avg)

    def set_time(self, dt):
        self.your_time = time.strftime("%m/%d/%Y  -  %I:%M %p")

    def switch(self, val):

        if val:
            self.img.source = "images\capture.png"
        else:
            self.img.source = "images\default.png"

    def refresh(self, bruh_why_am_i_here):
        self.img.reload()


class DooDadApp(App):
    def build(self):
        root = LayoutTest()

        # root.add_widget(ButtonTest())
        # ImageTest().sched()
        return root

    def run_cap(self, *args):
        for i in range(10):
            r = UrlRequest("http://192.168.1.189/capture", on_success=partial(self.update_label, i))
            print(i)

    def update_label(self, i, *args):
        print(i)


if __name__ == '__main__':
    DooDadApp().run()