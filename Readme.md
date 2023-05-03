# SQL Injections pytest TestSuite
This test suite uses ```pytest``` to organize and run tests steps.

## Environment Setup
My credentials:
```
$mysql_server = "172.17.0.2"; // or any host on which you deployed it
$mysql_user = "root";
$mysql_pass = "pass"; // The password you set up during installation
```

## Instructions
To setup the environment:
```
./setup.sh
```

To (eventually) install pytest:
```
pip install pytest
```

To run the script:
```
pytest
```


## Tests
For each page of the target application, there is test step that checks:

- if the page is working correctly (e.g., for login pages, that the login is working correctly)

- if the page is vulnerable to: 
    - Standard SQL injection (additional).
    - Union-based SQL injection.
    - Error-based SQL injection.
    - Blind - Boolean Based SQL injection (additional).
    - Blind - Time Based SQL injection (additional).


# TODO
- do ApplicationFixed
- enhance setup templating all the variable both in .sh, Seed/*, and .php
- do additional tests:
    - first offline
    - then in the script
- enable logging

## How to Use

If you want to change parameters:

```
pip install jinja2
python script.py --basepath Application --port 9000 --pass pass123
```

Then you can setup the application:
```
./setup.sh
```

And then launch the testsuite:
```
pytest
```