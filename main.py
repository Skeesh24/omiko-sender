import asyncio
import smtplib as sender
from ast import literal_eval
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading

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


prepare: dict = lambda msg: literal_eval(msg.decode("utf-8"))


def rabbitmq_queue_callback(ch, method, properties, body):
    send_email(**prepare(body))


def redis_queue_callback(body):
    send_email(**prepare(body))


async def main():
    print("[*] Starting service")
    print("[*] Initialization started")
    consumer = RedisConsumer(sett.BROKER_HOST)
    print("[*] Initialization ended")
    # create a task to run start_consuming asynchronously
    asyncio.create_task(consumer.start_consuming(redis_queue_callback))

    try:
        print("[*] consuming started")
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        consumer.stop_consuming()
        consumer.close()


if __name__ == "__main__":
    # create a new thread to run the event loop in
    loop_thread = threading.Thread(target=asyncio.run, args=(main(),))
    # start the thread
    loop_thread.start()
