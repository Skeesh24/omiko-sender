from redis import Redis

from interface import IBroker


class RedisBroker(IBroker):
    def connect(self, url: str):
        self.connection = Redis.from_url(url)

    def subscribe(self, queue_name: str, handler):
        self.queue_name = queue_name
        self.connection.pubsub().subscribe(**{queue_name: handler})

    def get_message(self):
        self.connection.lpop(self.queue_name)
