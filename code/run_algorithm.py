# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import time
import matplotlib.pyplot as plt

# Import algorithms
from random_walk import random_walk
from greedy import greedy
from greedy_lookahead import greedy as greedy_la
from beam import beamsearch
from branch_n_bound import branch_n_bound

# Import visualisation functions
from graph1D import plot1D

# Import auxiliary functions
from user_input import ask_number

def run_algorithm(algorithms, algorithm, protein_string, dimension):
    '''
    Runs an algorithm in a cetain dimension with a certain protein, decided by the user.
    Returns the protein object, energies dictionary and elapsed time in a list
    '''

    # Who could have seen that one coming
    if dimension == "1D":

        plot1D(protein_string)
        plt.show()

        exit("Error: Couldn't fold protein in only one dimension")

    # Run a random walk
    elif algorithm == algorithms[0]:

        # Ask the user for the number of runs
        N_runs = ask_number(2, 1E100, "integer", "How many proteins to fold [2-∞]?: ")

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, dict, matrix_sizes = random_walk(protein_string, N_runs, dimension)
        elapsed_time = time.time() - start_time

    # Run a normal greedy search
    elif algorithm == algorithms[1]:

        # Ask the user for the number of runs
        N_runs = ask_number(2, 1E100, "integer", "How many proteins to fold [2-∞]?: ")

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, dict, matrix_sizes = greedy(protein_string, N_runs, dimension)
        elapsed_time = time.time() - start_time

    # Run a normal greedy search with look_ahead
    elif algorithm == algorithms[2]:

        # Ask the user for the number of runs and look-aheads
        N_runs = ask_number(2, 1E100, "integer", "How many proteins to fold [2-∞]?: ")
        look_aheads = ask_number(0, 1E100, "integer", "How many steps to look ahead [0-∞]?: ")

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, dict, matrix_sizes = greedy_la(protein_string, look_aheads, N_runs, dimension)
        elapsed_time = time.time() - start_time

    # Run a beam search
    elif algorithm == algorithms[3]:

        # Ask the user for the beam width
        beam_width = ask_number(1, 1E100, "integer", "What is the beam width [1-∞]?: ")

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, dict, matrix_sizes = beamsearch(protein_string, beam_width, dimension)
        elapsed_time = time.time() - start_time

    # Run a probability-based branch n bound algorithm
    elif algorithm == algorithms[4]:

        # Ask the user for the probabilities
        prob_below_average = ask_number(0.0, 1.0, "float", "Choose a probability to discard proteins with energy below the average [0.0-1.0]?: ")
        prob_above_average = ask_number(0.0, 1.0, "float", "Choose a probability to discard proteins with energy above the average [0.0-1.0]?: ")

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, dict, matrix_sizes = branch_n_bound(protein_string, prob_above_average, prob_below_average, dimension)
        elapsed_time = time.time() - start_time

    return protein, dict, matrix_sizes, elapsed_time
