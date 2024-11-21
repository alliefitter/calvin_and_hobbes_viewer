from datetime import datetime
from importlib.resources import files
from typing import Annotated

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from calvin.db import DB, get_db
from calvin.publisher import Publisher, get_publisher
from calvin.util import get_comics_path

app = FastAPI()
COMICS = get_comics_path()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/comics")
def list_comics(db: Annotated[DB, Depends(get_db)]):
    return db.list_()


@app.get("/api/comics/image/{date}")
def get_image(date: datetime):
    filename = f"{date.strftime('%Y%m%d')}.jpg"
    return FileResponse(
        str(COMICS.joinpath(filename)), filename=filename, media_type="image/jpeg"
    )


@app.post("/api/comics/next", status_code=204)
def next_comic(publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("next_comic")


@app.post("/api/comics/today", status_code=204)
def get_todays_comic(publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("todays_comic")


@app.post("/api/comics/nextDaily", status_code=204)
def next_daily_comic(publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("next_daily_comic")


@app.post("/api/comics/previous", status_code=204)
def previous_comic(publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("previous_comic")


@app.post("/api/comics/current", status_code=204)
def current_comic(publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("current_comic")


@app.get("/api/comics/arcs")
def list_arcs(db: Annotated[DB, Depends(get_db)]) -> list[dict[str, str]]:
    return db.list_arcs()


@app.post("/api/comics/arcs/{arc_name}", status_code=204)
def start_arc(arc_name: str, publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("start_arc", arc_name)


@app.post("/api/comics/{comic_date}", status_code=204)
def comic(
    comic_date: datetime, publisher: Annotated[Publisher, Depends(get_publisher)]
):
    publisher.publish("comic", comic_date.strftime("%Y-%m-%d"))
