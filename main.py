# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import os, sys, time
import matplotlib.pyplot as plt

directory = os.path.dirname(os.path.realpath(__file__))

# Add the code paths
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "algorithms"))
sys.path.append(os.path.join(directory, "code", "algorithms", "2D"))
sys.path.append(os.path.join(directory, "code", "algorithms", "3D"))
sys.path.append(os.path.join(directory, "code", "datastructure"))
sys.path.append(os.path.join(directory, "code", "datastructure", "2D"))
sys.path.append(os.path.join(directory, "code", "datastructure", "3D"))

# Add the data path
sys.path.append(os.path.join(directory, "data"))

# Import algorithms
from random_walk import random_walk
from greedy import greedy
from branch_n_bound import branch_n_bound

# Import datastructure and auxiliary functions
from acid import Acid
from protein import Protein
from acid3D import Acid as Acid3D
from protein3D import Protein as Protein3D

from graph import visualise, dictionary_hist
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

def run_algorithm(algoritms, chosen_algorithm, chosen_protein):
    '''

    '''

    # Run a random walk
    if chosen_algorithm == algorithms[0]:

        N_tries = ask_integer("How many proteins to fold? ")
        while N_tries < 2:
            N_tries = ask_integer("How many proteins to fold? ")

        print(f">{N_tries}\n")

        start_time = time.time()
        protein, dict = random_walk(chosen_protein, N_tries)
        end_time = time.time() - start_time

    # Run a greedy algorithm
    elif chosen_algorithm == algorithms[1]:

        N_tries = ask_integer("How many proteins to fold? ")
        while N_tries < 2:
            N_tries = ask_integer("How many proteins to fold? ")

        print(f">{N_tries}\n")

        start_time = time.time()
        protein, dict = greedy(chosen_protein, N_tries)
        end_time = time.time() - start_time

    # Run a probability-based branch n bound algorithm
    elif chosen_algorithm == algorithms[2]:

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
        protein = branch_n_bound(chosen_protein, prob_above_average, prob_below_average)
        end_time = time.time() - start_time

    else:
        print(f"Error: Unknown algorithm '{chosen_algorithm}'")
        exit(1)

    return protein, end_time


if __name__ == "__main__":

    algorithms = ["random walk", "greedy", "probabilty-based branch-n-bound"]

    for i, algorithm in zip(range(len(algorithms)), algorithms):
        print(f"{i + 1}: {algorithm}")
    print()

    chosen_algorithm = ask_integer("Choose an algorithm: ") - 1
    while chosen_algorithm < 0 or chosen_algorithm > len(algorithms) - 1:
        chosen_algorithm = ask_integer("Choose an algorithm: ") - 1

    print(f">{algorithms[chosen_algorithm]}\n")

    proteins = read_input()
    for i, protein in zip(range(len(proteins)), proteins):
        print(f"{i + 1}: {protein}")
    print()

    chosen_protein = ask_integer("Choose a protein: ") - 1
    while chosen_protein < 0 or chosen_protein > len(proteins) - 1:
        chosen_protein = ask_integer("Choose a protein: ") - 1

    print(f">{proteins[chosen_protein]}\n")

    protein, end_time = run_algorithm(algorithms, algorithms[chosen_algorithm], proteins[chosen_protein])

    print(time.strftime('\nElapsed time: %H:%M:%S', time.gmtime(end_time)))
    protein.visualise(proteins[chosen_protein])

    plt.show()
