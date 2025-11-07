import sqlite3
from datetime import datetime
from importlib.resources import files
from os import listdir
from os.path import isfile, join
from pathlib import Path
from sqlite3 import Connection
from typing import Optional

import yaml
from PIL.Image import open as image_open, Image

from calvin.util import get_comics_path


class DB:
    def __init__(self):
        self.calvin = files("calvin")
        self.comics = get_comics_path()
        self.db_path = Path(str(self.calvin.joinpath("comics.db")))
        self.arcs = self.calvin.joinpath("data/arcs.yaml")

    @property
    def connection(self) -> Connection:
        return sqlite3.connect(str(self.db_path.absolute()))

    def init(self):
        if self.db_path.exists():
            self.db_path.unlink()
        with open(str(self.arcs), "r") as f:
            arcs: dict[str, int] = yaml.safe_load(f)

        cursor = self.connection.cursor()
        cursor.execute("create table comics (id integer primary key, filename string)")
        cursor.execute("create table arcs (name string, filename string)")
        cursor.execute("create table position (cursor_name string, position integer)")
        comics = sorted(
            [
                Path(str(f)).name
                for f in self.comics.iterdir()
                if f.is_file() and str(f).endswith(".jpg")
            ]
        )
        cursor.executemany(
            "insert into comics (filename) values (?)", [(c,) for c in comics]
        )
        cursor.executemany(
            "insert into arcs (name, filename) values (?, ?)",
            [(k, f"{str(v)}.jpg") for k, v in arcs.items()],
        )
        cursor.execute(
            "insert into position (cursor_name, position) values ('daily', 1)"
        )
        cursor.execute(
            "insert into position (cursor_name, position) values ('current', 1)"
        )
        cursor.connection.commit()
        cursor.connection.cursor()

    def list_(self):
        cursor = self.connection.cursor()
        rows = cursor.execute("select filename from comics").fetchall()

        return [r[0] for r in rows]

    def get_todays_comic(self) -> Image:
        return self._get_comic_for_cursor("daily")

    def get_next_daily_comic(self) -> Image:
        return self._increment_comic_for_cursor("daily")

    def get_current_comic(self) -> Image:
        return self._get_comic_for_cursor("current")

    def get_next_comic(self) -> Image:
        return self._increment_comic_for_cursor("current")

    def get_previous_comic(self) -> Image:
        return self._increment_comic_for_cursor("current", True)

    def get_arc_start(self, arc_name: str) -> Image | None:
        cursor = self.connection.cursor()
        result = cursor.execute(f"select filename from arcs where name = '{arc_name}'")
        row = result.fetchone()
        if row:
            (filename,) = row
            result = cursor.execute(
                f"select id from comics where filename = '{filename}'"
            )
            (position,) = result.fetchone()
            cursor.execute(
                f"update position set position = {position} where cursor_name = 'current'"
            )
            cursor.connection.commit()
            cursor.connection.close()
            return image_open(str(self.comics.joinpath(filename)))

        cursor.connection.close()
        return None

    def list_arcs(self) -> list[dict[str, str]]:
        cursor = self.connection.cursor()
        result = cursor.execute(f"select name, filename from arcs")
        rows = result.fetchall()
        cursor.connection.close()

        return [
            {
                "name": row[0],
                "date": datetime.strptime(row[1], "%Y%m%d.jpg").strftime("%Y-%m-%d"),
            }
            for row in rows
        ]

    def set_cursor_to_comic(self, filename: str, cursor_name: str):
        cursor = self.connection.cursor()
        result = cursor.execute(f"select id from comics where filename = '{filename}'")
        (position,) = result.fetchone()
        cursor.execute(
            f"update position set position = {position} where cursor_name = '{cursor_name}'"
        )
        cursor.connection.commit()
        cursor.connection.close()

    def _get_comic_for_cursor(self, cursor_name: str) -> Image:
        cursor = self.connection.cursor()
        result = cursor.execute(
            f"select position from position where cursor_name = '{cursor_name}'"
        )
        (position,) = result.fetchone()
        result = cursor.execute(f"select filename from comics where id = {position}")
        (filename,) = result.fetchone()
        cursor.connection.close()
        return image_open(str(self.comics.joinpath(filename)))

    def _increment_comic_for_cursor(
        self, cursor_name: str, decrement: bool = False
    ) -> Image:
        cursor = self.connection.cursor()
        result = cursor.execute("select max(id) from comics")
        (max_id,) = result.fetchone()
        result = cursor.execute(
            f"select position from position where cursor_name = '{cursor_name}'"
        )
        (position,) = result.fetchone()
        position = position - 1 if decrement else position + 1
        if position < 1:
            position = max_id
        elif position > max_id:
            position = 1

        result = cursor.execute(f"select filename from comics where id = {position}")
        (filename,) = result.fetchone()
        cursor.execute(
            f"update position set position = {position} where cursor_name = '{cursor_name}'"
        )
        cursor.connection.commit()
        cursor.connection.close()
        return image_open(str(self.comics.joinpath(filename)))

    def reset_daily(self):
        cursor = self.connection
        cursor.execute("update position set position = 1 where cursor_name = 'daily'")
        cursor.commit()
        self.connection.close()


def get_db() -> DB:
    return DB()
