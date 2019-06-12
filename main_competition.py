# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import os, sys, time
import matplotlib.pyplot as plt

directory = os.path.dirname(os.path.realpath(__file__))

# Add a path to the folders containing the code
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "algorithms"))
sys.path.append(os.path.join(directory, "code", "datastructure"))
sys.path.append(os.path.join(directory, "code", "visualisations"))

# Add a path to the data folder
sys.path.append(os.path.join(directory, "data"))
sys.path.append(os.path.join(directory, "data", "proteins"))

# Add a path to the results folder
sys.path.append(os.path.join(directory, "results"))

# Import auxiliary functions
from user_input import get_choices_competition as get_choices
from run_algorithm_competition import run_algorithm

def parse_data():
    '''
    Parses the  text file containing proteins represented as a string
    '''

    # Opens the file as a list of strings and returns it
    with open("data/proteins.txt", "r") as file:
        file_content = file.read()
        file_lines = file_content.split()

    return file_lines

if __name__ == "__main__":

    # Lists of options for user input
    protein_files = parse_data()
    algorithms = ["Random Walk", "Greedy - Look-ahead", "Beam Search", "Branch-n-Bound - probabilty-based", "Hill Climber"]

    # Get the user's choices
    choices = get_choices(algorithms, protein_files)
    choice_algorithm, choice_protein, dimension, protein_file = choices

    # Run the chosen algorithm
    results = run_algorithm(algorithms, choice_algorithm, choice_protein, dimension)
    protein, energies, start, elapsed_time, parameters = results

    # Determine the total protein solutions evaluated from the energies dictionary
    total_evaluated = sum(energies.values())

    # Convert the unix timestamps to dates and/or hours, minutes and seconds)
    start_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime(start))
    elapsed_HHMMSS = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    print(f"\nAlgorithm finished\nElapsed time: {elapsed_HHMMSS}")

    # Displays and prints the results
    protein.visualise(choice_protein)
    print(f"Lowest energy: {protein.energy}")

    plt.show()
