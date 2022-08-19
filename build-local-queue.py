#!/usr/bin/env python3
import pika
import os
import rabbit
import config as cfg

r = rabbit.Rabbit()

try:
    r.connect()
    dirs = os.listdir(cfg.DATA_PATH)
    for file in dirs:
        print(" [ ] Sending message " + file)
        in_file = open(cfg.DATA_PATH + '/' + file)
        r.send(cfg.EXCHANGE_NAME,
               cfg.ROUTING_KEY,
               cfg.QUEUE_NAME,
               in_file.read())
    r.close()
    print(" All text data sent")

except Exception as e:
    print("Error sending data :(")
    print(e)
