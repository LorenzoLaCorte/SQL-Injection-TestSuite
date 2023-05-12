# SQL Injections pytest TestSuite
This test suite uses ```pytest``` to organize and run tests steps.
For each page of the target application, there is test step that checks:

- if the page is working correctly (e.g., for login pages, that the login is working correctly)

- if the page is vulnerable to: 
    - Union-based SQL injection.
    - Error-based SQL injection.

## Instructions

You can either:
- use the default credentials and parameters,
- simply template your own one using ```setup.py```

### Environment Setup

If you prefer the second option you can:

Install *jinja*:
```
pip install jinja2
```

Set up the environment using the setup script:
```
python3 setup.py --basepath Application --port 9000 --pass pass123
```

### Run the Application

Once the test suite script is ready, you can setup the application:
```
./setup.sh
```

And then launch the testsuite:
```
pytest
```


## Possible Further Improvements
- do additional tests, in particular test if the page is vulnerable to: 
    - Standard SQL injection.
    - Blind - Boolean Based SQL injection.
    - Blind - Time Based SQL injection.