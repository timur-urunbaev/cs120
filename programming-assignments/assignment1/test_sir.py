'''
Test code for Modeling Epidemics

Emma Nechamkin and Anne Rogers
July 2018

Borja Sotomayor
September 2018, 2020

Anne Rogers
July 2019
'''

import json
import os
import sys
import random

import pytest

import sir

# Handle the fact that the grading code may not
# be in the same directory as sir.py
sys.path.append(os.getcwd())

# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")


def gen_check_rand_calls(seed, max_num_calls):
    '''
    Generate a function that can be used to check whether the correct
    number of calls were made to the random number generator.

    Inputs:
      seed (int): the seed for the random number generator
      max_num_calls (int): the maximum number of calls to
         random.random() that will need to be verified.

    Returns: function of one variable
    '''

    random.seed(seed)
    rand_vals = [random.random() for i in range(max_num_calls+1)]

    def check(expected_num_calls):
        '''
        Check whether the expected number of calls to random.random()
        were made.

        Inputs:
          expected_num_calls: the number of calls that should have
          been made.

        Returns: boolean that will be True if the check succeeded and
          False otherwise and, if necessary, an error message as a
          string.
        '''
        assert expected_num_calls <= max_num_calls

        # Make a call to random.
        actual_r = random.random()
        expected_r = rand_vals[expected_num_calls]

        # Did the call to random yield the expected value?
        if actual_r == pytest.approx(expected_r):
            return True, None

        for i, r in enumerate(rand_vals):
            if actual_r == pytest.approx(r):
                if i < expected_num_calls:
                    return False, "Not enough calls to random.random()"
                return False, "Too many calls to random.random()"

        return False, "Incorrect number of calls to random.random()"

    return check


CHECK_RAND_20170217 = gen_check_rand_calls(20170217, 100)


def read_config_file(filename):
    '''
    Load the test cases from a JSON file.

    Inputs:
      filename (string): the name of the test configuration file.

    Returns: (list) test cases
    '''

    with open(os.path.join(TEST_DIR, filename)) as f:
        return json.load(f)


def gen_none_error(recreate_msg):
    '''
    Generate the error message for an unexpected return value of None.

    Inputs:
      recreate_msg (string): a string with the informatino needed to
        rerun the test in ipython.

    Returns (string): error message
    '''

    msg = "The function returned None."
    msg += " Did you forget to include a return statement?\n"
    return msg + recreate_msg + "\n"


def gen_type_error(recreate_msg, expected, actual):
    '''
    Generate the error message for an return value of the wrong type

    Inputs:
      recreate_msg (string): a string with the informatino needed to
        rerun the test in ipython.

    Returns (string): error message
    '''


    msg = "The function returned a value of the wrong type.\n"
    msg += "  Expected return type: {}.\n"
    msg += "  Actual return type: {}.\n"
    msg += recreate_msg  + "\n"
    return msg.format(type(expected), type(actual))


def gen_mismatch_error(recreate_msg, expected, actual):
    '''
    Generate the error message for the case whether the expected and
    actual values do not match.

    Inputs:
      recreate_msg (string): a string with the informatino needed to
        rerun the test in ipython.

    Returns (string): error message
    '''

    msg = "Actual ({}) and expected ({}) values do not match.\n"
    msg += recreate_msg + "\n"
    return msg.format(actual, expected)


###### Task: Count number of infected people ######

@pytest.mark.parametrize(
    "params",
    read_config_file("count_infected.json"))
def test_count_infected(params):
    '''
    Test harness for count_infected function.

    Inputs:
      params (dictionary): the test parameters:
        city and the expected number of infected folks in the city.
    '''

    actual_num_infected = sir.count_infected(params["city"])

    recreate_msg = "To recreate this test in ipython3 run:\n"
    recreate_msg += "  sir.count_infected({})".format(params["city"])

    assert actual_num_infected is not None, \
        gen_none_error(recreate_msg)

    expected_num_infected = params["expected_num_infected"]
    assert isinstance(actual_num_infected, type(expected_num_infected)), \
        gen_type_error(recreate_msg,
                       expected_num_infected,
                       actual_num_infected)

    assert actual_num_infected == expected_num_infected, \
        gen_mismatch_error(recreate_msg,
                           expected_num_infected,
                           actual_num_infected)


