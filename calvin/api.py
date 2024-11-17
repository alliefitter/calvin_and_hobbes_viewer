from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Depends

from calvin.db import DB, get_db
from calvin.publisher import Publisher, get_publisher

app = FastAPI()


@app.get("/comics")
def list_comics(db: Annotated[DB, Depends(get_db)]):
    return db.list_()


@app.post("/comics/next")
def next_comic(publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("next_comic")


@app.post("/comics/previous")
def previous_comic(publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("previous_comic")


@app.post("/comics/current")
def current_comic(publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("current_comic")


@app.post("/comics/arcs/{arc_name}")
def start_arc(arc_name: str, publisher: Annotated[Publisher, Depends(get_publisher)]):
    publisher.publish("start_arc", arc_name)


@app.post("/comics/{date}")
def comic(comic_date: str, publisher: Annotated[Publisher, Depends(get_publisher)]):
    parsed_date = datetime.strptime(comic_date, "%Y-%d-%m")
    publisher.publish("comic", parsed_date.strftime("%Y%d%m"))
