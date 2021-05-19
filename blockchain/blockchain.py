from flask import Flask, request
from flask_restful import Api, Resource
import pika
import mariadb
import os

class Blockchain(Resource):

    def __init__(self):
        self.config = {
            'host': os.getenv('MARIADB_HOST'),
            'port': int(os.getenv('MARIADB_PORT')),
            'user': os.getenv('MARIADB_USER'),
            'password': os.getenv('MARIADB_PASSWORD'),
            'database': os.getenv('MARIADB_DATABASE')
        }

    def get(self):
        connection = mariadb.connect(**self.config)
        cursor = connection.cursor()
        cursor.execute("SELECT hash FROM block b ORDER BY id DESC LIMIT 1")
        
        resultset = cursor.fetchone()

        connection.close()

        if resultset:
            return {'hash': resultset[0]}
        else:
            return {'hash': ''}

    def post(self):
        data = request.form['data']

        connection = pika.BlockingConnection(pika.ConnectionParameters(host = os.getenv('RABBITMQ_HOST'), port = os.getenv('RABBITMQ_PORT')))
        
        channel = connection.channel()
        channel.queue_declare(  queue = os.getenv('RABBITMQ_QUEUE'), 
                                durable = True)
        channel.basic_publish(  exchange = '',
                                routing_key = os.getenv('RABBITMQ_QUEUE'),
                                body = data,
                                properties = pika.BasicProperties( delivery_mode = 1 ))
        
        connection.close()
        
        return {'response': data}

    def put(self):
        block = request.form['block']
        hash = request.form['hash']
        
        print(block)
        print(hash)

        connection = mariadb.connect(**self.config)
        cursor = connection.cursor()
        
        print(cursor)

        ele = cursor.execute("INSERT INTO block (block, hash) VALUES(?, ?)", (block, hash))

        connection.commit()

        connection.close()

        return {'hash': hash}

app = Flask(__name__)
api = Api(app)

api.add_resource(Blockchain, '/blockchain')

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 5000)