###### Task: has_an_infected_neighbor ######

@pytest.mark.parametrize(
    "params",
    read_config_file("has_infected_neighbor_tests.json"))
def test_has_an_infected_neighbor(params):
    '''
    Test harness for has_an_infected_neighbor

    Inputs:
      params (dictionary): the test parameters:
        city, iindex of a position in the city,
        the expected result
    '''

    actual = sir.has_an_infected_neighbor(params["city"], params["position"])

    recreate_msg = "To recreate this test run:\n"
    recreate_msg += "  sir.has_an_infected_neighbor({}, {})"
    recreate_msg = recreate_msg.format(params["city"], params["position"])

    assert actual is not None, \
        gen_none_error(recreate_msg)

    expected = params["expected"]
    assert isinstance(actual, type(expected)), \
        gen_type_error(recreate_msg,
                       expected,
                       actual)

    assert actual == expected, \
        gen_mismatch_error(recreate_msg, expected, actual)


###### Task : Advance person at position ######
@pytest.mark.parametrize(
    "params",
    read_config_file("advance_person_tests.json"))
def test_advance_person_at_position(params):
    '''
    Test harness for advance_person_at_position

    Inputs:
      params (dictionary): the test parameters:
        seed, city, index of position in the city,
        infection rate, number of days contagious
        expected result
    '''

    city_copy = params["city"][:]

    actual = sir.advance_person_at_position(params["city"],
                                            params["position"],
                                            params["days_contagious"])

    recreate_msg = "To recreate this test run:\n"
    recreate_msg += "  sir.advance_person_at_position({}, {}, {})"
    recreate_msg = recreate_msg.format(params["city"],
                                       params["position"],
                                       params["days_contagious"])

    assert actual is not None, \
        gen_none_error(recreate_msg)

    expected = params["expected"]
    assert isinstance(actual, type(expected)), \
        gen_type_error(recreate_msg,
                       expected,
                       actual)

    assert actual == expected, \
        gen_mismatch_error(recreate_msg, expected, actual)

    assert city_copy == params["city"], \
        "\nDo not modify the city!\n" + recreate_msg


###### Task: Move simulation forward one day ######
@pytest.mark.parametrize(
    "params",
    read_config_file("simulate_one_day_tests.json"))
def test_simulate_one_day(params):
    '''
    Test harness for simulate_one_day

    Inputs:
      params (dictionary): the test parameters:
        seed, city, infection rate, number of days contagious,
        expected result
    '''

    city_copy = params["city"][:]

    actual_city = sir.simulate_one_day(params["city"],
                                       params["days_contagious"])

    recreate_msg = "To recreate this test run:\n"
    recreate_msg += "  sir.simulate_one_day({}, {})"
    recreate_msg = recreate_msg.format(params["city"],
                                       params["days_contagious"])

    assert actual_city is not None, \
        gen_none_error(recreate_msg)

    expected_city = params["expected_city"]
    assert isinstance(actual_city, type(expected_city)), \
        gen_type_error(recreate_msg,
                       expected_city,
                       actual_city)

    assert city_copy == params["city"], \
        "\nDo not modify the input city!\n" + recreate_msg

    msg = "Input city and returned city should refer to different lists."
    msg += recreate_msg
    assert actual_city is not params["city"], msg

    assert actual_city == expected_city, \
        gen_mismatch_error(recreate_msg, expected_city, actual_city)


###### Task: run simulation over multiple days  ######

