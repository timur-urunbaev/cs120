'''
Helper functions for the test code
'''

import os
import json
import pytest

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

def read_config_file(filename):
    '''
    Load the test cases from a JSON file.

    Inputs:
      filename (string): the name of the test configuration file.

    Returns: (list) test cases
    '''

    full_path = os.path.join(TEST_DIR, filename)
    try:
        with open(full_path) as f:
            return json.load(f)
    except FileNotFoundError:
        msg = ("Cannot open file: {}."
               "Did you remember to run the script "
               "to get the data and the test files?")
        pytest.fail(msg.format(full_path))
