# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import copy
import numpy as np

from datastructure import Protein, Acid

def random_walk(protein_string, N_tries):
    '''
    Input is a string representing the protein by its amino acids
    Then folds a protein by randomly placing the next amino acid
    Calls a walk function that returns a single folded protein solution
    (future): runs for a given time and remembers the best solution
    '''

    # Use lenght to establish location of the first amino acid
    protein_length = len(protein_string)
    protein = Protein(protein_length)

    # Place the first two amino acids
    location = [protein_length - 1, protein_length - 1]
    protein.add_acid(protein_string[0], location, "")
    protein.acids[location[0], location[1]].add_connection("down")

    location = [location[0] + 1, location[1]]
    protein.add_acid(protein_string[1], location, "up")

    energy_min = 0
    energy_counter = {}

    # Try to fold N_tries proteins
    for i in range(N_tries):
        if (i + 1) % 1000 == 0:
            print(f"{i + 1}th protein folded")

        # Start with a clean protein
        new_protein = copy.deepcopy(protein)
        (solution_found, protein_result) = walk(new_protein, protein_string, location)

        # When a protein is created save its energy
        if solution_found:
            energy = protein_result.energy

            # When its energy lower the protein is saved
            if energy < energy_min:
                energy_min = energy
                protein_min = protein_result
                print(f"found new lowest energy: {energy_min}")

        # dictonary for histogram of solutions
        energy_counter[energy] = energy_counter.get(energy, 0) + 1

    print(f"\nlowest energy conformation was {energy_min}:")
    print(protein_min)
    print(f"\nlowest energy conformation was {energy_min}:")

    return protein_min, energy_counter


def walk(protein, protein_string, previous_location):
    '''
    Input is a protein object, the string representing that object and the location of the previous amino acid
    Folds a protein by randomly placing the next amino acid
    Returns
    '''

    # check possible locations to place new amino acid startin from the third
    for length in range(2, len(protein_string)):
        acid_type = protein_string[length]

        neighbors = protein.neighbors(previous_location)
        possible_sites = {}

        for direction in neighbors:
            location = neighbors[direction]
            acid = protein.acids[location[0], location[1]]

            if acid == 0:
                possible_sites[direction] = location

        if len(possible_sites) > 0:
            divider = 1. / len(possible_sites)

            number = np.random.random()

            for direction, i in zip(possible_sites, range(len(possible_sites))):
                # Determine the maximum random number for this site
                site_probability = (i + 1) * divider

                # Add an acid object to the randomly selected site
                if number <= site_probability:

                    previous_acid = protein.acids[previous_location[0], previous_location[1]]
                    previous_acid.add_connection(direction)

                    location = possible_sites[direction]

                    # Add the acid object to the protein and connect it to the previous acid
                    protein.add_acid(acid_type, location, direction)
                    previous_location = location

                    new_energy = protein.check_energy(location, acid_type)
                    protein.energy += new_energy

                    break

                # This shouldn't happen
                if i == len(possible_sites):
                    print("DIDNT ADD ACID? WHA?")
                    exit(1)

        else:
            break

    # Protein completed, end the random walks
    if protein.length == len(protein_string):
        return (True, protein)

    # Protein failed, retry with a new random walk
    else:
        return(False, protein)
