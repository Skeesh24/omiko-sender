import pika
from redis import Redis

from interfaces import IConsumer


class RedisConsumer(IConsumer):
    def __init__(self, host: str) -> None:
        self.__connection = Redis.from_url(url=host)
        self.STOP_CONSUME = False

    def prepare_consuming(self, handler, queue_name: str) -> None:
        """
        Prepare to consume the redis connection.
        """
        self.pubsub = self.__connection.pubsub()
        self.pubsub.subscribe(**{queue_name: handler})

        # def consume():
        #     while not self.STOP_CONSUME:
        #         message = self.pubsub.get_message()
        #         if message and message["type"] == "message":
        #             payload = message["data"]
        #             handler(payload)

        #     self.STOP_CONSUME = False

        # consume()

    def get_channel(self):
        return self.__connection

    def close(self) -> None:
        self.__connection.close()


class RabbitMQConsumer(IConsumer):
    def __init__(self, host: str) -> None:
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.__channel = self.__connection.channel()

    def prepare_consuming(self, handler, queue_name: str) -> None:
        self.__channel.queue_declare(queue_name)
        self.__channel.basic_consume(
            queue_name, on_message_callback=handler, auto_ack=True
        )
    
    def get_channel(self):
        return self.__channel

    def close(self) -> None:
        self.__connection.close()
