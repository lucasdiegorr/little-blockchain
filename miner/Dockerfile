FROM python:3.8-alpine

LABEL author="Lucas Rocha"

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672
ENV RABBITMQ_QUEUE=transation_queue
ENV HASH_DIFFICULT=0000
ENV BLOCKCHAIN_SERVICE=http://blockchain/blockchain

CMD python3 ./miner.py