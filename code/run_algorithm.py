# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import matplotlib.pyplot as plt
import numpy as np
import time

# Import algorithms
from beam import beamsearch
from branch_n_bound import branch_n_bound
from greedy_lookahead import greedy
from hillclimber import hillclimber
from random_walk import random_walk

# Import visualisation functions
from graph1D import plot1D

# Import auxiliary functions
from user_input import ask_number, ask_matrix_size

def run_algorithm(algorithms, algorithm, protein_string, dimension):
    '''
    Runs an algorithm in a cetain dimension with a certain protein, decided by the user.
    Returns the protein object, energies energiesionary and elapsed time in a list
    '''
    # Handle a 1D dimension selection
    if dimension == "1D":

        plot1D(protein_string)
        plt.show()

        exit("Error: Couldn't fold protein in only one dimension")

    # dictionary for keeping track of the used parameters
    parameters = {"Matrix size": "",
        "Iterations" : "",
        "Look-aheads" : "",
        "Prob. below" : "",
        "Prob. above" : "",
        "Beam width" : "",
        "Cut acids" : ""}

    # Ask the user for the matrix size to use
    matrix_size = ask_matrix_size(len(protein_string))
    parameters["Matrix size"] = f"{matrix_size}"
    matrix_sizes = {}

    # Run a random walk
    if algorithm == algorithms[0]:

        # Ask the user for the number of runs
        N_runs = ask_number(1, 1E100, "integer", "How many proteins to fold [2-∞]?: ")
        parameters["Iterations"] = f"{N_runs}"

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, energies, matrix_sizes = random_walk(protein_string, N_runs, dimension, matrix_size)
        elapsed_time = time.time() - start_time

    # Run a greedy search with look-ahead
    elif algorithm == algorithms[1]:

        # Ask the user for the number of runs and look-aheads
        N_runs = ask_number(1, 1E100, "integer", "How many proteins to fold [1-∞]?: ")
        parameters["Iterations"] = f"{N_runs}"

        look_aheads = ask_number(0, 1E100, "integer", "How many steps to look ahead [0-∞]?: ")
        parameters["Look-aheads"] = f"{look_aheads}"

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, energies, matrix_sizes = greedy(protein_string, look_aheads, N_runs, dimension, matrix_size)
        elapsed_time = time.time() - start_time

    # Run a beam search
    elif algorithm == algorithms[2]:

        # Ask the user for the beam width
        beam_width = ask_number(1, 1E100, "integer", "What is the beam width [1-∞]?: ")
        parameters["Beam width"] = f"{beam_width}"

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, energies, matrix_sizes = beamsearch(protein_string, beam_width, dimension, matrix_size)
        elapsed_time = time.time() - start_time

    # Run a probability-based branch and bound algorithm
    elif algorithm == algorithms[3]:

        # Ask the user for the probabilities for pruning
        prob_below_average = ask_number(0.0, 1.0, "float", "Choose a probability to discard proteins with energy below the average [0.0-1.0]?: ")
        parameters["Prob. below"] = f"{prob_below_average}"

        prob_above_average = ask_number(0.0, 1.0, "float", "Choose a probability to discard proteins with energy above the average [0.0-1.0]?: ")
        parameters["Prob. above"] = f"{prob_above_average}"

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, energies, matrix_sizes = branch_n_bound(protein_string, prob_above_average, prob_below_average, dimension, matrix_size)
        elapsed_time = time.time() - start_time

    # Run a hill climber
    elif algorithm == algorithms[4]:

        # Ask the user for the number of acids they want to cut out
        cut_acids = ask_number(4, 6, "integer", "How many acids will be cut out of the protein each time[4-6]: ")
        parameters["Cut acids"] = f"{cut_acids}"

        # Ask the user for the number of iterations that they want to re-fold a part of the protein
        iterations = ask_number(1, 1E100, "integer", "How many times will the protein be cut and re-folded(iterations): [1-∞]: ")
        parameters["Iterations"] = f"{iterations}"

        # Run the algorithm and keep track of the time
        start_time = time.time()
        protein, energies, matrix_sizes = hillclimber(protein_string, dimension, matrix_size, iterations, cut_acids)
        elapsed_time = time.time() - start_time

    return protein, energies, matrix_sizes, start_time, elapsed_time, parameters
