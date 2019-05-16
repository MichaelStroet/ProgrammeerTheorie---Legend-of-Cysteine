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

def greedy(protein_string, look_aheads, N_tries, dimension):
    '''
    The input is a string that represents the proteins amino acid sequence
    The output is a protein folded by a greedy look_ahead algorithm
    '''

    # Use protein length to establish location of first amino acid in a matrix
    protein = Protein(len(protein_string), dimension)

    # Place the first two amino acids
    location = protein.first_acid
    protein.add_acid(protein_string[0], location, "")
    protein.get_acid(location).add_connection("down")

    location = [location[0], location[1] + 1, location[2]]
    protein.add_acid(protein_string[1], location, "down")

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

        solution_found, protein = greedy_fold(protein, protein_string, look_aheads)

        # When a protein is created save its energy
        if solution_found:
            energy = protein.energy

            # When its energy is lower than lowest energy found, the protein is saved
            if energy < energy_min:
                energy_min = energy
                protein_min = copy.deepcopy(protein)
                print(f"found new lowest energy: {energy_min}")

            # dictonary for histogram of solutions
            energy_counter[energy] = energy_counter.get(energy, 0) + 1

            min_matrix_size = protein.smallest_matrix()

            matrix_sizes[energy] = matrix_sizes.get(energy, {})
            matrix_sizes[energy][min_matrix_size] = matrix_sizes[energy].get(min_matrix_size, 0) + 1


    return protein_min, energy_counter, matrix_sizes

def look_ahead(protein, look_aheads, protein_string, acid_index):
    '''

    '''
    # If there are no more steps to be taken, return the current energy
    if look_aheads < 1 or acid_index >= len(protein_string):
        return protein.energy

    # Check the type of the next acid
    acid_type = protein_string[acid_index]

    # Get the possible sites for placing a new acid
    possible_sites = protein.possible_sites(protein.last_acid)

    energies = {}

    # Check the energy of every next possible location
    if len(possible_sites) > 0:
        previous_energy = protein.energy

        # Determine the lowest energy of each possible site with all look-aheads included
        for direction, loc_next in possible_sites.items():
            previous_acid = protein.get_acid(protein.last_acid)
            previous_acid.add_connection(direction)

            # Place the first acid
            protein.add_acid(acid_type, loc_next, direction)
            protein.new_energy(protein.last_acid)

            # Determine the lowest energy of the steps further ahead
            energy = look_ahead(protein, look_aheads - 1, protein_string, acid_index + 1)

            # Add the lowest energy to the energies dictionary
            energies[direction] = energy

            # Return the matrix to its previous state
            protein.remove_acid(previous_energy)

        return min(energies.values())

    # Protein incomplete, abort folding and return energy +1
    else:
        return 1

def greedy_fold(protein, protein_string, look_aheads):
    '''
    The input is the protein matrix, string and length
    and the location of the last placed amino acid
    The ouput is a folded protein
    '''

    # Every direction for the following amino acid
    for acid_index in range(2, len(protein_string)):

        # Check the type of the next acid
        acid_type = protein_string[acid_index]

        locs_possible = []

        # Get the possible sites for placing a new acid
        possible_sites = protein.possible_sites(protein.last_acid)

        energies = {}

        # Check the energy of every next location
        if len(possible_sites) > 0:
            previous_energy = protein.energy

            # Determine the lowest energy of each possible site with all look-aheads included
            for direction, location in possible_sites.items():
                previous_acid = protein.get_acid(protein.last_acid)
                previous_acid.add_connection(direction)

                # Place the first acid and determine the new energy
                protein.add_acid(acid_type, location, direction)
                protein.new_energy(location)

                # Determine the lowest energy of the first acid and the steps further ahead
                energy = look_ahead(protein, look_aheads, protein_string, acid_index + 1)

                # Add the lowest energy to the energies dictionary
                energies[direction] = energy

                # Return the matrix to its previous state
                protein.remove_acid(previous_energy)

            # Compare energy, lowest else random
            energy_mean = np.mean(list(energies.values()))
            for key, value in energies.items():
                if value <= energy_mean:
                    locs_possible.append(key)

            # chooses a random direction from the possible locations then adds that acid
            loc_choice = random.choice(list(locs_possible))
            location = possible_sites[loc_choice]

            # Add the acid object to the protein and connect it to the previous amino acids
            previous_acid.add_connection(loc_choice)
            protein.add_acid(acid_type, location, loc_choice)
            protein.new_energy(location)

        # Protein incomplete, abort folding
        else:
            break

    # Return the folded protein
    if protein.length == len(protein_string):
        return(True, protein)
    else:
        return(False, protein)