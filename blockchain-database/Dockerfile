FROM mariadb:10.3

LABEL author="Lucas Rocha"

ENV MYSQL_DATABASE=blockchain
ENV MYSQL_ROOT_PASSWORD=Password123!

COPY initdb.sql /docker-entrypoint-initdb.d/

EXPOSE 3306
