#!/usr/bin/env python3
import pika
import os

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='lectura.sicadiz')
dirs = os.listdir('data')
for file in dirs:
    txt = open('data/' + file)
    channel.basic_publish(exchange='exchange.databridge',
                          routing_key='lectura',
                          body=txt.read())
    print(" [x] Sent " + file)
connection.close()
