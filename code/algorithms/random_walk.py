# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import copy
import numpy as np

from acid import Acid
from protein import Protein

def random_walk(protein_string, N_tries, dimension):
    '''
    Runs a random walk algorithm in which N_tries proteins are randomly
    created from a string of amino acid types. The best conformation,
    the one that has the lowest energy, is saved and returned along with
    a dictionary of all N_tries energy counts.
    '''

    # Use lenght to establish location of the first amino acid
    protein_length = len(protein_string)
    protein = Protein(protein_length, dimension)

    # Place the first amino acid
    location = protein.first_acid
    protein.add_acid(protein_string[0], location, "")
    protein.get_acid(location).add_connection("down")

    # Place the second amino acid below the first
    location = [location[0], location[1] + 1, location[2]]
    protein.add_acid(protein_string[1], location, "up")

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

        # When a complete protein has been created, get it's energy
        if solution_found:
            energy = protein.energy

            # When its energy is the lowest energy yet, save the protein object
            if energy < energy_min:
                energy_min = energy
                protein_min = copy.deepcopy(protein)
                print(f"Found new lowest energy: {energy_min}")

            # Add the energy to a dictionary counter
            energy_counter[energy] = energy_counter.get(energy, 0) + 1

            min_matrix_size = protein.smallest_matrix()

            matrix_sizes[energy] = matrix_sizes.get(energy, {})
            matrix_sizes[energy][min_matrix_size] = matrix_sizes[energy].get(min_matrix_size, 0) + 1

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
        possible_sites = protein.possible_sites()
        
        # If a new acid can be placed, randomly place said acid
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
                    new_energy = protein.check_energy(location, acid_type)
                    protein.energy += new_energy

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
