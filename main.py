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

# Import visualisation functions
from minimal_sizes import plot_matrix_sizes

# Import auxiliary functions
from user_input import get_choices
from run_algorithm import run_algorithm

def parse_data():
    '''
    Parses the  text file containing proteins represented as a string
    '''

    # Opens the file as a list of strings and returns it
    with open("data/input.txt", "r") as f:
        file_content = f.read()
        file_lines = file_content.split()

    return file_lines

if __name__ == "__main__":

    # Lists of options for user input
    save_results = ["Yes", "No"]
    show_results = ["Yes", "No"]
    dimensions = ["1D", "2D", "3D"]
    algorithms = ["random walk", "greedy", "greedy - look-ahead", "beam search", "branch-n-bound - probabilty-based"]
    proteins = parse_data()

    # Get the user's choices
    choices = get_choices(save_results, show_results, dimensions, algorithms, proteins)
    choice_save, choice_show, choice_dimension, choice_algorithm, choice_protein = choices

    # Run the chosen algorithm
    results = run_algorithm(algorithms, choice_algorithm, choice_protein, choice_dimension)

    if len(results) == 4:
        protein, energies, matrix_sizes, elapsed_time = results

        # Saves the results to file
        if save_results == "Yes":
            protein.visualise(choice_protein)
            plot_matrix_sizes(matrix_sizes, protein.matrix_size)

        # Displays and prints the results
        if choice_show == "Yes":
            protein.visualise(choice_protein)
            plot_matrix_sizes(matrix_sizes, protein.matrix_size)

            print(time.strftime('\nElapsed time: %H:%M:%S', time.gmtime(elapsed_time)))
            print(f"Energies:\n{energies}")

            plt.show()

    else:
        print(f"Error: Missing variable(s) in [protein, energies, matrix_sizes, elapsed_time]:")
        for variable in results:
            print(f"{variable}\n")

        exit(1)