def __test_run_simulation(params):
    '''
    Test harness for run_simulation

    Inputs:
      params (dictionary): the test parameters:
        seed, city, maximum number of days to simulate,
        infection rate, number of days contagious
        expected result
    '''

    actual = sir.run_simulation(params["starting_city"],
                                params["days_contagious"],
                                params["random_seed"],
                                params["vaccine_effectiveness"]
                                )

    recreate_msg = "To recreate this test run:\n"
    if params["random_seed"] is None and params["vaccine_effectiveness"] == 0.0:
        recreate_msg += " sir.run_simulation({}, {})"
        recreate_msg = recreate_msg.format(params["starting_city"],
                                           params["days_contagious"])
    else:
        recreate_msg += " sir.run_simulation({}, {}, {}, {})"
        recreate_msg = recreate_msg.format(params["starting_city"],
                                           params["days_contagious"],
                                           params["random_seed"],
                                           params["vaccine_effectiveness"]
                                           )

    assert actual is not None, \
        gen_none_error(recreate_msg)

    msg = "Result should be a pair: (city, number of days simulate)\n"
    msg += recreate_msg

    expected = tuple(params["expected"])
    assert isinstance(actual, type(expected)), msg
    assert len(actual) == 2, msg

    expected_city, expected_num_days = expected
    actual_city, actual_num_days = actual

    assert isinstance(actual_city, type(expected_city)), msg
    assert isinstance(actual_num_days, type(expected_num_days)), msg

    assert actual_city == expected_city, \
        gen_mismatch_error(recreate_msg,
                           expected_city,
                           actual_city)

    assert actual_num_days == expected_num_days, \
        gen_mismatch_error(recreate_msg,
                           expected_num_days,
                           actual_num_days)

@pytest.mark.parametrize(
    "params",
    read_config_file("run_simulation_tests.json"))
def test_run_simulation(params):
    __test_run_simulation(params)

###### Task: vaccinate a city ######

@pytest.mark.parametrize(
    "params",
    read_config_file("vaccinate_city.json"))
def test_vaccinate_city(params):
    '''
    Test harness for vaccinate_city
    Inputs:
      params (dictionary): the test parameters:
        seed, city, vaccine effectiveness, expected city
    '''

    # use the same seed for all the tests
    if params["seed"] == sir.TEST_SEED:
        # Use pre-generated random checking function
        check_rand = CHECK_RAND_20170217
    else:
        check_rand = gen_check_rand_calls(params["seed"], 100)

    random.seed(params["seed"])

    city_copy = params["city"][:]

    actual_city = sir.vaccinate_city(params["city"],
                                     params["vaccine_effectiveness"])

    recreate_msg = "To recreate this test run:\n"
    recreate_msg += "  random.seed({}); "
    recreate_msg += "sir.vaccinate_city({}, {})"
    recreate_msg = recreate_msg.format(params["seed"],
                                       params["city"],
                                       params["vaccine_effectiveness"])

    assert actual_city is not None, \
        gen_none_error(recreate_msg)

    expected_city = params["expected_city"]
    assert isinstance(actual_city, type(expected_city)), \
        gen_type_error(recreate_msg,
                       expected_city,
                       actual_city)

    assert city_copy == params["city"], \
        "\nDo not modify the input city!\n" + recreate_msg

    msg = "Input city and returned city should refer to different lists."
    msg += recreate_msg
    assert actual_city is not params["city"], msg

    assert actual_city == expected_city, \
        gen_mismatch_error(recreate_msg, expected_city, actual_city)

    (check, msg) = check_rand(params["num_rand_calls"])
    assert check, msg + "\n" + recreate_msg


@pytest.mark.parametrize(
    "params",
    read_config_file("simulation_with_vaccine.json"))
def test_simulation_with_vaccine(params):
    __test_run_simulation(params)

###### Task: Testing infection spread ######

@pytest.mark.parametrize(
    "params",
    read_config_file("calc_avg_days_to_zero_infections.json"))

def test_calc_avg_days_to_zero_infections(params):
    '''
    Test harness for compute_average_num_infected

    Inputs:
      params (dictionary): the test parameters:
        seed, city, maximum number of days to simulate,
        infection rate, number of days contagious
        expected result
    '''

    actual = sir.calc_avg_days_to_zero_infections(
        params["starting_city"],
        params["days_contagious"],
        params["starting_seed"],
        params["vaccine_effectiveness"],
        params["num_trials"])


    recreate_msg = "To recreate this test run:\n"
    recreate_msg += "  sir.calc_avg_days_to_zero_infections({}, {}, {}, {}, {})"
    recreate_msg = recreate_msg.format(params["starting_city"],
                                       params["days_contagious"],
                                       params["starting_seed"],
                                       params["vaccine_effectiveness"],
                                       params["num_trials"])

    assert actual is not None, \
        gen_none_error(recreate_msg)

    assert isinstance(actual, type(params["expected"])), \
        gen_type_error(recreate_msg,
                       params["expected"],
                       actual)

    assert actual == pytest.approx(params["expected"]), \
        gen_mismatch_error(recreate_msg,
                           params["expected"],
                           actual)
