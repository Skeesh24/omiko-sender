import smtplib as sender
from ast import literal_eval
from asyncio import run
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ
from threading import Thread

from redis import Redis


def send_email(to: str, subject: str, msg: str) -> None:
    with sender.SMTP(environ.get("SENDER_HOST"), environ.get("SENDER_PORT")) as server:
        server.starttls()
        server.login(environ.get("SENDER_USERNAME"), environ.get("SENDER_ACC"))

        message = MIMEMultipart()
        message["From"] = environ.get("SENDER_FROM")
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(msg, "html"))

        server.sendmail(environ.get("SENDER_FROM"), to, message.as_string())
        server.quit()


def queue_callback(body):
    send_email(**literal_eval(body.decode("utf-8")))
    print("email sent")


async def consuming(connection):
    while True:
        message = connection.lpop(environ.get("RECOVERY_QUEUE"))
        if message: queue_callback(message)


def unblocking_run(connection):
    run(consuming(connection))


if __name__ == "__main__":
    print("connect to the broker...")
    connection: Redis = Redis.from_url(url=environ.get("BROKER_HOST"))
    print("connection passed")
    q_name = environ.get("RECOVERY_QUEUE")
    print("queue declaration")
    connection.pubsub().subscribe(**{q_name: queue_callback})
    print("subscribed")
    print("consume initialized")
    Thread(target=unblocking_run, args=(connection,)).start()
