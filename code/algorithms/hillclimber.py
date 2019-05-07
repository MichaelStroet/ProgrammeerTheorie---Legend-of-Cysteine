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

    # create a random part of the protein to be removed
    acid_index = len(acid_locations) - 1
    random_start = random.randint(1, acid_index)            # for now the first acid needs to stay in place
    random_end = random.randint(random_start, acid_index)
    print(random_start, random_end)

    # every acid of the random part is removed
    for i in range(random_end, random_start -1 , - 1):
        location = acid_locations[i]
        start_protein.remove_acid_hillclimber(location)
        print(location)

    # remember the 
    print(first_acid)
    print(start_protein)

    pass
