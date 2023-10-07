import smtplib as sender
from ast import literal_eval
from asyncio import run
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

from interface import IBroker
from services import RedisBroker
from settings import sett


def send_email(to: str, subject: str, msg: str) -> None:
    with sender.SMTP(sett.SENDER_HOST, sett.SENDER_PORT) as server:
        server.starttls()
        server.login(sett.SENDER_USERNAME, sett.SENDER_ACC)

        message = MIMEMultipart()
        message["From"] = sett.SENDER_FROM
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(msg, "html"))

        server.sendmail(sett.SENDER_FROM, to, message.as_string())
        server.quit()


def queue_callback(body: bytes) -> None:
    send_email(**literal_eval(body.decode("utf-8")))
    print("email sent")


async def consuming(connection: IBroker):
    while True:
        message = connection.get_message()
        if message:
            queue_callback(message)


def unblocking_run(connection: IBroker):
    run(consuming(connection))


if __name__ == "__main__":
    print("connect to the broker...")
    consumer = RedisBroker()
    consumer.connect(sett.BROKER_HOST)
    print("connection passed")

    print("queue declaration")
    consumer.subscribe(sett.RECOVERY_QUEUE, queue_callback)
    print("subscribed")

    print("consume initialized")
    Thread(target=unblocking_run, args=(consumer,)).start()
