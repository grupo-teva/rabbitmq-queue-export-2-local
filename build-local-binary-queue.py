#!/usr/bin/env python3
import pika
import os
import rabbit
import config as cfg

r = rabbit.Rabbit()

try:
    r.connect()
    entries = os.scandir(cfg.DATA_PATH)
    for file in entries:
        if file.name == '.gitignore':
            continue
        print(" Sending binary message " + file.name)
        in_file = open(cfg.DATA_PATH + '/' + file.name, "rb")
        data = in_file.read()
        r.send(cfg.EXCHANGE_NAME,
               cfg.ROUTING_KEY,
               cfg.QUEUE_NAME,
               data)
    r.close()
    print(" All binary data sent")

except Exception as e:
    print("Error sending data :(")
    print(e)
