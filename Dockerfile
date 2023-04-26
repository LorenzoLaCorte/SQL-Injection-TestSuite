FROM alpine:latest

RUN apk update
RUN apk add php
RUN apk add php-mysqli
RUN apk add mysql-client
RUN apk add mariadb
RUN apk add mariadb-client

COPY Application /Application
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]