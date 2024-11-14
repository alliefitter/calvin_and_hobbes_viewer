import click
from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion

from calvin.db import DB


@click.group()
def cli():
    pass


@cli.command()
def next_comic():
    client = Client(CallbackAPIVersion.VERSION2)
    client.connect("localhost", 1883, 60)
    client.loop_start()
    client.publish("next_comic")
    client.loop_stop()


@cli.command()
def current_comic():
    client = Client(CallbackAPIVersion.VERSION2)
    client.connect("localhost", 1883, 60)
    client.loop_start()
    client.publish("current_comic")
    client.loop_stop()


@cli.command()
@click.argument("comic_date")
def comic(comic_date: str):
    print(comic_date)
    client = Client(CallbackAPIVersion.VERSION2)
    client.connect("localhost", 1883, 60)
    client.loop_start()
    client.publish("comic", comic_date)
    client.loop_stop()


@cli.command()
def init_db():
    DB().init()


@cli.command()
def list_comics():
    list_()


if __name__ == '__main__':
    cli()
