from abc import ABC, abstractclassmethod


class IConsumer(ABC):
    @abstractclassmethod
    def prepare_consuming(self, handler, queue_name: str) -> None:
        pass

    @abstractclassmethod
    def get_channel(self):
        pass

    @abstractclassmethod
    def close(self) -> None:
        pass
