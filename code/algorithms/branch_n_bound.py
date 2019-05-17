# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np
import copy

from acid import Acid
from protein import Protein

from dict_average import dict_average

def branch_n_bound(protein_string, prob_above_avg, prob_below_avg, dimension):

    global protein_str, prob_below_average, prob_above_average, length_total, energy_min_all, energy_min_partial

    prob_below_average = prob_below_avg
    prob_above_average = prob_above_avg
    protein_str = protein_string
    length_total = len(protein_string)

    global energy_counter, matrix_sizes
    energy_counter = {}
    matrix_sizes = {}

    # Create the protein matrix
    protein = Protein(length_total, dimension)

    # Initialize energy variables
    energy_min_all = 0
    energy_min_partial = [0] * length_total

    # Place first two amino acids
    protein.place_first_two(protein_string)
    previous_location = protein.last_acid

    # Call next_acid function to place a new amino acid
    next_acid(protein, previous_location)

    return best_protein, energy_counter, matrix_sizes

# Function that places an amino acid
def next_acid(protein, previous_location):

    global energy_min_all, best_protein

    '''
    Check possible sites for the next amino acid,
    see whether the matrix box left, up & right are empty,
    if so store their locations and direction in a dictionnary
    '''

    # Get the possible sites for placing a new acid
    possible_sites = protein.possible_sites(protein.last_acid)

    # If there are possible sites (the protein is not stuck)
    if len(possible_sites) > 0:

        previous_energy = protein.energy

        # Add the acid object to the protein and connect it to the previous acid
        for key_direction in possible_sites:

            amino_acid = protein_str[protein.length]

            previous_acid = protein.acids[previous_location[0], previous_location[1], previous_location[2]]
            previous_acid.add_connection(key_direction)

            location = possible_sites[key_direction]
            protein.add_acid(amino_acid, location, key_direction)

            # Calculate the new energy of the (partial) protein
            new_energy = protein.check_energy(location, amino_acid)
            protein.energy += new_energy

            # Add the energy to the dictionary counter & calculate the average
            energy_counter[protein.energy] = energy_counter.get(protein.energy, 0) + 1
            average_energy = dict_average(energy_counter)

            # Update lowest energy in the partial proteins list
            if protein.energy <= energy_min_partial[protein.length - 1]:
                energy_min_partial[protein.length - 1] = protein.energy
                #print("NEW min partial= ",energy_min_partial[protein.length - 1])

            '''
            Now we will see whether to continue adding acids to this protein or
            and update the energy, or prune
            '''

            # If it is the last amino acid of the protein string
            if protein.length == length_total:
                energy = protein.energy

                # Update lowest energy among all completed proteins
                if energy < energy_min_all:
                    energy_min_all = energy
                    print("New minimum energy found : ",energy_min_all)
                    best_protein = copy.deepcopy(protein)

                min_matrix_size = protein.smallest_matrix()

                matrix_sizes[energy] = matrix_sizes.get(energy, {})
                matrix_sizes[energy][min_matrix_size] = matrix_sizes[energy].get(min_matrix_size, 0) + 1


            # If it is a polar amino acid, add a new acid
            elif amino_acid == "P":
                next_acid(protein, location)

            # If it is a hydrophobic or cysteine amino acid, there are several possibilities
            else:
                '''
                if the curent energy is equal to or below the lowest energy of
                the partial protein, add a new amino acid
                '''
                if protein.energy <= energy_min_partial[protein.length - 1]:
                    next_acid(protein, location)

                # If the curent energy is below the average energy of
                # all partial proteins up to now, compute a random number between
                # 0 and 1 and if it is below the probability threshold, add a new
                # amino acid
                elif protein.energy <= average_energy:
                    r = np.random.random()

                    if r <= prob_below_average:
                        next_acid(protein, location)

                # If the curent energy is bigger the average energy of
                # all partial proteins up to now, compute a random number between
                # 0 and 1 and if it is below the probability threshold, add a new
                # amino acid
                else:
                    r = np.random.random()
                    if r <= prob_above_average:
                        next_acid(protein, location)

            # Remove the acid before continuing
            protein.remove_acid(previous_energy)


if __name__ == "__main__":
    branch_n_bound("HHPHHHPH")



'''
Pseudo-code for the Branch & Bound algorithm inspired from:

Mao Chen, Wen-Qi Huang,
A Branch and Bound Algorithm for the Protein Folding Problem in the HP Lattice Model,
Genomics, Proteomics & Bioinformatics,
Volume 3, Issue 4,
2005,
Pages 225-230
'''
