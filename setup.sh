#!/bin/bash

CONTAINER_NAME="mysql-container"
MYSQL_IP="172.17.0.2"
MYSQL_PASSWORD="pass"
PHP_PORT=9000
APP_PATH="Application"

if [[ ! -z $(docker ps -a -q -f name="$CONTAINER_NAME") ]]; then
    echo "MySQL container is already running."
    sudo docker stop "$CONTAINER_NAME" && sudo docker rm "$CONTAINER_NAME"
fi

sudo docker run --name "$CONTAINER_NAME" -e MYSQL_ROOT_PASSWORD="$MYSQL_PASSWORD" -p 3006:3306 -d mysql

until docker exec "$CONTAINER_NAME" mysqladmin ping -h "$MYSQL_IP" -u root --password="$MYSQL_PASSWORD" --silent; do
    echo "Waiting for the container to be running."
    sleep 1
done

echo "Configuring mysql and starting the Application."
mysql -h "$MYSQL_IP" -u root --password="$MYSQL_PASSWORD" < ./Seed/create-database.sql
mysql -h "$MYSQL_IP" -u root --password="$MYSQL_PASSWORD" fstt23_assignment < ./Seed/create-users.sql
mysql -h "$MYSQL_IP" -u root --password="$MYSQL_PASSWORD" fstt23_assignment < ./Seed/create-items.sql

cd "$APP_PATH" && php -S localhost:"$PHP_PORT"