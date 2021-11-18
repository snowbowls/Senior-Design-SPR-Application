import kivy
from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty


from kivy.loader import Loader

from kivy.clock import Clock

import time
import urllib.request
import numpy
import os

from kivy.network.urlrequest import UrlRequest
from functools import partial

from kivy_garden.graph import Graph, MeshLinePlot, BarPlot

from threading import Thread
from PIL import Image, ImageStat, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# If ESP is hosting
#   Name: I-SEE-YOU
#   Pass: yeetyeet
#   IP: 192.168.4.1

# capUrl = 'http://192.168.4.1/capture'
# capUrl = 'http://192.168.1.189/capture'
capUrl = 'https://www.neenahpaper.com/-/media/images/storefront/chips/environment-papers/environment-papers-ultra-bright-white-smooth.ashx'
capimg = kivy.uix.image.Image(source="images/capture.png")

times = []
sched_val = 0.265
ex_avg = 0
cap_cnt = 0
fps_val = 0


class ButtonTest(Widget):
    pass


def get_brightness_level():
    global levels
    while True:
        mx = 99
        if len(levels) >= 300:
            levels = []
        levels.append(mx)


def get_brightness():
    global levels
    im = Image.open("images\capture.png").convert('L')
    stat = ImageStat.Stat(im)
    if len(levels) >= 300:
        levels = []
    levels.append(stat.rms[0])
    print("--- %s bright ---" % stat.rms[0])


def imagegrabhandler(self, *args):
    start = time.time()
    imagegrab(self, start)
    update(self)


def imagegrab(self, start, *args):
    global cap_cnt
    global ex_avg
    global fps_val

    urllib.request.urlretrieve(
        capUrl, "images\capture.png")

    times.append(time.time() - start)
    print("--- %s seconds ---" % (times[-1]))

    cap_cnt += 1
    ex_avg = numpy.format_float_positional(numpy.mean(times), precision=5)
    fps_val = numpy.format_float_positional(1 / (numpy.mean(times) + sched_val), precision=2)

    get_brightness()


def update(self):
    capimg.reload()


class LayoutTest(BoxLayout):
    your_time = StringProperty()
    img = ObjectProperty()

    count = StringProperty()
    exavg = StringProperty()
    fps = StringProperty()
    exint = StringProperty()
    highinten = StringProperty()
    lowinten = StringProperty()

    isShownStats = BooleanProperty(True)
    isShownMenu = BooleanProperty(False)
    isCapture = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(LayoutTest, self).__init__(**kwargs)

        self.orientation = "vertical"

        self.padding = 10

        self.img.source = "images\default.png"

        self.plot = MeshLinePlot(color=[1, 0, 0, 1])

        Clock.schedule_interval(self.set_time, 0.1)

    def experiment(self):
        pass

    def start_capture(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.325)

        imagegrabhandler(self)
        Clock.schedule_interval(imagegrabhandler, sched_val)
        Clock.schedule_once(self.switch, sched_val + 0.1)
        Clock.schedule_interval(self.refresh, sched_val)
        Clock.schedule_interval(self.stat, 0.5)

    def stop_capture(self):
        self.switch(0)
        # WOOOOOEE THERE, maybe don't use these slow methods
        Clock.unschedule(imagegrabhandler)
        Clock.unschedule(self.refresh)
        Clock.unschedule(self.get_value)
        Clock.unschedule(self.stat)

    def stat(self, dt):
        self.count = str(cap_cnt)
        self.exavg = str(ex_avg)
        self.fps = str(fps_val)
        self.exint = str(sched_val)

    def get_value(self, dt):
        self.plot.points = [(i/2, j) for i, j in enumerate(levels)]

        self.highinten = str(max(levels))
        self.lowinten = str(min(levels))

    def set_time(self, dt):
        self.your_time = time.strftime("%m/%d/%Y  -  %I:%M %p")

    def switch(self, val):

        if val:
            self.img.source = "images\capture.png"
        else:
            self.img.source = "images\default.png"

    def refresh(self, bruh_why_am_i_here):
        self.img.reload()

    def clear_values(self):
        global levels
        levels = []
        self.plot.points = [(i / 2, j) for i, j in enumerate(levels)]
        self.count = str(0)
        self.exavg = str(0)
        self.fps = str(0)
        self.exint = str(0)
        self.lowinten = str(0)
        self.highinten = str(0)


class FASSPRApp(App):
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

## --------------------------------------------------------------------------------------------------------------------

import itertools

from kivy.utils import get_color_from_hex as rgb

colors = itertools.cycle([rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')])


class SASSPRRoot(BoxLayout):
    img = ObjectProperty()

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def showtest(self):
        self.clear_widgets()
        self.img = Testy()
        self.add_widget(self.img)


class Testy(BoxLayout):
    ree = ObjectProperty


class List(BoxLayout):
    but = ObjectProperty()


class Main(Screen):
    img = ObjectProperty()
    isShownMenu = BooleanProperty(False)
    isShownStats = BooleanProperty(True)
    isCaptureOn = BooleanProperty(False)
    isShownGraph = BooleanProperty(False)

    your_time = StringProperty()

    count = StringProperty()
    exavg = StringProperty()
    fps = StringProperty()
    exint = StringProperty()


    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.img.source = "images\default.png"

    def reset_plots(self, graph):
        for plot in self.plot:
            plot.bind_to_graph(graph)
            plot.points = []

    def start_capture(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.325)

        imagegrabhandler(self)
        Clock.schedule_interval(imagegrabhandler, sched_val)
        Clock.schedule_once(self.switch, sched_val + 0.1)
        Clock.schedule_interval(self.refresh, sched_val)
        Clock.schedule_interval(self.stat, 0.5)

    def stop_capture(self):
        self.switch(0)
        # WOOOOOEE THERE, maybe don't use these slow methods
        Clock.unschedule(imagegrabhandler)
        Clock.unschedule(self.refresh)
        Clock.unschedule(self.get_value)
        Clock.unschedule(self.stat)

    def stat(self, dt):
        self.count = str(cap_cnt)
        self.exavg = str(ex_avg)
        self.fps = str(fps_val)
        self.exint = str(sched_val)

    def switch(self, val):

        if val:
            self.img.source = "images\capture.png"
        else:
            self.img.source = "images\default.png"

    def refresh(self, bruh_why_am_i_here):
        self.img.reload()

    def get_value(self, dt):
        self.plot.points = [(i/2, j) for i, j in enumerate(levels)]


class FASSPRApp(App):
    def build(self):
        return LayoutTest()


if __name__ == '__main__':
    levels = []
    # get_level_thread = Thread(target=get_brightness_level)
    # get_level_thread.daemon = True
    FASSPRApp().run()
