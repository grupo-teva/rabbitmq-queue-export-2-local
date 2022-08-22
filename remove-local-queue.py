#!/usr/bin/env python3
import pika
import sys
import rabbit
import config as cfg

r = rabbit.Rabbit()

try:
    queue_name = ''.join(sys.argv[1:]) or cfg.QUEUE_NAME
    r.remove_queue(queue_name)

except Exception as e:
    print("Error deleting queue :(")
    print(e)
