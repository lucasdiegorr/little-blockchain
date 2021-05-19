FROM python:3.8-alpine

LABEL author="Lucas Rocha"


COPY . /app
WORKDIR /app

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN pip3 install -r requirements.txt

RUN apk del build-deps

ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672
ENV RABBITMQ_QUEUE=transation_queue
ENV MARIADB_HOST=mysql
ENV MARIADB_PORT=3306
ENV MARIADB_USER=root
ENV MARIADB_PASSWORD=Password123!
ENV MARIADB_DATABASE=blockchain

EXPOSE 5000

CMD python3 ./blockchain.py