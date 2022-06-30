#!/usr/bin/env python
import pika
import random
import datetime
import orjson
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

dataToSend = f'{random.getrandbits(400000):=032b}'
count = 0

while True:
    messageToSend = orjson.dumps({"count": count, "data": dataToSend, "timestamp": datetime.datetime.now()})
    count = count + 1
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=messageToSend)
    print("Messages Published: " + str(count))
    time.sleep(0.2)

#print(" [x] Sent 'Hello World!'")

connection.close()