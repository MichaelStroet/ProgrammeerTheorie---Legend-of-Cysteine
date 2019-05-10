# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import random

from acid import Acid

from functions import new_location

def hillclimber(start_protein, dimension):
    """
    This algorithm will decrease the energy state of a random protein
    by refolding parts of the protein structure
    The input is a random start_position of a protein
    """
    print(start_protein)
    if dimension == 2:
        acid_z = 0
    else:
        acid_z = 1          #<---- still needs to be defined properly

    # initialise first acid location
    acid_x, acid_y = start_protein.first_acid
    energy = start_protein.energy
    print([acid_x, acid_y], energy)

    # retrieve the first acid
    first_acid = start_protein.acids[acid_x, acid_y]
    acid = first_acid

    # create a list to hold protein locations
    acid_locations = []

    # fill the list with locations
    while not acid.connections["next"] == "":
        acid = start_protein.acids[acid_x, acid_y]
        acid_x, acid_y = acid.position
        acid_locations.append([acid_x, acid_y])
        acid_x, acid_y = new_location([acid_x, acid_y], acid.connections["next"], len(start_protein.acids))

    print(acid_locations)

    # determine index and range
    acid_index = len(acid_locations) - 1
    cut_range = 2                                                    # deletes range - 1 

    # make two cuts in the protein, leaving atleast one acid
    cut_start = random.randint(-1, acid_index - 2)                   # start -1 to end -2
    cut_end = cut_start + cut_range

    print("start ", cut_start,"; end: ", cut_end)


    # determine the connections of the cut
    if not cut_start == -1:
        start_acid_row = acid_locations[cut_start][0]
        start_acid_column = acid_locations[cut_start][1]
        start_acid = start_protein.acids[start_acid_row, start_acid_column]

        print(start_acid.connections)
        start_acid.connections["next"] = ""
        print(start_acid.connections)

    else:
        print("cuts first protein off")

    if not cut_end == acid_index + 1:
        end_acid_row = acid_locations[cut_end][0]
        end_acid_column = acid_locations[cut_end][1]
        end_acid = start_protein.acids[end_acid_row, end_acid_column]

        print(end_acid.connections)
        end_acid.connections["previous"] = ""
        print(end_acid.connections)

    else: 
        print("cuts the last protein off")

    # every acid between the start and end is removed
    for i in range(cut_start + 1 , cut_end):
        acid_row = acid_locations[i][0]
        acid_column = acid_locations[i][1]
        print(i, acid_row, acid_column)
        start_protein.acids[acid_row, acid_column] = 0

    print(start_protein)

    # 
    pass
