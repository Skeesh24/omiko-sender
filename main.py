import smtplib as sender
from ast import literal_eval
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pika

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


def queue_callback(ch, method, properties, body):
    prepare: dict = lambda msg: literal_eval(msg.decode("utf-8"))

    send_email(**prepare(body))


def initialize():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=sett.BROKER_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(sett.RECOVERY_QUEUE)
    channel.basic_consume(
        sett.RECOVERY_QUEUE, on_message_callback=queue_callback, auto_ack=True
    )
    return connection, channel


connection, channel = initialize()

try:
    print("[*] consuming started")
    channel.start_consuming()
except KeyboardInterrupt:
    print("Interrupted")
    channel.stop_consuming()
    connection.close()
