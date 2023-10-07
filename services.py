import pika
from redis import Redis

from interface import IBroker


class RedisBroker(IBroker):
    def connect(self, url: str) -> None:
        self.connection = Redis.from_url(url)

    def subscribe(self, queue_name: str, handler) -> None:
        self.queue_name = queue_name
        self.connection.pubsub().subscribe(**{queue_name: handler})

    def get_message(self) -> bytes:
        return self.connection.rpop(self.queue_name)


class RabbitMQBroker(IBroker):
    def connect(self, url: str) -> None:
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host=url))
        self.__channel = self.__connection.channel()

    def subscribe(self, queue_name: str, handler) -> None:
        self.queue_name = queue_name
        self.__channel.queue_declare(queue_name)
        self.__channel.basic_consume(
            queue_name, on_message_callback=handler, auto_ack=True
        )

    def get_message(self) -> bytes:
        message = self.__channel.basic_get(self.queue_name)
        if all(message):
            return None
        return message[2]
