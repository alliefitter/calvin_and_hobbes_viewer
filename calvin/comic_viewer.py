from importlib.resources import files
from tkinter import Label, Tk

from PIL import ImageTk, Image

from calvin.db import DB


class ComicViewer:
    def __init__(self):
        self.comics = files("calvin.comics")
        self.root = Tk()
        self.root.config(cursor="none")
        self.root.attributes("-fullscreen", True)
        self.db = DB()
        img = ImageTk.PhotoImage(self._scale_image(self.db.get_next_comic()))
        self.panel = Label(self.root, image=img, bg='#949494')
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.root.update()
    
    def next_comic(self):
        print("next image")
        comic = self.db.get_next_comic()
        img = ImageTk.PhotoImage(self._scale_image(comic))
        self.panel.pack_forget()
        self.panel = Label(self.root, image=img, bg='#949494')
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.root.update()

    def get_current_comic(self):
        comic = self.db.get_current_comic()
        img = ImageTk.PhotoImage(self._scale_image(comic))
        self.panel.pack_forget()
        self.panel = Label(self.root, image=img, bg='#949494')
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.root.update()

    def get_comic(self, comic: str):
        img = ImageTk.PhotoImage(self._scale_image(Image.open(str(self.comics.joinpath(f"{comic}.jpg")))))
        self.panel.pack_forget()
        self.panel = Label(self.root, image=img, bg='#949494')
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.root.update()

    @classmethod
    def _scale_image(cls, image: Image):
        width = 964
        height = int(image.height * (width / image.width))
        if height > 540:
            width = int(width * (540 / height))
            height = 540
        return image.resize((width, height))