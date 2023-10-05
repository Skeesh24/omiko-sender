import smtplib as sender
from os import environ
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ast import literal_eval
import pika
from os import environ

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
    send_email(**literal_eval(body.decode("utf-8").replace("`", '"')))

connection = pika.BlockingConnection(pika.ConnectionParameters(host=sett.BROKER_HOST))
channel = connection.channel()
q_name = sett.RECOVERY_QUEUE
channel.queue_declare(q_name)
channel.basic_consume(q_name, on_message_callback=queue_callback, auto_ack=True)

try:
    print("[*] consuming started")
    channel.start_consuming()
except KeyboardInterrupt:
    print("Interrupted")
    channel.stop_consuming()
    connection.close()
