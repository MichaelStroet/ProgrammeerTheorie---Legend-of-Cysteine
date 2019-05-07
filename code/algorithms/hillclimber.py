# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

from acid import Acid

def hillclimber(start_protein):
    """
    This algorithm will decrease the energy state of a random protein
    by refolding parts of the protein structure
    The input is a random start_position of a protein
    """
    print(start_protein)
    first_acid_location = start_protein.first_acid
    location = first_acid_location
    print(first_acid_location)
    first_acid = start_protein.acids[first_acid_location]
    acid = first_acid

    acid_data = []

    while not acid.connections["next"] == "":
        adic = start_protein.acids[location]
        acid_x = acid.position[0]
        acid_y = acid.position[1]

        acid_data.apppend([acid_x, acid_y])
        print(acid)

    print(acid_data)
    print(first_acid)

    pass
