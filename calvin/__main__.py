from datetime import datetime

import click
import uvicorn
from click import DateTime, STRING

from calvin.db import DB
from calvin.publisher import Publisher


@click.group()
def cli():
    pass


@cli.command()
def next_daily_comic():
    with Publisher() as publisher:
        publisher.publish("next_daily_comic")


@cli.command()
def next_comic():
    with Publisher() as publisher:
        publisher.publish("next_comic")


@cli.command()
def previous_comic():
    with Publisher() as publisher:
        publisher.publish("previous_comic")


@cli.command()
def current_comic():
    with Publisher() as publisher:
        publisher.publish("current_comic")


@cli.command()
@click.argument("comic_date", type=DateTime(["%Y-%m-%d"]))
def comic(comic_date: datetime):
    with Publisher() as publisher:
        publisher.publish("comic", comic_date.strftime("%Y%d%m"))


@cli.command()
@click.argument("arc_name", type=STRING)
def start_arc(arc_name: str):
    with Publisher() as publisher:
        publisher.publish("start_arc", arc_name)


@cli.command()
def list_arcs():
    arcs = DB().list_arcs()
    arc_list = []
    for arc in arcs:
        arc_list.append(
            f"{arc['name']}: {datetime.strptime(arc['filename'], '%Y%m%d.jpg').strftime('%Y-%m-%d')}"
        )
    print("\n".join(arc_list))


@cli.command()
def init_db():
    DB().init()


@cli.command()
def list_comics():
    list_()


@cli.command()
def run_server():
    uvicorn.run("calvin.api:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    cli()
