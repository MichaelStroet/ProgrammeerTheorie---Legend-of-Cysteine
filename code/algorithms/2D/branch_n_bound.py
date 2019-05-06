# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np
import copy

from acid import Acid
from protein import Protein

'''
09/04
ಠ_ಠ
16/04
 new version
 18/04
 It works!
 22/04
 Added more comments
'''

def branch_n_bound(protein_string, prob_above_avg, prob_below_avg):

    global protein_str, prob_below_average, prob_above_average, length_total, energy_min_all, energy_min_partial
    prob_below_average = prob_below_avg
    prob_above_average = prob_above_avg
    protein_str = protein_string
    length_total = len(protein_string)

    # Create the protein matrix
    protein = Protein(length_total)

    # Initialize variables
    energy_min_all = 0
    energy_min_partial = [0] * length_total
    energy_counter = {}

    # Place first amino acid[row, column]
    start_index = int((len(protein.acids) - 1) / 2.)
    start_location = [start_index, start_index]
    protein.add_acid(protein_string[0], start_location,"")
    protein.acids[start_location[0], start_location[1]].add_connection("down")

    # Place second amino acid underneath first
    previous_location = start_location
    location = [previous_location[0] + 1, previous_location[1]]
    protein.add_acid(protein_string[1], location, "down")
    #protein.acids[location[0], location[1]].add_connection("up")
    previous_location = location

    # Call next_acid function to place a new amino acid
    next_acid(protein, energy_counter, previous_location)

    print("\nMinumum energy found per length: ",energy_min_partial)
    print("Minumum energy found ",energy_min_all)
    print(best_protein)
    return best_protein

# Function for calculating the average of the values in a dictionary
def dict_average(dict):
    sum_energy = 0
    for key, value in dict.items():
        sum_energy += key * value
    values = dict.values()
    return sum_energy / sum(values)

# Function that places an amino acid
def next_acid(protein, energy_counter, previous_location):

    global energy_min_all, best_protein

    '''
    Check possible sites for the next amino acid,
    see whether the matrix box left, up & right are empty,
    if so store their locations and direction in a dictionnary
    '''

    locations = protein.neighbors(previous_location)
    possible_sites = {}

    # For each possible location, see if there is already an amino acid
    for direction in locations:
        location = locations[direction]
        acid = protein.acids[location[0],location[1]]
        if acid == 0:
            possible_sites[direction] = location

    # If there are possible sites (it is not stuck)
    if len(possible_sites) > 0:

        previous_energy = protein.energy

        # Add the acid object to the protein and connect it to the previous acid
        for key_direction in possible_sites:

            amino_acid = protein_str[protein.length]

            previous_acid = protein.acids[previous_location[0], previous_location[1]]
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

                # Update lowest energy among all completed proteins
                if protein.energy < energy_min_all:
                    energy_min_all = protein.energy
                    print("New minimum energy found : ",energy_min_all)
                    best_protein = copy.deepcopy(protein)
                    # print(best_protein)
                    # print("\nMinumum partial energy : ",energy_min_partial)

            # If it is a polar amino acid, add a new acid
            elif amino_acid == "P":
                next_acid(protein, energy_counter, location)

            # If it is a hydrophobic or cysteine amino acid, there are several possibilities
            else:
                '''
                if the curent energy is equal to or below the lowest energy of
                the partial protein, add a new amino acid
                '''
                if protein.energy <= energy_min_partial[protein.length - 1]:
                    next_acid(protein, energy_counter, location)

                # If the curent energy is below the average energy of
                # all partial proteins up to now, compute a random number between
                # 0 and 1 and if it is below the probability threshold, add a new
                # amino acid
                elif protein.energy <= average_energy:
                    r = np.random.random()

                    if r <= prob_below_average:
                        next_acid(protein, energy_counter, location)

                # If the curent energy is bigger the average energy of
                # all partial proteins up to now, compute a random number between
                # 0 and 1 and if it is below the probability threshold, add a new
                # amino acid
                else:
                    r = np.random.random()
                    if r <= prob_above_average:
                        next_acid(protein, energy_counter, location)

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
