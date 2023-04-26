#!/bin/sh

# Start MySQL server (if not already running)
# /etc/init.d/mariadb start

# # Wait for MySQL server to start up
# while ! mysqladmin ping -h 127.0.0.1 --silent; do
#     sleep 1
# done

# # Load database schema and data
# mysql -h 127.0.0.1 -u root --password=${MYSQL_ROOT_PASSWORD} fstt23_assignment < ./Seed/create-items.sql
# mysql -h 127.0.0.1 -u root --password=${MYSQL_ROOT_PASSWORD} fstt23_assignment < ./Seed/create-users.sql
# mysql -h 127.0.0.1 -u root --password=${MYSQL_ROOT_PASSWORD} fstt23_assignment < ./Seed/create-items.sql

# Start PHP server
cd /Application && php -S localhost:9000