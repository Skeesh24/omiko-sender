from abc import ABC, abstractclassmethod


class IConsumer(ABC):
    @abstractclassmethod
    def start_consuming(self, handler: function) -> None:
        pass

    @abstractclassmethod
    def stop_consuming(self) -> None:
        pass

    @abstractclassmethod
    def close(self) -> None:
        pass
