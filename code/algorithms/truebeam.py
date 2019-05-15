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


def beamsearch(pr_string, dimension):

    global best_nodes, protein_length, protein_string, energy_counter, beam_list
    protein_string = pr_string

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
    beam_list = [0] * 3


    next_layer(protein, previous_location)

    return protein_min, energy_counter

def next_layer(the_protein, prev_location):
    '''
    Check possible sites for the next amino acid,
    see whether the matrix box left, up & right are empty,
    if so store their locations and direction in a dictionnary
    '''

    global protein_min

    possible_sites = {}
    energy = {}
    protein_energy ={}
    beam_possibilities = {}
    prev_locs = []
    print(beam_list)
    acid_type = protein_string[the_protein.length]

    print(len(prev_location))
    for i in range(len(prev_location)):
        previous_location = prev_location[i]
        print(previous_location)
        print(beam_list)
        protein = the_protein
        if any(beam_list):
            i = 1
            for j in range(len(beam_list)):
                for i in range(len(beam_list[j])):
                    print(beam_list[j][i])
                    # dir = beam_list[j][i]
                    # loc = new_location(previous_location, beam_list[j][i], len(protein.acids), len(protein.acids[0]))
                    #
                    # previous_acid = protein.acids[previous_location[0], previous_location[1], previous_location[2]]
                    # print(previous_acid)
                    # previous_acid.add_connection(dir)
                    # protein.add_acid(acid_type, loc, dir)
                    # print(protein)
                    # print(protein.check_energy(loc, acid_type))

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
                print(previous_acid)
                previous_acid.add_connection(direction)

                # Acid is placed, energy is stored, acid is removed again
                protein.add_acid(acid_type, site, direction)
                energy[direction] = protein.check_energy(site, acid_type)
                total_energy = previous_energy + protein.check_energy(site, acid_type)
                print("TOTAL energy: ", total_energy)
                protein_energy[direction] = total_energy
                beam_possibilities[direction] = total_energy
                protein.remove_acid(previous_energy)
            sorted_possibilities = sorted(beam_possibilities.items(), key=operator.itemgetter(1))
            beam_possibilities = dict(sorted_possibilities)
            print(sorted_possibilities)
            print(beam_possibilities)
            #beam_possibilities["low"] = -1
            #beam_possibilities["high"] = -2

        print(beam_possibilities)

        proteins = {}
        i = 0
        for key in sorted(beam_possibilities, key=beam_possibilities.get)[:3]:
            print(key, beam_possibilities[key])
            print(beam_list[i])
            proteins[i] = copy.deepcopy(protein)
            print(proteins[i])
            prev_acid = proteins[i].acids[previous_location[0], previous_location[1], previous_location[2]]
            print(prev_acid)
            prev_acid.add_connection(key)
            proteins[i].add_acid(acid_type, locations[key], key)
            proteins[i].energy += energy[key]
            print(proteins[i])

            beam_list[i] = beam_possibilities[key]
            beam_list[i] = [beam_list[i], key]
            i+=1
        print(beam_list)
        print(proteins)
        for i in range(len(beam_list)):
            print(beam_list[i])
            last_index = len(beam_list[i]) - 1
            direction = beam_list[i][last_index]
            print(direction)
            #previous_acid.add_connection(direction)
            #protein.add_acid(acid_type, locations[direction], direction)
            location = locations[direction]
            prev_locs.append(location)

            print("prev: ", prev_locs)

        next_layer(protein, prev_locs)
