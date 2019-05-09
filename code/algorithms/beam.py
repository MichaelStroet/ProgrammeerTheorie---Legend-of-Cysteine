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
    best_nodes = {'a' : 0, 'b' : 0,'c' : 0}
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

            # Compare energy, lowest else random
            minimum_value = min(protein_energy.values())
            print("energy: ", protein_energy)
            print("values: ",protein_energy.values())
            print("min: ", minimum_value)
            i = 0

            energy_mean = np.mean(list(energy.values()))
            for key, energy_value in energy.items():
                if energy_value <= energy_mean:
                    locs_possible.append(key)

            for key, energy_value in protein_energy.items():

                nested_values = list(best_nodes.values())
                print("list of best nodes values: ", nested_values)
                minimum_value = min(nested_values)
                maximum_value = max(nested_values)

                if energy_value < minimum_value:
                    print(f"{energy_value} < {minimum_value}")
                    for node_value in best_nodes:
                        print(node_value)
                        if best_nodes[node_value] == maximum_value:
                            print("before: ", best_nodes)
                            best_nodes[key] = best_nodes.pop(node_value)
                            best_nodes[key] = energy_value
                            print("after: ",best_nodes)
                            break


                #hop = list(list(best_nodes.values())[i].values())[0]

                # if value < int(hop):
                #         print("replace")
                #         best_nodes[i] = {key : value}
                # print(len(best_nodes))
                if i < len(best_nodes):
                    i+=1
                else:
                    i = 0
                print("i= ",i)

            print("possibilities: ", locs_possible)
            print("best_nodes: ", best_nodes)


            # chooses a random direction from the possible locations then add that acid
            loc_choice = random.choice(list(locs_possible))
            location = locs_next[loc_choice]

            # Add the acid object to the protein and connect it to the previous amino acids
            previous_acid.add_connection(loc_choice)
            protein.add_acid(acid_type, location, loc_choice)
            protein.energy += energy[loc_choice]

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
