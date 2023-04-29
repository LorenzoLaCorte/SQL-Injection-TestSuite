#!/usr/bin/env python3

# Pytest script to test if an application is vulnerable from SQL injections
# Author: Lorenzo La Corte

import logging
from pathlib import Path
import pytest
import requests


logging.basicConfig(filename="requests.log",
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


# TODO: refactor
def CollectTargets(basepath):
    targets: dict[str, list[str]] = {}
    basepath = Path(basepath)
    subdirs = basepath.iterdir()

    for subdir in subdirs:
        if subdir.is_file(): continue
        targets[subdir.name] = []
        for file in subdir.iterdir():
            if file.is_file():  targets[subdir.name].append(subdir.name+'/'+file.name)

    return targets


# TODO: refactor with args: https://stackoverflow.com/questions/40880259/how-to-pass-arguments-in-pytest-by-command-line
basepath = "Application/"
targets = CollectTargets(basepath)
IP = "localhost"
PORT = 9000

union_payloads = [
        "' UNION ALL SELECT __COLS__ -- - ",
        "\" UNION ALL SELECT __COLS__ -- - ",
        "1 UNION ALL SELECT __COLS__ -- - ",
]

error_payloads = [
        "' AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - ",
        "\" AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - ",
        "1 AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - ",
]

# --------------------------- REQUEST METHODS --------------------------- #

def send_request(target, params, method) -> str:
    if method == "GET": 
        response = requests.get(f"http://{IP}:{PORT}/{target}", params=params)
        print(f"Sending request to: http://{IP}:{PORT}/{target} - With params: {params}") # TODO: turn to log

    elif method == "POST":
        response = requests.post(f"http://{IP}:{PORT}/{target}", data=params)

    else:
        raise Exception(f"Error: Unrecognized Method")

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}")

    print(f"Result is: {response.text}\n") # TODO: turn to log
    return response.text


def functional_request(target, params, method, oracle) -> bool:
    return oracle in send_request(target, params, method)


def security_request(target, params, method, oracle) -> bool:
    return oracle not in send_request(target, params, method)

# ------------------------- FUNCTIONAL TESTING ------------------------- #

@pytest.mark.parametrize("page", targets['find'])
def test_functional_step_find(page):
    params = {"search": "Apple"}
    oracle = "Apple"
    assert functional_request(page, params, "GET", oracle)

@pytest.mark.parametrize("page", targets['login'])
def test_functional_step_login(page):
    params = {"user": "any", "pass": "password"}
    oracle = "Welcome"
    assert functional_request(page, params, "POST", oracle)

@pytest.mark.parametrize("page", targets['search'])
def test_functional_step_search(page):
    params = {"max": 100} if "price" in page else {"search": "Apple"}
    oracle = "3.00 €" if "search_by_price3" in page else "Apple"
    assert functional_request(page, params, "GET", oracle)


# ------------------------- SECURITY TESTING ------------------------- #


@pytest.mark.parametrize("page", targets['find'])
@pytest.mark.parametrize("payload", list(map(lambda payload: payload.replace("__COLS__", "USER(),USER()"), union_payloads)) + error_payloads)
def test_security_step_find(page, payload):
    params = {"search": payload}
    oracle = "root"
    assert security_request(page, params, "GET", oracle)

@pytest.mark.parametrize("page", targets['login'])
@pytest.mark.parametrize("payload", list(map(lambda payload: payload.replace("__COLS__", "USER(),USER(),USER(),USER()"), union_payloads)) + error_payloads)
def test_security_step_login(page, payload):
    params = {"user": "any", "pass": payload}
    oracle = "root"
    assert security_request(page, params, "POST", oracle)

@pytest.mark.parametrize("page", targets['search'])
@pytest.mark.parametrize("payload", list(map(lambda payload: payload.replace("__COLS__", "USER() AS name, USER() AS price"), union_payloads)) + error_payloads)
def test_security_step_search(page, payload):
    params = {"max": payload} if "price" in page else {"search": payload}
    oracle = "root"
    assert security_request(page, params, "GET", oracle)
