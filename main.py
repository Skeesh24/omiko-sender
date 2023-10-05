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


def rabbitmq_queue_callback(ch, method, properties, body):
    send_email(**prepare(body))


def redis_queue_callback(body):
    send_email(**prepare(body))


if __name__ == "__main__":
    print("[*] Starting service")
    prepare: dict = lambda msg: literal_eval(msg.decode("utf-8"))
    initialize = lambda host: RedisConsumer(host=host)
    print("[*] Initialization started")
    consumer = initialize(sett.BROKER_HOST)
    print("[*] Initialization ended")

    try:
        print("[*] consuming started")
        consumer.start_consuming(redis_queue_callback)
    except KeyboardInterrupt:
        print("Interrupted")
        consumer.stop_consuming()
        consumer.close()
