#!/usr/bin/env python
import pika
from logger import logger
class Sender:
    def __init__(self, host,user,pw,queue):
        credentials = pika.PlainCredentials(user, pw)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,credentials=credentials))
        self.channel = self.connection.channel()
        self.queue=self.channel.queue_declare(queue, durable=True)
        self.queue_name=queue
    def send_msg(self,msg):
        self.channel.basic_publish(exchange='',
                            routing_key=self.queue_name,
                            body=msg,
                            properties=pika.BasicProperties(
                                delivery_mode=2,  # make message persistent
                            ))
    def close(self):
        self.connection.close()
    def get_msg_count(self):
        return self.queue.method.message_count

if __name__ == "__main__":
    send=Sender('154.223.179.149','worker','hello','task_queue')
    for i in range(2):
        send.send_msg(str(i))
    send.close()