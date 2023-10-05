import pika
from redis import Redis

from interfaces import IConsumer
from settings import sett


class RedisConsumer(IConsumer):
    def __init__(self, host: str) -> None:
        self.connection = Redis.from_url(url=host)

    def start_consuming(self, handler):
        pubsub = self.connection.pubsub()
        self.pubsub = pubsub
        pubsub.subscribe(**{sett.RECOVERY_QUEUE: handler})

    def stop_consuming(self):
        self.pubsub.unsubscribe()

    def close(self):
        self.connection.close()


class RabbitMQConsumer(IConsumer):
    def __init__(self, host: str) -> None:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()

    def start_consuming(self, handler):
        self.channel.queue_declare(sett.RECOVERY_QUEUE)
        self.channel.basic_consume(
            sett.RECOVERY_QUEUE, on_message_callback=handler, auto_ack=True
        )
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()

    def close(self):
        self.connection.close()
