#!/usr/bin/env python
import pika, sys, os
import random
import datetime
import orjson

# Created by following https://www.rabbitmq.com/tutorials/tutorial-one-python.html
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        message = orjson.loads(body.decode())

        message['timestamp'] = datetime.datetime.fromisoformat(message['timestamp'])
        message['latency'] = datetime.datetime.now() - message['timestamp']

        print(f"count: {message['count']}, latency: {message['latency']}. timestamp: {message['timestamp']}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)