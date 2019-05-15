"""
initialize dict with 3 first directions: left, down, right at length 2

check energy of 3 options
add option to dict if lower energy than maximum of dictonary
{2left : - 1, 2right : -1, 2down : 0}

take option with lowest length
if length == lowest length?
    go in that direction
        start again
else:
    remove acid to get to that length
"""
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
from truefunctions import opposite
from truefunctions import new_location


def beamsearch(protein_string, dimension):

    global best_nodes, protein_length
    # Use protein length to establish location of first amino acid in a matrix
    protein_length = len(protein_string)
    protein = Protein(protein_length, dimension)

    # Place the first two amino acids
    location = protein.first_acid
    protein.add_acid(protein_string[0], location, "")
    protein.acids[location[0], location[1], location[2]].add_connection("down")

    location = [location[0], location[1] + 1, location[2]]
    protein.add_acid(protein_string[1], location, "down")
    previous_location = location

    energy_min = 0
    energy_counter = {}

    best_nodes = {'2down' : 0, '2left' : 0,'2right' : 0}

    next_acid(protein, protein_string, energy_counter, previous_location)

    return protein_min, energy_counter


# Function that places an amino acid
def next_acid(protein, protein_string, energy_counter, previous_location):

    '''
    Check possible sites for the next amino acid,
    see whether the matrix box left, up & right are empty,
    if so store their locations and direction in a dictionnary
    '''
    global protein_min
    print("*****NEW START******")
    print(previous_location)
    locations = protein.neighbors(previous_location)
    print(locations)
    possible_sites = {}
    energy = {}
    protein_energy ={}
    acid_type = protein_string[protein.length]
    print(acid_type)


    # For each possible location, see if there is already an amino acid
    for direction in locations:
        location = locations[direction]
        acid = protein.acids[location[0],location[1], location[2]]
        if acid == 0:
            possible_sites[direction] = location

    # If there are possible sites (it is not stuck)
    if len(possible_sites) > 0:
        previous_energy = protein.energy
        print("energy: ", protein.energy)

        for direction, site in possible_sites.items():
            acid_type = protein_string[protein.length]
            print("type: ", acid_type)

            previous_acid = protein.acids[previous_location[0], previous_location[1], previous_location[2]]
            previous_acid.add_connection(direction)

            # Acid is placed, energy is stored, acid is removed again
            protein.add_acid(acid_type, site, direction)
            energy[direction] = protein.check_energy(site, acid_type)
            total_energy = previous_energy + protein.check_energy(site, acid_type)
            print("TOTAL energy: ", total_energy)
            protein_energy[direction] = total_energy
            print("length before: ", protein.length)
            protein.remove_acid(previous_energy)
            print("length after: ", protein.length)


        print("Protein_energy: ", protein_energy)
        print("Best_nodes: ", best_nodes)
        print("\n")

        for key, energy_value in protein_energy.items():

            nested_values = list(best_nodes.values())
            print("IN FOR LOOP")
            print("energy value: ", energy_value)

            print("list of best nodes values: ", nested_values)
            minimum_value = min(nested_values)
            maximum_value = max(nested_values)

            print("min: ", minimum_value)
            print("max: ", maximum_value)

            """
                UPDATE BEST NODES
            """
            if energy_value < minimum_value:
                print(energy_value, "smaller than min")
                for node_value in best_nodes:
                    # replace node with biggest energy with the new node
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
                    # replace node with biggest energy with the new node
                    if best_nodes[node_value] == maximum_value:
                        print(f"{best_nodes[node_value]} == {maximum_value}]")
                        print("before: ", best_nodes)
                        #print("key: ", key)
                        #print("node value: ", node_value)
                        print("length: ", protein.length)
                        new_key = str(protein.length) + str(key)
                        print("new key: ", new_key)
                        best_nodes[new_key] = best_nodes.pop(node_value)
                        #print("middle: ", best_nodes)
                        best_nodes[new_key] = energy_value
                        print("after: ",best_nodes)
                        break
            else:
                print("else: ", energy_value)

            print("best_nodes: ", best_nodes)
            print("Protein length: ", protein.length)

            """
                PLACE NEXT AMINO ACID
            """
            for nod in best_nodes:
                print("***nod: ", nod)
                needed_length = re.findall('\d+',nod)
                needed_direction = ''.join(filter(str.isalpha, nod))
                print(needed_direction)

                #next acid in best nodes is at the right length
                if int(needed_length[0]) == protein.length:
                    print("locations: ", locations)
                    print("type: ", acid_type)
                    loc_next = locations[needed_direction]
                    print("loc_next: ", loc_next)
                    print("acid: ", previous_acid)
                    previous_acid.add_connection(needed_direction)
                    protein.add_acid(acid_type, loc_next, needed_direction)
                    protein.energy += best_nodes[nod]
                    best_nodes["99up"] = best_nodes.pop(nod)
                    best_nodes["99up"] = 1
                    previous_location = loc_next
                    protein_min = protein
                    next_acid(protein, protein_string, energy_counter, previous_location)
                    break
                    break

                #next acid in best nodes is not at the right length
                elif len(needed_length) > 0:
                    print("needed length: ", int(needed_length[0]))
                    print("PREVIOUS ACID: ", previous_acid)
                    while protein.length > int(needed_length[0]):
                        print(protein)
                        print("length before: ", protein.length)
                        protein.remove_acid(previous_energy)
                        print(previous_acid.connections)
                        direction_back = previous_acid.connections['previous']
                        print("direction: ", direction_back)
                        location_previous_acid = new_location(previous_location, direction_back, len(protein.acids), len(protein.acids[0]))
                        #print(previous_acid)
                        previous_acid = protein.acids[location_previous_acid[0], location_previous_acid[1], location_previous_acid[2]]
                        print(previous_acid)
                        print("length after: ", protein.length)

                    print(protein)
                    print("locations: ", locations)
                    acid_type = protein_string[protein.length]
                    print("type: ", acid_type)
                    print("previous acid : ", previous_acid)
                    locations = protein.neighbors(previous_acid.position)
                    loc_next = locations[needed_direction]
                    print("loc_next: ", loc_next)
                    previous_acid.add_connection(needed_direction)
                    protein.add_acid(acid_type, loc_next, needed_direction)
                    protein.energy += best_nodes[nod]
                    best_nodes["99up"] = best_nodes.pop(nod)
                    best_nodes["99up"] = 1
                    previous_location = loc_next
                    protein_min = protein
                    print(protein)
                    next_acid(protein, protein_string, energy_counter, previous_location)
                    break
                    break

                else:
                    print("else")
    if protein.length == protein_length:
        return(True, protein)
    else:
        return(False, protein)
