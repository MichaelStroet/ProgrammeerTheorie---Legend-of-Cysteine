# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
Probability based Branch and Bound
This algorithm will fold a protein by adding new acids to the protein and saving
it if it has the lowest energy found until now. It will try to place all acids
to that protein before exploring other folding options.

This code was inspired by the pseudo-code from Mao Chen & Wen-Qi Huang, 2005.
"""

import copy, sys
import numpy as np

from acid import Acid
from protein import Protein

from dict_average import dict_average

def branch_n_bound(p_string, prob_above_avg, prob_below_avg, dimension, matrix_size):
    '''
    This algorithm will fold a protein using a probability based version of the
    Branch and Bound algorithm.  If the probabilities for pruning are set to 1 and 1,
    this algorithm behaves as a depth-first alhorithm and searches the whole statespace
    for the best solution.
    '''
    # Set global variables
    global protein_string, prob_below_average, prob_above_average, length_total, energy_min_all, energy_min_partial

    prob_below_average = prob_below_avg
    prob_above_average = prob_above_avg
    protein_string = p_string
    length_total = len(protein_string)

    # Initialize global dictionaries
    global energy_counter, matrix_sizes, energy_tracker
    energy_tracker = [{} for i in range(length_total)]
    energy_counter = {}
    matrix_sizes = {}

    # Create a protein object with a specific matrix size
    protein = Protein(matrix_size, dimension)

    # Initialize energy variable that keeps the lowest energy for a complete protein
    energy_min_all = 1

    # Initialize energy variable that keeps the lowest energy for a protein of each length
    energy_min_partial = [0] * length_total

    # Place first two amino acids
    protein.place_first_two(protein_string)
    previous_location = protein.last_acid

    # Call next_acid function to place a new amino acid
    next_acid(protein, previous_location)

    print(energy_tracker)
    print(energy_counter)
    print(sum(energy_counter.values()))

    if not protein_min:
        exit("Error: No protein 'protein_min' to return")
    else:
        return protein_min, energy_counter, matrix_sizes

# Function that places an amino acid
def next_acid(protein, previous_location):
    '''
    Places the next acid and sees how the energy of the (partial) protein compares
    to the average. There is a random element in the decision  to continue adding
    acids to this protein or to prune this branch.
    '''
    global energy_min_all, protein_min

    # Get the possible sites for placing a new acid
    possible_sites = protein.possible_sites(protein.last_acid)

    # If there are possible sites (the protein is not stuck)
    if len(possible_sites) > 0:

        previous_energy = protein.energy

        # Add the acid object to the protein and connect it to the previous acid
        for key_direction in possible_sites:

            amino_acid = protein_string[protein.length]

            previous_acid = protein.acids[previous_location[0], previous_location[1], previous_location[2]]
            previous_acid.add_connection(key_direction)

            location = possible_sites[key_direction]
            protein.add_acid(amino_acid, location, key_direction)

            # Calculate the new energy of the (partial) protein
            protein.new_energy(protein.last_acid)

            # Add the energy to the dictionary counter & calculate the average
            index = protein.length - 1
            energy_tracker[index][protein.energy] = energy_tracker[index].get(protein.energy, 0) + 1

            average_energy = dict_average(energy_tracker[index])

            # Update lowest energy in the partial proteins list
            if protein.energy <= energy_min_partial[index]:
                energy_min_partial[index] = protein.energy

            '''
            Now we will see whether to continue adding acids to this protein
            and update the energy, or prune
            '''

            # If it is the last amino acid of the protein string
            if protein.length == length_total:

                energy = protein.energy
                energy_counter[energy] = energy_counter.get(energy, 0) + 1


                # Update lowest energy among all completed proteins
                if energy < energy_min_all:
                    energy_min_all = energy
                    print(f"New minimum energy found: {energy_min_all}")
                    protein_min = copy.deepcopy(protein)

                # Determine the smallest matrix size needed for this protein
                min_matrix_size = protein.smallest_matrix()
                matrix_sizes[energy] = matrix_sizes.get(energy, {})
                matrix_sizes[energy][min_matrix_size] = matrix_sizes[energy].get(min_matrix_size, 0) + 1

            # If it is a polar amino acid, add a new acid
            elif amino_acid == "P":
                next_acid(protein, location)

            # If it is a hydrophobic or cysteine amino acid, there are several possibilities
            else:

                # If the curent energy is equal to or below the lowest energy of
                # the partial protein, add a new amino acid
                if protein.energy <= energy_min_partial[index]:
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
