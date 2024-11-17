from types import TracebackType

from paho.mqtt.client import Client
from paho.mqtt.enums import CallbackAPIVersion


class Publisher:
    client: Client

    def __enter__(self):
        self.connect()
        return self

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        self.close()
        if value:
            raise value

        return True

    def connect(self):
        self.client = Client(CallbackAPIVersion.VERSION2)
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()

    def close(self):
        self.client.loop_stop()

    def publish(self, topic: str, message: str | None = None):
        self.client.publish(topic, message)


async def get_publisher():
    publisher = Publisher()
    publisher.connect()
    try:
        yield publisher

    finally:
        publisher.close()
