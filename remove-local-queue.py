#!/usr/bin/env python3
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_delete(queue='reindex')
connection.close()
