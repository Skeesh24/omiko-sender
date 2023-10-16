from dataclasses import dataclass
from os import environ

env = lambda key: environ.get(key)


@dataclass
class sett:
    SENDER_HOST: str = env("SENDER_HOST")
    SENDER_PORT: str = env("SENDER_PORT")
    SENDER_USERNAME: str = env("SENDER_USERNAME")
    SENDER_ACC: str = env("SENDER_ACC")
    SENDER_FROM: str = env("SENDER_FROM")
    RECOVERY_QUEUE: str = env("RECOVERY_QUEUE")
    BROKER_HOST: str = env("BROKER_HOST")