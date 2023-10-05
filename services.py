import asyncio

import pika
import redis

from interfaces import IConsumer
from settings import sett


class RedisConsumer(IConsumer):
    async def __init__(self, host: str) -> None:
        self.connection = redis.from_url(host)
        self.STOP_CONSUME = False

    async def start_consuming(self, handler):
        """
        Start consuming a redis connection.
        This method is blocking
        """
        self.pubsub = self.connection.pubsub()
        self.pubsub.subscribe(**{sett.RECOVERY_QUEUE: handler})

        async def consume():
            while not self.STOP_CONSUME:
                message = self.pubsub.get_message()
                if message and message["type"] == "message":
                    payload = message["data"]
                    handler(payload)

            self.STOP_CONSUME = False

        loop = asyncio.get_event_loop()
        return await loop.run_until_complete(consume)

    async def stop_consuming(self):
        self.STOP_CONSUME = True

    async def close(self):
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
