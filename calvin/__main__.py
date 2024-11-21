from datetime import datetime
from calvin import daemon

import httpx
import uvicorn
from typer import Typer

from calvin.db import DB

app = Typer()


@app.command()
def next_daily_comic():
    httpx.post("http://localhost:8000/api/comics/nextDaily")


@app.command()
def next_comic():
    httpx.post("http://localhost:8000/api/comics/next")


@app.command()
def previous_comic():
    httpx.post("http://localhost:8000/api/comics/previous")


@app.command()
def current_comic():
    httpx.post("http://localhost:8000/api/comics/current")


@app.command()
def get_comic(comic_date: datetime):
    httpx.post(f"http://localhost:8000/api/comics/{comic_date.strftime('%Y%m%d')}")


@app.command()
def start_arc(arc_name: str):
    httpx.post(f"http://localhost:8000/api/comics/arcs/{arc_name}")


@app.command()
def list_arcs():
    response = httpx.post("http://localhost:8000/api/comics/arcs")
    arcs = response.json()
    arc_list = []
    for arc in arcs:
        arc_list.append(
            f"{arc['name']}: {datetime.strptime(arc['filename'], '%Y%m%d.jpg').strftime('%Y-%m-%d')}"
        )
    print("\n".join(arc_list))


@app.command()
def init_db():
    DB().init()


@app.command()
def list_comics():
    response = httpx.post("http://localhost:8000/api/comics")
    for comic in response.json():
        print(comic)


@app.command()
def run_server():
    uvicorn.run("calvin.api:app", host="0.0.0.0", port=8000, reload=False)


@app.command()
def run_daemon():
    daemon.main()


if __name__ == "__main__":
    app()
