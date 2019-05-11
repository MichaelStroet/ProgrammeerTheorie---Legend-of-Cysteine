# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
This algorithm will fold a protein using a beam search algorithm
"""

import copy
import random
import numpy as np
import re

from trueacid import Acid
from trueprotein import Protein

def beamsearch(protein_string, N_tries, dimension):
    '''
    The input is a string that represents the proteins amino acid sequence
    The output is a protein folded by a greedy algorithm
    '''

    # Use protein length to establish location of first amino acid in a matrix
    protein_length = len(protein_string)
    protein = Protein(protein_length, dimension)

    # Place the first two amino acids
    location = protein.first_acid
    protein.add_acid(protein_string[0], location, "")
    protein.acids[location[0], location[1], location[2]].add_connection("down")

    location = [location[0], location[1] + 1, location[2]]
    protein.add_acid(protein_string[1], location, "down")

    energy_min = 0
    energy_counter = {}
    best_nodes = {'down2' : 0, 'left3' : 0,'right2' : 0}
    print(best_nodes)


    # Try to fold N_tries protein greedy like
    for i in range(N_tries):
        if (i + 1) % 1000 == 0:
            print(f"{i + 1}th protein folded")

        # Remove acids until only the first two are left
        while protein.length > 2:
            protein.remove_acid(0)

        # # Start with a clean protein
        # protein_clean = copy.deepcopy(protein)

        solution_found, protein = greedy_fold(protein, protein_string, protein_length, location, best_nodes)

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

    return protein_min, energy_counter

def greedy_fold(protein, p_string, p_len, loc_current, best_nodes):
    '''
    The input is the protein matrix, string and length
    and the location of the last placed amino acid
    The ouput is a folded protein
    '''

    # Every direction for the following amino acid
    for acid_index in range(2, p_len):
        print("acid_index: :", acid_index)

        # Clean slate for location based items
        locs_next = {}
        locs_possible = []
        energy = {}
        protein_energy = {}

        # Check the type of the amino acid to be placed and its possible locations
        acid_type = p_string[acid_index]
        directions = protein.neighbors(loc_current)

        # Check if any directions are a valid location for amino acid placement
        for direction, loc_new in directions.items():

            # Remember the next possible locations
            if protein.acids[loc_new[0], loc_new[1], loc_new[2]] == 0:
                locs_next[direction] = loc_new

        # Check the energy of every next location
        if len(locs_next) > 0:
            previous_energy = protein.energy

            # Every next location's energy is collected after pseudo placing
            for direction, loc_next in locs_next.items():
                previous_acid = protein.acids[loc_current[0], loc_current[1], loc_current[2]]
                previous_acid.add_connection(direction)

                # Acid is placed, energy is stored, acid is removed again
                protein.add_acid(acid_type, loc_next, direction)
                energy[direction] = protein.check_energy(loc_next, acid_type)
                total_energy = previous_energy + protein.check_energy(loc_next, acid_type)
                print(total_energy)
                protein_energy[direction] = total_energy
                protein.remove_acid(previous_energy)


            minimum_value = min(protein_energy.values())
            #print("energy: ", protein_energy)
            print("values of each direction: ",protein_energy.values())
            #print("min protein: ", minimum_value)

            energy_mean = np.mean(list(energy.values()))
            for key, energy_val in energy.items():
                if energy_val <= energy_mean:
                    locs_possible.append(key)

            for key, energy_value in protein_energy.items():

                nested_values = list(best_nodes.values())
                print("list of best nodes values: ", nested_values)
                minimum_value = min(nested_values)
                maximum_value = max(nested_values)

                print("energy value: ", energy_value)
                print("min: ", minimum_value)
                print("max: ", maximum_value)

                #if energy_value < minimum_value:
                #print(f"{energy_value} < {minimum_value}")
                if energy_value < minimum_value:
                    print(energy_value, "smaller than min")
                    for node_value in best_nodes:
                        if best_nodes[node_value] == maximum_value:
                            print(f"{best_nodes[node_value]} == {maximum_value}]")
                            print("before: ", best_nodes)
                            #print("key: ", key)
                            #print("node value: ", node_value)
                            print("length: ", protein.length)
                            new_key = str(protein.length) + str(key)
                            best_nodes[new_key] = best_nodes.pop(node_value)
                            #print("middle: ", best_nodes)
                            best_nodes[new_key] = energy_value
                            print("after: ",best_nodes)
                            break

                elif energy_value < maximum_value:
                    print(energy_value, "smaller than max")
                    for node_value in best_nodes:
                        if best_nodes[node_value] == maximum_value:
                            print(f"{best_nodes[node_value]} == {maximum_value}]")
                            print("before: ", best_nodes)
                            #print("key: ", key)
                            #print("node value: ", node_value)
                            print("length: ", protein.length)
                            new_key = str(protein.length) + str(key)
                            best_nodes[new_key] = best_nodes.pop(node_value)
                            #print("middle: ", best_nodes)
                            best_nodes[new_key] = energy_value
                            print("after: ",best_nodes)
                            break
                else:
                    print("else: ", energy_value)

            print("best_nodes: ", best_nodes)
            print("length: ", protein.length)

            #nodes_needed = {}
            for nd in best_nodes:
                print("nd: ", nd)
                needed_length = re.findall('\d+',nd)
                needed_direction = ''.join(filter(str.isalpha, nd))
                #nodes_needed[needed_length] = needed_direction
                if len(needed_length) > 0:
                    while protein.length > int(needed_length[0]):
                        print(protein)
                        protein.remove_acid(energy_value)
                        acid_index -=1
                        acid_type = p_string[acid_index]
                        print("curr: ", loc_current)
                        print("acid :", protein.acids)
                        directions = protein.neighbors(loc_current)

                        # Check if any directions are a valid location for amino acid placement
                        for direction, loc_new in directions.items():

                            # Remember the next possible locations
                            if protein.acids[loc_new[0], loc_new[1], loc_new[2]] == 0:
                                locs_next[direction] = loc_new

                    previous_acid.add_connection(needed_direction)
                    print(locs_next)
                    location = locs_next[needed_direction]
                    protein.add_acid(acid_type, location, needed_direction)
                    protein.energy += energy[needed_direction]
                    break

                    # Change the current location
                    loc_current = location
                else:
                    loc_choice = random.choice(list(locs_possible))
                    location = locs_next[loc_choice]

                    # Add the acid object to the protein and connect it to the previous amino acids
                    previous_acid.add_connection(loc_choice)
                    protein.add_acid(acid_type, location, loc_choice)
                    protein.energy += energy[loc_choice]

                    # Change the current location
                    loc_current = location
                    break


                    print(protein.length)

            print("possibilities: ", locs_possible)

            #
            # # chooses a random direction from the possible locations then add that acid
            # loc_choice = random.choice(list(locs_possible))
            # location = locs_next[loc_choice]
            #
            # # Add the acid object to the protein and connect it to the previous amino acids
            # previous_acid.add_connection(loc_choice)
            # protein.add_acid(acid_type, location, loc_choice)
            # protein.energy += energy[loc_choice]
            #
            # # Change the current location
            # loc_current = location

        # Protein incomplete, abort folding
        else:
            break

    # Return the folded protein
    if protein.length == p_len:
        return(True, protein)
    else:
        return(False, protein)


# Function that places an amino acid
def next_acid(protein, energy_counter, previous_location):

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
        acid = protein.acids[location[0],location[1], location[2]]
        if acid == 0:
            possible_sites[direction] = location

    # If there are possible sites (it is not stuck)
    if len(possible_sites) > 0:

        previous_energy = protein.energy

        # Add the acid object to the protein and connect it to the previous acid
