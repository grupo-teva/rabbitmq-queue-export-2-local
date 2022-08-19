import pika
import config as cfg
 
class Rabbit():
    def __init__(self):
        self.conn = None
        self.channel = None
 
    def connect(self):
        credentials = pika.PlainCredentials(cfg.USER_NAME,
                                            cfg.USER_PASSWD)
        parameters = pika.ConnectionParameters(cfg.RABBIT_HOST,
                                               cfg.RABBIT_PORT,
                                               cfg.VIRTUAL_HOST,
                                               credentials)
        self.conn = pika.BlockingConnection(parameters)
        self.channel = self.conn.channel()

    def close(self):
        self.conn.close()

    def remove_queue(self, queue_name):
        self.connect()
        self.channel.queue_delete(queue=queue_name)
        print(" [x] Queue " + queue_name + " terminated")
        self.close()

    def send(self, exchange_name, routing_key, queue_name, data):
        self.channel.exchange_declare(exchange=exchange_name,
                                      exchange_type='direct')
        self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange=exchange_name,
                                queue=queue_name,
                                routing_key=routing_key)
        self.channel.basic_publish(exchange=exchange_name,
                                   routing_key=routing_key,
                                   body=data)
        print(" [x] Sent data to RabbitMQ")

    def send_one(self, exchange_name, routing_key, queue_name, data):
        self.connect()
        self.channel.exchange_declare(exchange=exchange_name,
                                      exchange_type='direct')
        self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange=exchange_name,
                                queue=queue_name,
                                routing_key=routing_key)
        self.send(exchange_name, routing_key, queue_name, data)
        print(" [x] Sent data to RabbitMQ")
        self.close()
