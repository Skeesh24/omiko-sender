import pika
from redis import Redis

from interfaces import IConsumer
from settings import sett


class RedisConsumer(IConsumer):
    def __init__(self, host: str) -> None:
        self.connection = Redis.from_url(url=host)
        self.STOP_CONSUME = False

    def start_consuming(self, handler):
        """
        Start consuming a redis connection.
        This method is blocking
        """
        self.pubsub = self.connection.pubsub()
        self.pubsub.subscribe(**{sett.RECOVERY_QUEUE: handler})

        def consume():
            while not self.STOP_CONSUME:
                self.connection.lpop(sett.RECOVERY_QUEUE)
            self.STOP_CONSUME = False

        consume()

    def stop_consuming(self):
        self.STOP_CONSUME = True

    def close(self):
        self.connection.close()


class RabbitMQConsumer(IConsumer):
    def __init__(self, host: str) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
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
