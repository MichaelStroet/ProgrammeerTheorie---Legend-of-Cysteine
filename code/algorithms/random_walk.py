# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
Random walk
This script will fold a number of proteins using a random walk.
The location of the next amino acid will be randomly selected.
The algorithm keeps placing amino acids until the protein is complete or if it gets stuck.
"""

import copy
import numpy as np

from acid import Acid
from protein import Protein

def random_walk(protein_string, N_tries, dimension, matrix_size):
    '''
    Runs a random walk algorithm in which N_tries proteins are randomly
    created from a string of amino acid types. The best conformation,
    the one that has the lowest energy, is saved and returned along with
    a dictionary of all N_tries energy counts and the minimal matrix sizes for
    the folded protein.
    '''
    # Create a protein object with a specific matrix size
    protein = Protein(matrix_size, dimension)

    # Place the first two amino acids
    protein.place_first_two(protein_string)
    location = protein.last_acid

    energy_min = 1

    energy_counter = {}
    matrix_sizes = {}

    # Try to fold N_tries proteins
    for i in range(N_tries):

        # Print an update for every 1000th protein
        if (i + 1) % 1000 == 0:
            print(f"{i + 1}th protein folded")

        # Remove acids until only the first two are left
        while protein.length > 2:
            protein.remove_acid(0)

        # Run the next random walk
        solution_found, protein = walk(protein, protein_string, location)

        # When a complete protein has been created, get its energy
        if solution_found:
            energy = protein.energy

            # When its energy is the lowest energy yet, save the protein object
            if energy < energy_min:
                energy_min = energy
                protein_min = copy.deepcopy(protein)
                print(f"New minimum energy found : {energy_min}")

            # Add the energy to a dictionary counter
            energy_counter[energy] = energy_counter.get(energy, 0) + 1

            # Determine the smallest matrix size needed for this protein
            min_matrix_size = protein.smallest_matrix()
            matrix_sizes[energy] = matrix_sizes.get(energy, {})
            matrix_sizes[energy][min_matrix_size] = matrix_sizes[energy].get(min_matrix_size, 0) + 1

    if not protein_min:
        exit("Error: No protein 'protein_min' to return")
    else:
        return protein_min, energy_counter, matrix_sizes


def walk(protein, protein_string, previous_location):
    '''
    Creates a single protein by randomly placing new amino acids. Keeps
    track of the energy of the protein and returns a protein object.
    '''

    # Loop over each amino acid type in the protein string
    for length in range(2, len(protein_string)):
        acid_type = protein_string[length]

        # Get the possible sites for placing a new acid
        possible_sites = protein.possible_sites(protein.last_acid)

        # If a new acid can be placed, randomly place it
        if len(possible_sites) > 0:
            divider = 1. / len(possible_sites)
            random_number = np.random.random()

            # Loop over each possible site
            for direction, i in zip(possible_sites, range(len(possible_sites))):

                # Randomly select the site where to place the new acid
                site_probability = (i + 1) * divider
                if random_number <= site_probability:

                    # Add the "next" connection to the previously-placed acid
                    previous_acid = protein.get_acid(previous_location)
                    previous_acid.add_connection(direction)

                    location = possible_sites[direction]

                    # Add the next acid to the protein object
                    protein.add_acid(acid_type, location, direction)
                    previous_location = location

                    # Check if the new acid has lowered the energy of the protein
                    protein.new_energy(protein.last_acid)

                    break

        # The random walk has gotten itself stuck
        else:
            break

    # Protein created succesfully
    if protein.length == len(protein_string):
        return (True, protein)

    # Protein failed
    else:
        return(False, protein)
