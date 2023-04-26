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

logging.basicConfig(filename="requests.log",
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

union_payloads = {
        'single': "' UNION ALL SELECT __COLS__ -- - ",
        'double': "\" UNION ALL SELECT __COLS__ -- - ",
        'value': "1 UNION ALL SELECT __COLS__ -- - ",
}

error_payloads = {
        'single': "' AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - ",
        'double': "\" AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - ",
        'value': "1 AND ExtractValue(0, CONCAT( 0x5c, USER() ) ) -- - ",
}

def CollectTargets(basepath):
    targets: dict[str, list[str]] = {}
    basepath = Path(basepath)
    subdirs = basepath.iterdir()

    for subdir in subdirs:
        if subdir.is_file(): continue
        targets[subdir.name] = []
        for file in subdir.iterdir():
            if file.is_file():  targets[subdir.name].append(file.name)

    pages = []
    for subdir, files in targets.items(): 
        for file in files:
            pages.append(tuple([subdir+'/'+file]))

    return pages

class TestClass(unittest.TestCase):

    basepath = "Application/"
    targets = []

    def setUp(self):
        self.targets = CollectTargets(self.basepath)
        print(self.targets)

    @pytest.mark.parametrize("page", targets)
    def test_functional_step(page):
        print(page)
        assert True

    @pytest.mark.parametrize("page", targets)
    def test_security_step(page):
        assert True

    def tearDown(self):
        pass


def testSuite(args):
    print(f"\u2699 Lax TestSuite \u2699", flush=True)

    suite = unittest.TestSuite()
    suite.addTest(TestClass('test_functional_step'))
    suite.addTest(TestClass('test_security_step'))


    return suite

def main() -> None:
    parser: ArgumentParser = ArgumentParser()

    args: Namespace = parser.parse_args()
    
    unittest.TextTestRunner(verbosity=2).run(testSuite(args)) 

if __name__ == '__main__':
    main()