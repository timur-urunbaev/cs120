'''
Schelling Model of Housing Segregation

Automatically added to test code for is_satisfied

Handle the fact that the test code may not be in the same directory as
schelling.py
'''

import os
import sys
import pytest

import test_helpers

# Handle the fact that the grading code may not
# be in the same directory as schelling.py
sys.path.insert(0, os.getcwd())

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

# Keep pylint from complaining about generated code.
#pylint: disable-msg=wrong-import-position
#pylint: disable-msg=missing-docstring
import utility
import schelling

# EPS = 0.000001

#pylint: disable-msg=too-many-arguments
def helper_test_is_satisfied(filename, R, location, sim_sat_range, expected):
    '''Check result of calling is_satisfied on the specified location
    with in a D-neighborhood and the specified threshold.

    Inputs:
        filename: (string) name of the input grid file
        R: (integer) neighborhood parameter
        location: (pair of integers) location in the grid to be tested
        sim_sat_range: (pair of floats) (lower bound, upper bound) for
          satisfaction score
        expected: (boolean) expected result.

    '''
    full_path = os.path.join(TEST_DIR, filename)
    grid = utility.read_grid(full_path)

    actual = schelling.is_satisfied(grid, R, location, sim_sat_range)
    if actual != expected:
        recreate_msg = "To recreate this test in ipython3 run:\n"
        recreate_msg += "  grid = utility.read_grid('{}')\n"
        recreate_msg += "  schelling.is_satisfied(grid, {}, {}, {})\n"
        recreate_msg = recreate_msg.format(full_path,
                                           R,
                                           location,
                                           sim_sat_range)
        s = "Actual value ({}) is not equal to the expected value ({}).\n"
        s = s + "\n\n" + recreate_msg
        pytest.fail(s.format(actual, expected))

@pytest.mark.parametrize(
    "params",
    test_helpers.read_config_file("test_is_satisfied.json"))
def test_is_satisfied(params):
    helper_test_is_satisfied(params["filename"],
                             params["R"],
                             tuple(params["location"]),
                             tuple(params["sim_sat_range"]),
                             params["expected_result"])
