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
import operator
import heapq

from acid import Acid
from protein import Protein
from functions import opposite
from functions import new_location
from operator import itemgetter


def beamsearch(pr_string, width, dimension):

    global best_nodes, protein_length, protein_string, energy_counter, beam_list, proteins, B_width
    protein_string = pr_string
    B_width = width
    # Use protein length to establish location of first amino acid in a matrix
    protein_length = len(protein_string)
    protein = Protein(protein_length, dimension)

    # Place the first two amino acids
    location = protein.first_acid
    protein.add_acid(protein_string[0], location, "")
    protein.acids[location[0], location[1], location[2]].add_connection("down")

    location = [location[0], location[1] + 1, location[2]]
    protein.add_acid(protein_string[1], location, "down")
    previous_location = [location]

    energy_min = 0
    energy_counter = {}
    proteins = {}

    for i in range(B_width):
        proteins[i] = protein
    #print(proteins)

    beam_list = [0] * B_width

    next_layer(protein, previous_location)

    # for i in range(len(proteins)):
    #     print(proteins[i].energy)
    protein_min = proteins[0]
    energy_min = protein_min.energy
    #print(protein_min.energy)

    return protein_min, energy_min

def next_layer(the_protein, prev_location):
    '''
    Check possible sites for the next amino acid,
    see whether the matrix box left, up & right are empty,
    if so store their locations and direction in a dictionnary
    '''

    global protein_min

    prev_locs = []
    list = []
    temporary_proteins = [0] * B_width
    #print("BEAM: ", beam_list)
    acid_type = protein_string[the_protein.length]

    #print("PREVIOUS LOCATION: ", prev_location)
    beam_possibilities = {}

    for i in range(len(prev_location)):
        protein_energy ={}
        possible_sites = {}
        energy = {}


        previous_location = prev_location[i]
        #print(previous_location)
        if any(proteins):
            #print(proteins[i])
            protein = proteins[i]
        else:
            protein = the_protein
        # if any(beam_list):

            # for j in range(len(beam_list)):
            #     for k in range(len(beam_list[j])):
            #         k = 1
            #         print("list : ", beam_list[0][1])
            #         print(beam_list[j][k])
            #         dir = beam_list[j][k]
            #         loc = new_location(previous_location, dir, len(protein.acids), len(protein.acids[0]))
            #         previous_acid = protein.acids[previous_location[0], previous_location[1], previous_location[2]]
            #         print(previous_acid)
            #         previous_acid.add_connection(dir)
            #         protein.add_acid(acid_type, loc, dir)
            #         print(protein)
            #         print(protein.check_energy(loc, acid_type))

        locations = protein.neighbors(previous_location)

        # For each possible location, see if there is already an amino acid
        for direction in locations:
            location = locations[direction]
            acid = protein.acids[location[0],location[1], location[2]]
            if acid == 0:
                possible_sites[direction] = location

        # If there are possible sites (it is not stuck)
        if len(possible_sites) > 0:
            previous_energy = protein.energy

            for direction, site in possible_sites.items():

                acid_type = protein_string[protein.length]

                previous_acid = protein.acids[previous_location[0], previous_location[1], previous_location[2]]
                #print(previous_acid)
                previous_acid.add_connection(direction)

                # Acid is placed, energy is stored, acid is removed again
                protein.add_acid(acid_type, site, direction)
                energy[direction] = protein.check_energy(site, acid_type)
                total_energy = previous_energy + protein.check_energy(site, acid_type)
                #print("TOTAL energy: ", total_energy)
                protein_energy[direction] = total_energy
                direction = str(i) + str(direction)
                beam_possibilities[direction] = total_energy
                protein.remove_acid(previous_energy)
            sorted_possibilities = sorted(beam_possibilities.items(), key=operator.itemgetter(1))
            beam_possibilities = dict(sorted_possibilities)
            #print(sorted_possibilities)
            #print(beam_possibilities)
            list.append(beam_possibilities)
            #beam_possibilities["low"] = -1
            #beam_possibilities["high"] = -2

    #print("POSSIBILITIES: ",beam_possibilities)

    i = 0
    #print(sorted(beam_possibilities, key=beam_possibilities.get))

    for key in sorted(beam_possibilities, key=beam_possibilities.get)[:B_width]:
        #print(key, beam_possibilities[key])
        needed_protein = int(re.findall('\d+',key)[0])
        #print(needed_protein)
        needed_direction = ''.join(filter(str.isalpha, key))
        #print(needed_direction)
        previous_loc = prev_location[needed_protein]
        needed_locations = protein.neighbors(previous_loc)
        needed_loc = needed_locations[needed_direction]
        prev_locs.append(needed_loc)
        #print(needed_protein)
        #print(beam_list[i])
        temporary_proteins[i] = copy.deepcopy(proteins[needed_protein])
        #print(temporary_proteins[i])
        prev_acid = temporary_proteins[i].acids[previous_loc[0], previous_loc[1], previous_loc[2]]
        #print(prev_acid)
        prev_acid.add_connection(needed_direction)

        temporary_proteins[i].add_acid(acid_type, needed_loc, needed_direction)
        needed_energy = temporary_proteins[i].check_energy(needed_loc, acid_type)
        temporary_proteins[i].energy += needed_energy
        #print(temporary_proteins[i])

        beam_list[i] = beam_possibilities[key]
        beam_list[i] = [beam_list[i], key]
        i+=1
    #print(beam_list)
    #print("PROTEINS: ", proteins[0], proteins[1], proteins[2])
    #print("TEMP: ", temporary_proteins[0], temporary_proteins[1], temporary_proteins[2])


    for i in range(len(beam_list)):
        # print(beam_list[i])
        # needed_protein = int(re.findall('\d+',key)[0])
        # needed_direction = ''.join(filter(str.isalpha, key))
        proteins[i] = temporary_proteins[i]
        # last_index = len(beam_list[i]) - 1
        # direction = beam_list[i][last_index]
        # print(direction)
        # #previous_acid.add_connection(direction)
        # #protein.add_acid(acid_type, locations[direction], direction)
        # location = locations[direction]
        # prev_locs.append(location)

    #print("prev: ", prev_locs)
    #print("PROTEINS: ", proteins[0], proteins[1], proteins[2])

    if proteins[0].length == protein_length:
        return(temporary_proteins)
    else:
        next_layer(protein, prev_locs)
