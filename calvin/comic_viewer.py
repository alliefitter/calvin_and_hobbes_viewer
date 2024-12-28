from datetime import datetime
from importlib.resources import files
from time import sleep, time
from tkinter import Label, Tk

from PIL import ImageTk
from PIL.Image import open, Image
from PIL.ImageTk import PhotoImage

from calvin.db import DB
from calvin.util import get_comics_path

DATA = files("calvin.data")


class ComicViewer:
    def __init__(self):
        self.comics = get_comics_path()
        self.root = Tk()
        self.root.config(cursor="none")
        self.root.attributes("-fullscreen", True)
        self.db = DB()
        img = ImageTk.PhotoImage(
            self._set_background(self._scale_image(self.db.get_todays_comic()))
        )
        self.panel = Label(self.root, image=img, bg="#949494")
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.root.update()

    def get_todays_comic(self):
        comic = self.db.get_todays_comic()
        self._set_next_image(comic)

    def next_daily_comic(self):
        frames = [PhotoImage(file=str(DATA.joinpath(f'frame_{i}_delay-0.05s.gif'))) for i in range(6)]
        self.panel.pack_forget()
        self.panel = Label(self.root, bg="#949494")
        self.panel.pack(side="bottom", fill="both", expand="yes")
        for frame in frames * 10:
            self.panel.configure(image=frame)
            self.panel.image = frame
            self.panel.pack(side="bottom", fill="both", expand="yes")
            self.root.update()
            sleep(.05)

        comic = self.db.get_next_daily_comic()
        self._set_next_image(comic)

    def get_current_comic(self):
        comic = self.db.get_current_comic()
        self._set_next_image(comic)

    def next_comic(self):
        comic = self.db.get_next_comic()
        self._set_next_image(comic)

    def previous_comic(self):
        comic = self.db.get_previous_comic()
        self._set_next_image(comic)

    def get_comic(self, comic_date: str):
        comic = datetime.strptime(comic_date, "%Y-%m-%d").strftime("%Y%m%d")
        filename = f"{comic}.jpg"
        path = self.comics.joinpath(filename)
        if path.exists():
            self.db.set_cursor_to_comic(filename, "current")
            self._set_next_image(open(path))

    def start_arc(self, arc_name: str):
        start_comic = self.db.get_arc_start(arc_name)
        if start_comic:
            self._set_next_image(start_comic)

    @classmethod
    def _scale_image(cls, image: Image):
        width = 964
        height = int(image.height * (width / image.width))
        if height > 540:
            width = int(width * (540 / height))
            height = 540
        return image.resize((width, height))

    @classmethod
    def _set_background(cls, comic: Image) -> Image:
        x = int((1024 - comic.width) / 2)
        y = int((600 - comic.height) / 2)
        background = open(str(DATA.joinpath("textured_grey.jpg")))
        background.paste(comic, (x, y))

        return background

    def _set_next_image(self, comic: Image):
        image = ImageTk.PhotoImage(self._set_background(self._scale_image(comic)))
        self.panel.pack_forget()
        self.panel = Label(self.root, image=image, bg="#949494")
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.root.update()
