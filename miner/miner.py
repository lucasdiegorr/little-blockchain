from hashlib import sha256
from datetime import datetime
import os
import requests
import time
import pika

class Miner:
    def start_consuming(self):
        time.sleep(30)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = os.getenv('RABBITMQ_HOST'), port = os.getenv('RABBITMQ_PORT')))
        
        self.channel = self.connection.channel()
        self.channel.queue_declare(  queue = os.getenv('RABBITMQ_QUEUE'), 
                                durable=True)
        self.channel.basic_qos( prefetch_count = 1)
        self.channel.basic_consume( queue = os.getenv('RABBITMQ_QUEUE'), 
                                    on_message_callback = self.hash_block)
        try:
            self.channel.start_consuming()
        except Exception as err:
            print('Exception: {0}'.format(err))
            self.channel.stop_consuming()
        
        self.connection.close()
    
    def is_hash_valid(self, hash):
        print(hash)
        return hash.startswith(os.getenv('HASH_DIFFICULT'))

    def hash_block(self, channel, method, properties, body):
        timestamp = datetime.utcnow().timestamp()
        response = requests.get(os.getenv('BLOCKCHAIN_SERVICE'))
        print(response.json())
        prev_hash = response.json()

        hash = ''
        nonce = 1

        while not self.is_hash_valid(hash):
            block = '{}:{}:{}:{}'.format(body, timestamp, prev_hash, nonce)
            hash = sha256(block.encode()).hexdigest()
            nonce += 1

        response = requests.put(os.getenv('BLOCKCHAIN_SERVICE'), data = {'block': block, 'hash' : hash})
        self.channel.basic_ack( delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    miner = Miner()
    miner.start_consuming()