# wrappings for pushing into the queue, rabbitMQ, we are using amqp protocol
import pika

# for the sleep on the callback
import time
import logging

###############################################################################
#                  Begin of Logging block
###############################################################################
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler() # Log for display
f_handler = logging.FileHandler('test.log', mode='a') # Log for file
formattc = logging.Formatter('[%(asctime)s](%(levelname)s %(name)s) eBot: %(message)s',
                             datefmt='%d%m%y-%H:%M:%S')
formattf = logging.Formatter('[%(asctime)s](%(levelname)s %(name)s) eBot: %(message)s',
                             datefmt='%d%m%y-%H:%M:%S')
c_handler.setFormatter(formattc)
f_handler.setFormatter(formattf)
logger.setLevel(logging.DEBUG)
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.info('queue module loaded!')
###############################################################################
#                  End of Logging block
###############################################################################

class Queue(object):

    def __init__(self, amqp_url, queue_name):
        self.queue_name = queue_name
        self.parameters = pika.URLParameters(amqp_url)
        self.connection = None
        self.channel = None
        self.exchange = ''

    def connect(self):
        self.connection = pika.BlockingConnection(self.parameters)

    def create_channel(self):
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=20)
        return self.channel

    def callback(ch, method, properties, body):
        logger.debug(" [x] Received %r" % body)
        time.sleep(body.count(b'.'))
        logger.debug(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def get_message_from_channel(self, channel):
        method_frame, header_frame, body = channel.basic_get(queue=self.queue_name)
        message = str(body.decode('utf8', 'strict')) 
        return message, method_frame, header_frame, body

    def publish_message(self, channel, message_body):
        channel.basic_publish(exchange=self.exchange, routing_key=self.queue_name, body=message_body)

    def parameters(self):
        return self.parameters

    def connection(self):
        return self.connection

    def close_connection(self):
        return self.connection.close()

    def return_basic_nack(self, delivery_tag):
        return self.channel.basic_nack(delivery_tag=delivery_tag, requeue=True)
