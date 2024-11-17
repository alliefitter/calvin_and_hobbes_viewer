from functools import partial
from typing import Any

from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion

from calvin.comic_viewer import ComicViewer


def on_connect(client: Client, *args):
    client.subscribe("comic")
    client.subscribe("next_daily_comic")
    client.subscribe("current_comic")
    client.subscribe("start_arc")
    client.subscribe("next_comic")
    client.subscribe("previous_comic")


def on_message(viewer: ComicViewer, client: Client, userdata: Any, msg: MQTTMessage):
    print(f"Received {msg.topic}")
    match msg.topic:
        case "next_daily_comic":
            viewer.next_daily_comic()

        case "next_comic":
            viewer.next_comic()

        case "previous_comic":
            viewer.previous_comic()

        case "comic":
            viewer.get_comic(msg.payload.decode("utf-8"))

        case "start_arc":
            viewer.start_arc(msg.payload.decode("utf-8"))

        case "current_comic":
            viewer.get_current_comic()


def main():
    viewer = ComicViewer()
    client = Client(CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = partial(on_message, viewer)

    client.connect("localhost", 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
