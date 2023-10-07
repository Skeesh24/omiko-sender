from abc import ABC, abstractclassmethod


class IBroker:
    @abstractclassmethod
    def connect(self, url: str):
        pass

    @abstractclassmethod
    def subscribe(self, queue_name: str, handle):
        pass

    @abstractclassmethod
    def get_message(self) -> bytes:
        pass
