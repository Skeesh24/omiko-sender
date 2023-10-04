import smtplib as sender
from os import environ
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ast import literal_eval
import pika
from os import environ


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


def queue_callback(ch, method, properties, body):
    send_email(**literal_eval(body.decode("utf-8").replace("`", '"')))
    print("email sent")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=environ.get("BROKER_HOST")))
print("connection passed")
channel = connection.channel()
q_name = environ.get("RECOVERY_QUEUE")
channel.queue_declare(q_name)
print("queue declaration")
channel.basic_consume(q_name, on_message_callback=queue_callback, auto_ack=True)
print("consume initialized")

try:
    print("[*] consuming started")
    channel.start_consuming()
except KeyboardInterrupt:
    print("Interrupted")
    channel.stop_consuming()
    connection.close()
