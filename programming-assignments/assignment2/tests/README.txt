CS 121: Schelling's Model of Housing Segregation

City files:

The grid file format is simple. The first line contains the grid
size. Each subsequent line contains information for a single row,
starting with row 0. An "M" means that the corresponding location has
a maroon homeowner, a "B" means that the corresponding location has a
blue homeowner, and an "F" means that the location is open.

Here's a list of the grid files:

    a20-sample-writeup.txt: example from the writeup.

    grid-sea-of-red.txt: A grid in which all the homes are occupied by
    maroon homeowners, except two homes that are for sale and two home
    occupied by blue homeowners.

    grid-blue-stripe.txt: A 5x5 grid used in some of the is_satisfied
    tests.

    grid-ten.txt: a 10x10 grid used in a number of tests.

    large-grid.txt: a 40x40 grid used to test whether a solution is
    inefficient

    The files with a "-final.txt" extension represent the final state
    of a test. See the writeup for the list of the corresponding
    tests.

Test files:

The test files contain the parameters used by the test code in
../test_is_satified.py and ../test_do_simulation.py.  JSON is a text
format. These files can be examined in a standard text editor.

Here is a list of the test parameter files:

    test_is_satisfied.json: test parameters for is_satisfied in JSON format.

    test_do_simulation_small.json: test parameters for the small do_simulation tests in JSON format.

    test_do_simulation_medium.json: test parameters for the medium do_simulation tests in JSON format.

    test_do_simulation_large.json: test parameters for the large do_simulation tests in JSON format.
