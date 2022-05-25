"""
CS121: Schelling Model of Housing Segregation

Test code for do_simulation
"""

import os
import sys
import pytest

BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

timeout = 60

# Handle the fact that the grading code may not
# be in the same directory as schelling.py
sys.path.insert(0, os.getcwd())

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)

# Keep pylint from complaining about generated code.
#pylint: disable-msg=wrong-import-position
#pylint: disable-msg=missing-docstring

from schelling import do_simulation
import test_helpers
import utility

def count_homeowners(grid):
    '''
    Count the number of occupied homes:

    Inputs:
        grid: (list of lists of strings) the grid

    Returns: integer
    '''

    num_homeowners = 0
    for row in grid:
        for home in row:
            if home != "O":
                num_homeowners += 1
    return num_homeowners

def helper_test_do_simulation(params):
    '''Do one simulation with the specified parameters

    Match actual grid generated with the expected grid and match
    expected number of relocations and actual number of relocations.

    Inputs:
        params: dictionary with the test parameters.
    '''

    input_filename = os.path.join(TEST_DIR, params["input_filename"])
    R = params["R"]
    sim_sat_range = tuple(params["sim_sat_range"])
    patience = params["patience"]
    max_num_steps = params["max_num_steps"]

    actual_grid = utility.read_grid(input_filename)
    if not params["initial_for_sale"]:
        init_for_sale = utility.find_homes_for_sale(actual_grid)
    else:
        init_for_sale = [tuple(t) for t in params["initial_for_sale"]]

    orig_for_sale = init_for_sale[:]
    expected_num_homeowners = count_homeowners(actual_grid)
    expected_num_relocations = params["expected_num_relocations"]

    actual_num_relocations = do_simulation(actual_grid, R, sim_sat_range,
                                           patience, max_num_steps,
                                           init_for_sale)
    actual_num_homeowners = count_homeowners(actual_grid)

    expected_filename = params["expected_filename"]
    expected_grid = utility.read_grid(expected_filename)

    recreate_msg = "To recreate this test in ipython3 run:\n"
    recreate_msg += "  grid = utility.read_grid('{}')\n"
    recreate_msg += "  schelling.do_simulation(grid, {}, {}, {}, {}, {})"
    recreate_msg = recreate_msg.format(input_filename,
                                       R,
                                       sim_sat_range,
                                       patience,
                                       max_num_steps,
                                       orig_for_sale)

    if actual_num_relocations != expected_num_relocations:
        s = ("actual and expected number of relocations do not match\n"
             "  got {:d}, expected {:d}")
        s = s.format(actual_num_relocations, expected_num_relocations)
        s = s + "\n\n" + recreate_msg
        pytest.fail(s)

    if actual_num_homeowners != expected_num_homeowners:
        if actual_num_homeowners <= expected_num_homeowners:
            s = "Homeowners are fleeing the city!\n"
        else:
            s = "The city is gaining homeowners.\n"
        s = s + "  Actual number of homeowners: {:d}\n"
        s = s + "  Expected number of homeowners: {:d}\n"
        s = s + "\n\n" + recreate_msg
        s = s.format(actual_num_homeowners, expected_num_homeowners)
        pytest.fail(s)

    mismatch = utility.find_mismatch(actual_grid, expected_grid)
    if mismatch:
        (i, j) = mismatch
        s = ("actual and expected grid values do not"
             " match at location ({:d}, {:d})\n")
        s = s + "  got {}, expected {}"
        s = s + "\n\n" + recreate_msg
        s = s.format(i, j, actual_grid[i][j], expected_grid[i][j])
        pytest.fail(s)



@pytest.mark.parametrize(
    "params",
    test_helpers.read_config_file("test_do_simulation_small.json"))
def test_do_simulation_small(params):
    helper_test_do_simulation(params)


@pytest.mark.parametrize(
    "params",
    test_helpers.read_config_file("test_do_simulation_medium.json"))
def test_do_simulation_medium(params):
    helper_test_do_simulation(params)

@pytest.mark.parametrize(
    "params",
    test_helpers.read_config_file("test_do_simulation_large.json"))
def test_do_simulation_large(params):
    helper_test_do_simulation(params)
