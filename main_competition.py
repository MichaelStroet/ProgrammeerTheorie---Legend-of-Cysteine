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
from run_algorithm import run_algorithm

def parse_data():
    '''
    Parses the  text file containing proteins represented as a string
    '''

    # Opens the file as a list of strings and returns it
    with open("data/proteins.txt", "r") as file:
        file_content = file.read()
        file_lines = file_content.split()

    return file_lines

def save_result(protein, protein_string, protein_file, elapsed_HHMMSS, algorithm, parameters):
    file_path = f"data/folded_proteins/{protein_file}"

    if not os.path.isfile(file_path):
        file_empty = True
    else:
        with open(file_path, "r") as file:
            if os.stat(file_path).st_size == 0:
                file_empty = True
            else:
                file_empty = False
                file_lines = file.readlines()
                file_energy = int(file_lines[10][10:-1])

    # Check if an existing file already has a lower or equal energy
    if not file_empty:
        if protein.energy >= file_energy:
            return f"Protein energy ({protein.energy}) is larger or equal to the file energy ({file_energy}. '{protein_file}' unchanged)"

    # Create/Update the text file
    with open(file_path, "w") as file:
        file.write("# An afternoon of algorithmic protein folding - competition\n\n")

        file.write("# The Legend of Cysteine:\n")
        file.write("# Ruby Bron\n")
        file.write("# Michael Stroet\n")
        file.write("# Sophie Stiekema\n\n")

        file.write(f"{protein_string}\n")
        file.write(f"{protein.competition_format()}\n\n")

        file.write(f"# Energy: {protein.energy}\n")
        file.write(f"# Elapsed time: {elapsed_HHMMSS}\n")
        file.write(f"# Algorithm: {algorithm}\n\n")

        file.write("# Parameters:\n")

        for parameter in parameters.items():
            if len(parameter[1]) > 0:
                file.write(f"# {parameter[0]}: {parameter[1]}\n")

        return f"Created/Updated '{protein_file}' in data/folded_proteins"

if __name__ == "__main__":

    # Lists of options for user input
    protein_files = parse_data()
    algorithms = ["Random Walk", "Greedy - Look-ahead", "Beam Search", "Branch-n-Bound - probabilty-based", "Hill Climber"]

    # Get the user's choices
    choices = get_choices(algorithms, protein_files)
    choice_algorithm, choice_protein, dimension, protein_file = choices

    # Run the chosen algorithm
    results = run_algorithm(algorithms, choice_algorithm, choice_protein, dimension)
    protein, energies, matrix_sizes, start, elapsed_time, parameters = results

    # Determine the total protein solutions evaluated from the energies dictionary
    total_evaluated = sum(energies.values())

    # Convert the unix timestamps to dates and/or hours, minutes and seconds)
    start_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime(start))
    elapsed_HHMMSS = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    print(f"\nAlgorithm finished\nElapsed time: {elapsed_HHMMSS}")

    print(save_result(protein, choice_protein, protein_file, elapsed_HHMMSS, choice_algorithm, parameters))

    # Displays and prints the results
    protein.visualise(choice_protein)
    print(f"Lowest energy: {protein.energy}")

    plt.show()
