# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import copy
import numpy as np
import matplotlib.pyplot as plt

from datastructure import Protein, Acid

def random_walk(protein_string):
    '''
    Input is a string representing the protein by its amino acids
    Then folds a protein by randomly placing the next amino acid
    Calls a walk function that returns a single folded protein solution
    (future): runs for a given time and remembers the best solution
    '''

    # Use lenght to establish location of the first amino acid 
    protein_length = len(protein_string)
    protein = Protein(protein_length)

    location = [protein_length - 1, protein_length - 1]

    # Place the first two amino acids
    protein.add_acid(protein_string[0], location, "")
    location = [location[0] + 1, location[1]]
    protein.add_acid(protein_string[1], location, "")

    # Keep folding proteins until one is completed
    solution_found = False
    while not solution_found:
        new_protein = copy.deepcopy(protein)
        (solution_found, protein_result) = walk(new_protein, protein_string, location)


def walk(protein, protein_string, previous_location):
    '''
    Input is a protein object, the string representing that object and the location of the previous amino acid
    Folds a protein by randomly placing the next amino acid
    Returns 
    '''

    # check possible locations to place new amino acid startin from the third
    for length in range(2, len(protein_string)):
        acid_type = protein_string[length]

        location_bottom = [previous_location[0] + 1, previous_location[1]]
        location_top = [previous_location[0] - 1, previous_location[1]]
        location_right = [previous_location[0], previous_location[1] + 1]
        location_left = [previous_location[0], previous_location[1] - 1]

        locations = [location_bottom, location_top, location_right, location_left]

        possible_sites = []

        for loc in locations:
            if protein.acids[loc[0], loc[1]] == 0:
                possible_sites.append(loc)

        print("possible sites are",possible_sites)
        if len(possible_sites) > 0:
            divider = 1. / len(possible_sites)

            number = np.random.random()
            #print(number)

            for i in range(len(possible_sites)):
                # Determine the maximum random number for this site
                site_probability = (i + 1) * divider

                # Add an acid object to the randomly selected site
                if number <= site_probability:
                    location = possible_sites[i]

                    protein.add_acid(acid_type, location, "")
                    previous_location = location

                    test = protein.check_energy(location)
                    print(test)
                    break

                # This shouldn't happen
                if i == len(possible_sites):
                    print("DIDNT ADD ACID? WHA?")
                    exit(1)

        else:
            break

    # Protein completed, end the random walks
    if protein.length == len(protein_string):
        print(protein)
        return (True, protein)

    # Protein failed, retry with a new random walk
    else:
        print("FAILED")
        return(False, protein)
