# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import random

from trueacid import Acid

from truefunctions import new_location

def hillclimber(start_protein):
    """
    This algorithm will decrease the energy state of a random protein
    by refolding parts of the protein structure
    The input is a random start_position of a protein
    """
    print(start_protein)
    print(start_protein.length)
 
    # initialise first acid location
    acid_z, acid_y, acid_x = start_protein.first_acid
    energy = start_protein.energy
    print([acid_z, acid_y, acid_x], energy)

    # retrieve the first acid
    first_acid = start_protein.acids[acid_z, acid_y, acid_x]
    acid = first_acid

    # create a list to hold protein locations
    acid_locations = []

    # fill the list with acid locations
    while not acid.connections["next"] == "":
        acid = start_protein.acids[acid_z, acid_y, acid_x]
        acid_z, acid_y, acid_x = acid.position
        acid_locations.append([acid_z, acid_y, acid_x])
        acid_z, acid_y, acid_x = new_location([acid_z, acid_y, acid_x], acid.connections["next"], 1, start_protein.matrix_length)

    print(acid_locations)

    # determine index and range
    acid_index = len(acid_locations) - 1
    cut_range = 2                                                    # deletes range - 1 

    # make two cuts in the protein, leaving atleast one acid
    cut_start = random.randint(-1, acid_index - 2)                   # start -1 to end -2
    cut_end = cut_start + cut_range

    print("start ", cut_start,"; end: ", cut_end)


    # determine the acid before the cut
    if not cut_start == -1:
        start_acid_layer = acid_locations[cut_start][0]
        start_acid_row = acid_locations[cut_start][1]
        start_acid_column = acid_locations[cut_start][2]
        start_acid = start_protein.acids[start_acid_layer, start_acid_row, start_acid_column]

        # remove the next connection it had
        start_acid.connections["next"] = ""

    else:
        print("cuts first protein off")

    # determine the acid after the second cut
    if not cut_end == acid_index + 1:
        end_acid_layer = acid_locations[cut_end][0]
        end_acid_row = acid_locations[cut_end][1]
        end_acid_column = acid_locations[cut_end][2]
        end_acid = start_protein.acids[start_acid_layer, end_acid_row, end_acid_column]

        # remove the previous connection it had
        end_acid.connections["previous"] = ""

    else: 
        print("cuts the last protein off")

    # every acid between the start and end is removed
    for i in range(cut_start + 1 , cut_end):
        acid_layer = acid_locations[i][0]
        acid_row = acid_locations[i][1]
        acid_column = acid_locations[i][2]
        print(i, acid_layer, acid_row, acid_column)
        start_protein.acids[acid_layer, acid_row, acid_column] = 0

    print(start_protein)

    # 
    pass
