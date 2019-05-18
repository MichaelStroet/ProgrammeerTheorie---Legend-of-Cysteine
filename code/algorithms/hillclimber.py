# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import copy
import random
import numpy as np

from acid import Acid

from functions import new_location

def hillclimber(start_protein, iterations):
    """
    This algorithm will decrease the energy state of a random protein
    by refolding parts of the protein structure
    The input is a random start_position of a protein
    """
    print(start_protein)
    print(start_protein.length)
 
    # first acid location
    acid_z, acid_y, acid_x = start_protein.first_acid
    energy = start_protein.energy
    print([acid_z, acid_y, acid_x], energy)

    # retrieve the first acid
    acid = start_protein.acids[acid_z, acid_y, acid_x]

    # create a list to hold protein locations
    acid_locations = []
    
    # fill the list with acid locations
    # todo: check if I can get the connections more easily with just acid.location instead of connections
    while not acid.connections["next"] == "":
        acid = start_protein.acids[acid_z, acid_y, acid_x]
        acid_z, acid_y, acid_x = acid.location
        acid_locations.append([acid_z, acid_y, acid_x])

        # todo: change matrix_length to matrix_size after push
        acid_z, acid_y, acid_x = new_location([acid_z, acid_y, acid_x], acid.connections["next"], 1, start_protein.matrix_size)

    print(acid_locations)
    protein = copy.deepcopy(start_protein)

    # remove and add acids every iteration
    for i in range(0, iterations):
        protein_searched = copy.deepcopy(start_protein)
        incomplete_protein, removed_acids, binding_sites = remove_acids(protein, acid_locations)
        protein_searched = new_path(incomplete_protein, binding_sites, removed_acids, 0)
        print("iteration:", i + 1)


def remove_acids(protein, acid_locations):
    """
    This function removes acids of a folded protein
    """

    # determine index and range
    acid_index = len(acid_locations) - 1
    cut_range = 2

    # make two cuts in the protein, leaving atleast one acid
    cut_start = random.randint(-1, acid_index - cut_range)
    cut_end = cut_start + cut_range + 1

    # remember the acids that the newly placed acids will need to be attached to
    start, end = 0, 0

    print("start ", cut_start,"; end: ", cut_end)

    # determine the acid before the cut
    if cut_start > -1:
        start_layer, start_row, start_column = acid_locations[cut_start]
        start = protein.acids[start_layer, start_row, start_column]

        # remove the next connection
        start.connections["next"] = ""

    # determine the acid after the second cut
    if cut_end < acid_index:
        end_layer, end_row, end_column = acid_locations[cut_end]
        end = protein.acids[end_layer, end_row, end_column]

        # remove the previous connection
        end.connections["previous"] = ""

    # every acid between the start and end is removed
    acids_removed = []
    for i in range(cut_start + 1 , cut_end):
        acid_layer, acid_row, acid_column = acid_locations[i]
        acid_removed = protein.acids[acid_layer, acid_row, acid_column]
        acids_removed.append(acid_removed)
        acid_removed = 0

    print(protein)
    print("cut away acids:", len(acids_removed))

    return protein, acids_removed, [start, end]


def new_path(protein, binding_sites, removed_acids, index):
    print("lets start a new journey, a path to the unknown")
    start, end = binding_sites

    # if there is a start and end acid outside of the cut
    if not start == 0 and not end == 0:
        print("start, end:", start.location, end.location)

    # when the last acid is cut off 
    elif not start == 0:
        print("start:", start.location)

    # when the first acid is cut off
    else:
        print("end:",end.location)
    print(protein)
    return(protein)


# for add acid I need: type, location and direction_previous