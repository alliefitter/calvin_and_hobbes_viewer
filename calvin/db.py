import sqlite3
from importlib.resources import files
from os import listdir
from os.path import isfile, join
from pathlib import Path
from sqlite3 import Connection

from PIL import Image


class DB:
    def __init__(self):
        self.calvin = files("calvin")
        self.comics = self.calvin.joinpath("comics")
        self.db_path = Path(str(self.calvin.joinpath("comics.db")))

    @property
    def connection(self) -> Connection:
        return sqlite3.connect(str(self.db_path.absolute()))

    def init(self):
        if self.db_path.exists():
            self.db_path.unlink()

        cursor = self.connection.cursor()
        cursor.execute("create table comics (id integer primary key, filename string)")
        cursor.execute("create table position (id integer primary key, position integer)")
        comics = sorted([f for f in listdir('calvin/comics') if isfile(join('calvin/comics', f)) and f.endswith(".jpg")])
        cursor.executemany("insert into comics (filename) values (?)", [(c,) for c in comics])
        cursor.execute("insert into position (position) values (0)")
        cursor.connection.commit()
        cursor.connection.cursor()

    def list_(self):
        cursor = self.connection.cursor()
        print(cursor.execute("select * from comics").fetchall())

    def get_next_comic(self) -> Image:
        cursor = self.connection.cursor()
        result = cursor.execute("select position from position where id = 1")
        position, = result.fetchone()
        position += 1
        result = cursor.execute(f"select filename from comics where id = {position}")
        filename, = result.fetchone()
        cursor.execute(f"update position set position = {position}")
        cursor.connection.commit()
        cursor.connection.close()
        return Image.open(str(self.comics.joinpath(filename)))

    def get_current_comic(self) -> Image:
        cursor = self.connection.cursor()
        result = cursor.execute("select position from position where id = 1")
        position, = result.fetchone()
        result = cursor.execute(f"select filename from comics where id = {position}")
        filename, = result.fetchone()
        cursor.connection.close()
        return Image.open(str(self.comics.joinpath(filename)))

    def reset_position(self):
        cursor = self.connection
        cursor.execute('update position set position = 0')
        cursor.commit()
        self.connection.close()
