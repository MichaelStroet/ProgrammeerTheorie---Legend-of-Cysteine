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

# Add a path to the results folder
sys.path.append(os.path.join(directory, "results"))

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
    with open("data/input.txt", "r") as file:
        file_content = file.read()
        file_lines = file_content.split()

    return file_lines

if __name__ == "__main__":

    # Lists of options for user input
    save_results = ["Yes", "No"]
    show_results = ["Yes", "No"]
    dimensions = ["1D", "2D", "3D"]
    algorithms = ["Random Walk", "Greedy", "Greedy - Look-ahead", "Beam Search", "Branch-n-Bound - probabilty-based", "Hill Climber"]
    proteins = parse_data()

    # Get the user's choices
    choices = get_choices(save_results, show_results, dimensions, algorithms, proteins)
    choice_save, choice_show, choice_dimension, choice_algorithm, choice_protein = choices

    # Run the chosen algorithm
    results = run_algorithm(algorithms, choice_algorithm, choice_protein, choice_dimension)
    protein, energies, matrix_sizes, start, elapsed_time, parameters = results

    # Convert the unix timestamps to dates and/or hours, minutes and seconds)
    start_time = time.strftime("%H:%M:%S %d-%m-%Y", time.gmtime(start))
    elapsed_HHMMSS = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    print(f"\nAlgorithm finished\nElapsed time: {elapsed_HHMMSS}")

    # Saves the results to a csv file and saves the figures as png files
    if choice_save == "Yes":

        with open("results/results.csv", "a", encoding = "utf-8") as file:
            row = ""
            row += f"{start_time},"                 # Start time
            row += f"{elapsed_HHMMSS},"             # Elapsed time
            row += f"{choice_dimension},"           # Dimension
            row += f"{choice_protein},"             # Protein
            row += f"{choice_algorithm},"           # Algorithm
            row += f"{protein.energy},"             # Lowest energy
            row += f"{parameters['Matrix size']},"  # Matrix size
            row += f"{parameters['Iterations']},"   # Iterations
            row += f"{parameters['Look-aheads']},"  # Look-aheads
            row += f"{parameters['Prob. below']},"  # Probability below average
            row += f"{parameters['Prob. above']},"  # Probability above average
            row += f"{parameters['Beam width']},"   # Beam width
            row += f"{parameters['???']}"          # Hillclimber parameter(s)?
            row += "\n"

            file.write(row)

            protein.visualise(choice_protein)
            plt.savefig(f"results/figures/testfig.png")
            plt.clf()

            plot_matrix_sizes(matrix_sizes, protein.matrix_size)
            plt.savefig(f"results/figures/testmatrices.png")
            plt.clf()

    # Displays and prints the results
    if choice_show == "Yes":
        protein.visualise(choice_protein)
        plot_matrix_sizes(matrix_sizes, protein.matrix_size)
        print(f"Energies:\n{energies}")
        print(f"Matrix sizes:\n{matrix_sizes}")

        plt.show()
