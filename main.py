import smtplib as sender
from ast import literal_eval
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from services import RabbitMQConsumer, RedisConsumer
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


initialize = lambda host: RedisConsumer(host=host)

consumer = initialize(sett.BROKER_HOST)
consumer.start_consuming(queue_callback)


try:
    print("[*] consuming started")
    consumer.start_consuming()
except KeyboardInterrupt:
    print("Interrupted")
    consumer.stop_consuming()
    consumer.close()
