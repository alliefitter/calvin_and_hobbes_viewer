from importlib.resources import files
from itertools import count
from tkinter import Label

from PIL import Image
from PIL.ImageTk import PhotoImage

DATA = files("calvin.data")


class WhiteNoiseLabel(Label):
    location: int
    delay: int
    frames: list[PhotoImage]

    def load(self):
        im = Image.open(str(DATA.joinpath("white_noise.gif")))
        self.location = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']

        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = []

    def next_frame(self):
        if self.frames:
            self.location += 1
            self.location %= len(self.frames)
            self.config(image=self.frames[self.location])
            self.after(self.delay, self.next_frame)
