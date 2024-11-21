import os
from pathlib import Path


def get_comics_path() -> Path:
    if "COMICS_PATH" not in os.environ:
        raise ValueError("Missing required environment variable COMICS_PATH")

    comics = Path(os.environ["COMICS_PATH"])
    if not comics.exists():
        raise ValueError(f"COMICS_PATH does not exist, {comics.absolute()}")

    return comics
