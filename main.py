# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import os, sys, time
import matplotlib.pyplot as plt

directory = os.path.dirname(os.path.realpath(__file__))

# Add the code paths
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "algorithms"))
sys.path.append(os.path.join(directory, "code", "datastructure"))
sys.path.append(os.path.join(directory, "code", "visualisations"))

# Add the data path
sys.path.append(os.path.join(directory, "data"))

# Import algorithms
from truerandom_walk import random_walk
from truegreedy import greedy
from truebranch_n_bound import branch_n_bound

# Import visualisation functions
from minimal_sizes import plot_matrix_sizes

# Import auxiliary functions
from user_input import ask_integer, ask_float

def read_input():
    '''
    Parse text file containing proteins represented as a string
    Returns a list containing a single protein (represented as a string) per list entry
    '''

    # Opens a datafile as a list with strings
    with open("data/input.txt", "r") as f:
        file_content = f.read()
        file_lines = file_content.split()
    return file_lines

def run_algorithm(algorithms, algorithm, protein_string, dimension):
    '''

    '''

    # Run a random walk
    if algorithm == algorithms[0]:

        N_tries = ask_integer("How many proteins to fold? ")
        while N_tries < 2:
            N_tries = ask_integer("How many proteins to fold? ")

        print(f">{N_tries}\n")

        start_time = time.time()
        protein, dict, matrix_sizes = random_walk(protein_string, N_tries, dimension)
        end_time = time.time() - start_time

        plot_matrix_sizes(matrix_sizes)

    elif algorithm == algorithms[1]:

        N_tries = ask_integer("How many proteins to fold? ")
        while N_tries < 2:
            N_tries = ask_integer("How many proteins to fold? ")

        print(f">{N_tries}\n")

        start_time = time.time()
        protein, dict = greedy(protein_string, N_tries, dimension)
        end_time = time.time() - start_time

    # Run a probability-based branch n bound algorithm
    elif algorithm == algorithms[2]:

        # Get probabilities
        prob_below_average = ask_float("Choose a probability to discard proteins with energy below the average? ")
        while 0 > prob_below_average or prob_below_average > 1:
            print("A probability is between 0 and 1. Try again.")
            prob_below_average = ask_float("Choose a probability to discard proteins with energy below the average? ")
            print("Probability below average: ",prob_below_average)

        prob_above_average = ask_float("Choose a probability to discard proteins with energy above the average? ")
        while 0 > prob_above_average or prob_above_average > 1:
            print("A probability is between 0 and 1. Try again.")
            prob_above_average = ask_float("Choose a probability to discard proteins with energy above the average? ")
            print("Probability above average: ",prob_above_average)

        start_time = time.time()
        protein = branch_n_bound(protein_string, prob_above_average, prob_below_average, dimension)
        end_time = time.time() - start_time

    else:
        print(f"Error: Unknown algorithm '{algorithm}'")
        exit(1)

    return protein, end_time

def print_list(list):
    for i, element in zip(range(len(list)), list):
        print(f"{i + 1}: {element}")
    print()

if __name__ == "__main__":

    dimensions = ["2D", "3D"]
    print_list(dimensions)

    chosen_dimension = ask_integer("Choose the dimensions: ") - 1
    while chosen_dimension < 0 or chosen_dimension > len(dimensions) - 1:
        chosen_dimension = ask_integer("Choose the dimensions: ") - 1

    print(f">{dimensions[chosen_dimension]}\n")

    algorithms = ["random walk", "greedy", "probabilty-based branch-n-bound"]
    print_list(algorithms)

    chosen_algorithm = ask_integer("Choose an algorithm: ") - 1
    while chosen_algorithm < 0 or chosen_algorithm > len(algorithms) - 1:
        chosen_algorithm = ask_integer("Choose an algorithm: ") - 1

    print(f">{algorithms[chosen_algorithm]}\n")

    proteins = read_input()
    print_list(proteins)

    chosen_protein = ask_integer("Choose a protein: ") - 1
    while chosen_protein < 0 or chosen_protein > len(proteins) - 1:
        chosen_protein = ask_integer("Choose a protein: ") - 1

    print(f">{proteins[chosen_protein]}\n")

    protein, end_time = run_algorithm(algorithms, algorithms[chosen_algorithm], proteins[chosen_protein], dimensions[chosen_dimension])
    print(protein)
    print(time.strftime('\nElapsed time: %H:%M:%S', time.gmtime(end_time)))

    protein.visualise(proteins[chosen_protein])

    plt.show()
