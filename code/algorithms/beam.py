# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
Beam Search

This algorithm will fold a protein using a beam search algorithm
"""

import copy
import re
import operator

from acid import Acid
from protein import Protein
from functions import new_location
from operator import itemgetter


def beamsearch(pr_string, width, dimension):

    # Set global variables
    global best_nodes, protein_length, protein_string, energy_counter, beam_list, proteins, B_width, matrix_sizes

    protein_string = pr_string
    B_width = width

    # Use protein length to establish location of first amino acid in a matrix
    protein_length = len(protein_string)
    protein = Protein(protein_length, dimension)

    # Place the first two amino acids
    protein.place_first_two(protein_string)
    previous_location = [protein.last_acid]

    # Initialize dictionaries
    energy_counter = {}
    matrix_sizes = {}

    # Initialize the proteins dictionary that keeps track of the protein objects
    proteins = {}
    for i in range(B_width):
        proteins[i] = protein

    # Initialize the list that keeps the direction of new acids and energy of the protein
    beam_list = [0] * B_width

    # Start the search
    next_layer(protein, previous_location)

    # Take the top protein as best protein
    protein_min = proteins[0]
    energy_min = protein_min.energy

    return protein_min, energy_min, matrix_sizes

# Function that calculates the next steps and chooses the ones with minimal energy
def next_layer(the_protein, prev_location):
    '''
    Check possible sites for the next amino acid,
    see whether the matrix box left, up & right are empty,
    if so store their locations and direction in a dictionnary
    '''

    prev_locs = []

    # Initialize the temporary list that holds copies of the offocial proteins
    # This list is needed as the official list can only be updated once all new
    # proteins have been folded, otherwise we may lose the protein we wanted
    # to continue folding as it may already have been replaced by a new folding
    temporary_proteins = [0] * B_width

    acid_type = protein_string[the_protein.length]

    # Create a dictionary that keeps track of all the children
    beam_possibilities = {}

    # For each location
    for i in range(len(prev_location)):
        # Initialize dictionaries
        protein_energy ={}
        energy = {}

        previous_location = prev_location[i]

        if any(proteins):
            protein = proteins[i]
        else:
            protein = the_protein

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
                energy[direction] = protein.check_energy(site, acid_type)
                total_energy = previous_energy + protein.check_energy(site, acid_type)
                protein_energy[direction] = total_energy

                # If the protein is complete, calculate the smallest matrix size
                if protein.length == protein_length:
                    min_matrix_size = protein.smallest_matrix()
                    matrix_sizes[total_energy] = matrix_sizes.get(total_energy, {})
                    matrix_sizes[total_energy][min_matrix_size] = matrix_sizes[total_energy].get(min_matrix_size, 0) + 1

                # Create a variable that remembers the place of the protein in the list (i) and the direction of the next acid
                direction = str(i) + str(direction)

                # Add it to the dictionary of all children
                beam_possibilities[direction] = total_energy

                # Remove the acid
                protein.remove_acid(previous_energy)

            # Sort all the children and reconvert it into a dict
            sorted_possibilities = sorted(beam_possibilities.items(), key=operator.itemgetter(1))
            beam_possibilities = dict(sorted_possibilities)

    # Set i to zero for indexing in the beam_list
    i = 0

    # For each protein in the beam
    for key in sorted(beam_possibilities, key=beam_possibilities.get)[:B_width]:

        # Retrieve the place of the protein in the previous locations list
        needed_protein = int(re.findall('\d+',key)[0])

        # Retrieve the direction of the acid
        needed_direction = ''.join(filter(str.isalpha, key))

        # Retrieve the location of the previous acid
        previous_loc = prev_location[needed_protein]

        # Get a list of the neighboring sites to get the acid's new location
        needed_locations = protein.neighbors(previous_loc)
        needed_loc = needed_locations[needed_direction]
        prev_locs.append(needed_loc)

        # Make a copy of the protein in the temporary list and add the new acid
        temporary_proteins[i] = copy.deepcopy(proteins[needed_protein])
        prev_acid = temporary_proteins[i].acids[previous_loc[0], previous_loc[1], previous_loc[2]]
        prev_acid.add_connection(needed_direction)
        temporary_proteins[i].add_acid(acid_type, needed_loc, needed_direction)
        needed_energy = temporary_proteins[i].check_energy(needed_loc, acid_type)
        temporary_proteins[i].energy += needed_energy

        # Add the direction and energy to the beam list and update the index
        beam_list[i] = beam_possibilities[key]
        beam_list[i] = [beam_list[i], key]
        i+=1

    # Update the official proteins dictionary
    for i in range(len(beam_list)):
        proteins[i] = temporary_proteins[i]

    # Check if the protein is complete, if so return, if not continue searching
    if proteins[0].length == protein_length:
        return(temporary_proteins)
    else:
        next_layer(protein, prev_locs)
