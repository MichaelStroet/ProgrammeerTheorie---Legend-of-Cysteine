# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
This algorithm will fold a protein using a greedy algorithm
Greedy in this case means always placing an amino acid at the location that results in the lowest energy
"""

import copy
import random
import numpy as np

from acid import Acid
from protein import Protein

def greedy(protein_string, N_tries, dimension, matrix_size):
    '''
    The input is a string that represents the proteins amino acid sequence
    The output is a protein folded by a greedy algorithm
    '''
    # Create a protein object with a specific matrix size
    protein = Protein(matrix_size, dimension)
    protein_length = len(protein_string)

    # Place the first two amino acids
    protein.place_first_two(protein_string)
    location = protein.last_acid

    energy_min = 0

    energy_counter = {}
    matrix_sizes = {}

    # Try to fold N_tries protein greedy like
    for i in range(N_tries):
        if (i + 1) % 1000 == 0:
            print(f"{i + 1}th protein folded")

        # Remove acids until only the first two are left
        while protein.length > 2:
            protein.remove_acid(0)

        # # Start with a clean protein
        # protein_clean = copy.deepcopy(protein)

        solution_found, protein = greedy_fold(protein, protein_string, protein_length, location)

        # When a protein is created save its energy
        if solution_found:
            energy = protein.energy

            # When its energy is lower than lowest energy found, save the protein
            if energy < energy_min:
                energy_min = energy
                protein_min = copy.deepcopy(protein)
                print(f"found new lowest energy: {energy_min}")

            # Update the dictonary for histogram of solutions
            energy_counter[energy] = energy_counter.get(energy, 0) + 1

            # Determine the smallest matrix size needed for this protein
            min_matrix_size = protein.smallest_matrix()
            matrix_sizes[energy] = matrix_sizes.get(energy, {})
            matrix_sizes[energy][min_matrix_size] = matrix_sizes[energy].get(min_matrix_size, 0) + 1

    return protein_min, energy_counter, matrix_sizes

def greedy_fold(protein, p_string, p_len, loc_current):
    '''
    The input is the protein matrix, string and length
    and the location of the last placed amino acid
    The ouput is a folded protein
    '''

    # For every direction for the following amino acid
    for acid_index in range(2, p_len):

        # Clean slate for location based items
        possible_sites = {}

        # Initialize list of locations with smallest energies
        low_energy_locations = []

        # Initialize the dictionary to keep track of the lowest energies
        energies = {}

        # Check the type of the to be placed acid and its possible locations
        acid_type = p_string[acid_index]

        # Get the possible sites for placing a new acid
        possible_sites = protein.possible_sites(protein.last_acid)

        # Check the energy of every next location
        if len(possible_sites) > 0:
            previous_energy = protein.energy

            # Collect every next location's energy after pseudo placing
            for direction, loc_next in possible_sites.items():
                previous_acid = protein.acids[loc_current[0], loc_current[1], loc_current[2]]
                previous_acid.add_connection(direction)

                # Place the acid, store its energy and remove the acid
                protein.add_acid(acid_type, loc_next, direction)
                energies[direction] = protein.check_energy(loc_next, acid_type)
                protein.remove_acid(previous_energy)

            # Compare energy, choose lowest else random
            energy_mean = np.mean(list(energies.values()))
            for key, value in energies.items():
                if value <= energy_mean:
                    low_energy_locations.append(key)

            # Choose a random direction from the possible locations then add that acid
            loc_choice = random.choice(list(low_energy_locations))
            location = possible_sites[loc_choice]

            # Add the acid object to the protein and connect it to the previous amino acids
            previous_acid.add_connection(loc_choice)
            protein.add_acid(acid_type, location, loc_choice)
            protein.new_energy(protein.last_acid)

            # Change the current location
            loc_current = location

        # Protein incomplete, abort folding
        else:
            break

    # Return the folded protein
    if protein.length == p_len:
        return(True, protein)
    else:
        return(False, protein)
