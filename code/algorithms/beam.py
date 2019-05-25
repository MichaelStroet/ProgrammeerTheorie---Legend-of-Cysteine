# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
Beam Search
This script will fold a protein by keeping track of several options (beam width)
per length and adding a new acid to each option before continuing.
"""

import copy, operator, re

from acid import Acid
from functions import new_location
from operator import itemgetter
from protein import Protein


def beamsearch(p_string, width, dimension, matrix_size):
    '''
    Runs a Beam Search algorithm with a predetermined width which determies how
    many proteins are kept at each new generation. The best conformation,
    the one that has the lowest energy, is saved and returned along with
    a dictionary of all energy counts and the minimal matrix sizes for the folded
    protein.
    '''
    # Set global variables
    global best_nodes, protein_length, protein_string, energy_counter, proteins, B_width, matrix_sizes, initial_protein

    protein_string = p_string
    protein_length = len(protein_string)
    B_width = width

    # Create a protein object with a specific matrix size
    initial_protein = Protein(matrix_size, dimension)

    # Place the first two amino acids
    initial_protein.place_first_two(protein_string)
    previous_location = [initial_protein.last_acid]

    # Initialize dictionaries
    energy_counter = {}
    matrix_sizes = {}

    # Initialize the proteins dictionary that keeps track of the protein objects
    proteins = {}
    for i in range(B_width):
        proteins[i] = initial_protein

    # Start the search
    find_possibilities(previous_location)

    # Take the top protein as best protein
    protein_min = proteins[0]
    energy_min = protein_min.energy

    if protein_min:
        return protein_min, energy_counter, matrix_sizes
    else:
        exit("Error: No protein 'protein_min' to return")

# Function that calculates the next steps and chooses the ones with minimal energy
def find_possibilities(list_locations):
    '''
    Caluclate energy for all possible locations for all chosen children
    '''

    # Create a dictionary that keeps track of all the children
    beam_possibilities = {}

    # For each location
    for i in range(len(list_locations)):
        energy = {}

        previous_location = list_locations[i]

        if any(proteins):
            protein = proteins[i]
        else:
            protein = initial_protein

        possible_sites = protein.possible_sites(previous_location)

        # If there are possible sites (the protein is not stuck)
        if len(possible_sites) > 0:

            previous_energy = protein.energy

            for direction, site in possible_sites.items():

                acid_type = protein_string[protein.length]

                # Determine the previous acid and add the connection
                previous_acid = protein.acids[previous_location[0], previous_location[1], previous_location[2]]
                previous_acid.add_connection(direction)

                # Place the acid and store the energy
                protein.add_acid(acid_type, site, direction)
                protein.new_energy(site)
                total_energy = protein.energy

                # If the protein is complete, determine the smallest matrix size needed for this protein
                if protein.length == protein_length:
                    min_matrix_size = protein.smallest_matrix()
                    matrix_sizes[total_energy] = matrix_sizes.get(total_energy, {})
                    matrix_sizes[total_energy][min_matrix_size] = matrix_sizes[total_energy].get(min_matrix_size, 0) + 1

                    # Update the dictonary for histogram of solutions
                    energy_counter[total_energy] = energy_counter.get(total_energy, 0) + 1


                # Create a variable that remembers the place of the protein in the list (i) and the direction of the next acid
                direction = str(i) + str(direction)

                # Add it to the dictionary of all children
                beam_possibilities[direction] = total_energy

                # Remove the acid
                protein.remove_acid(previous_energy)

    # Sort all the children and reconvert it into a dict
    sorted_possibilities = sorted(beam_possibilities.items(), key=operator.itemgetter(1))
    beam_possibilities = dict(sorted_possibilities)

    # Call function that keeps only the proteins with the lowest energy
    keep_lowest(list_locations, beam_possibilities, acid_type)


def keep_lowest(list_locations, beam_possibilities, acid_type):

    '''
    Keep only *B_width* number of children with the lowest energy among all
    '''
    previous_locations = []

    # Initialize the temporary list that holds copies of the offocial proteins
    # This list is needed as the official list can only be updated once all new
    # proteins have been folded, otherwise we may lose the protein we wanted
    # to continue folding as it may already have been replaced by a new folding
    temporary_proteins = [0] * B_width

    # Set i to zero for indexing
    i = 0

    # For each protein in the beam
    for key in sorted(beam_possibilities, key=beam_possibilities.get)[:B_width]:

        # Retrieve the place of the protein in the previous locations list
        needed_protein = int(re.findall('\d+',key)[0])
        protein = proteins[needed_protein]

        # Retrieve the direction of the acid
        needed_direction = ''.join(filter(str.isalpha, key))

        # Retrieve the location of the previous acid
        previous_loc = list_locations[needed_protein]

        # Get a list of the neighboring sites to get the acid's new location
        needed_locations = protein.neighbors(previous_loc)
        needed_loc = needed_locations[needed_direction]
        previous_locations.append(needed_loc)

        # Make a copy of the protein in the temporary list, add the new acid & update energy
        temporary_proteins[i] = copy.deepcopy(proteins[needed_protein])
        previous_acid = temporary_proteins[i].acids[previous_loc[0], previous_loc[1], previous_loc[2]]
        previous_acid.add_connection(needed_direction)
        temporary_proteins[i].add_acid(acid_type, needed_loc, needed_direction)
        temporary_proteins[i].new_energy(needed_loc)

        # Add the direction and energy to the beam list and update the index
        i+=1

    # Update the official proteins dictionary
    for i in range(B_width):
        proteins[i] = temporary_proteins[i]

    del temporary_proteins

    # Give the user an update
    print(f"New protein length: {proteins[0].length} acids ")

    # Check if the protein is complete, if so return, if not continue searching
    if proteins[0].length == protein_length:
        return
    else:
        find_possibilities(previous_locations)
