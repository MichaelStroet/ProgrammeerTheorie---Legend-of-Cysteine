# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
Hillclimber
This script will take a folded protein from Greedy, cut out some amino acids and
try to replace them in a better manner. The algorithm keeps trying new foldings
until it finds one with a lower energy.
"""

import copy, random
import numpy as np

from acid import Acid
from functions import new_location
from protein import Protein
from greedy_lookahead import greedy


def hillclimber(protein_string: str, dimension: str, matrix_size: int, iterations: int, cut_acids: int):
    '''
    This algorithm will re-fold parts of the protein structure and return it
    '''
    matrix_size = len(protein_string)

    # Initialize a single greedy protein without look-ahead
    protein, energy_counter, matrix_sizes = greedy(protein_string, 0, 1, dimension, matrix_size)
    new_protein = copy.deepcopy(protein)
    energy_old = copy.deepcopy(protein.energy)
    acid_locations = [acid.location for acid in protein.acid_list]
    acid_index = len(protein.acid_list) - 1
    energy_counter = {}
    matrix_sizes = {}

    # Every iteration a change is made to the folded protein
    for i in range(0, iterations):

        # determine cuts in the protein, leaving atleast one acid
        cut_start = random.randint(-1, acid_index - cut_acids)
        cut_end = cut_start + cut_acids + 1

        # Remove the acids in between the cuts
        remove_acids(new_protein, cut_start, cut_end)

        # Add previously removed acids
        add_acids(new_protein, cut_start, cut_end)

        # Calculate energy for new protein
        acid_locations = [acid.location for acid in protein.acid_list]
        for acid_location in acid_locations:
            new_protein.new_energy(acid_location)
        new_protein.energy = int(new_protein.energy / 2)
        energy = new_protein.energy
        energy_counter[energy] = energy_counter.get(energy, 0) + 1

        # Determine the smallest matrix size needed for this protein
        protein.first_acid = protein.get_acid_index(0).location
        min_matrix_size = protein.smallest_matrix()
        matrix_sizes[energy] = matrix_sizes.get(energy, {})
        matrix_sizes[energy][min_matrix_size] = matrix_sizes[energy].get(min_matrix_size, 0) + 1

        # Compare the energy between the old and new protein
        if new_protein.energy < protein.energy:
<<<<<<< HEAD
            print(f"New minimum energy found : {energy}")
=======
            print(f"New minimum energy found: {new_protein.energy}")
>>>>>>> 9f0b51895575dfd4b919777b6d99ba47556ae95d
            new_protein = copy.deepcopy(new_protein)
            protein = copy.deepcopy(new_protein)
        else:
            new_protein = copy.deepcopy(protein)

    if not protein:
        exit("Error: No protein 'protein' to return")
    else:
        return protein, energy_counter, matrix_sizes

def remove_acids(protein: Protein, cut_start: int, cut_end: int):
    '''
    Removes acids between two points
    '''
    for i in range(cut_start + 1 , cut_end):
        protein.remove_acid_index(i)

def add_acids(protein: Protein, start: int, end: int):
    '''
    Adds acids that were previously removed between the start and end point
    '''
    acid_index_list = list(range(start + 1, end))
    end_location = None

    # If there is a start and end acid outside of the cut
    if start >= 0 and end <= protein.length - 1:
        end_location = protein.get_acid_index(end).location
        current_location = protein.get_acid_index(start).location

    # When the last acid is cut off
    elif start >= 0:
        current_location = protein.get_acid_index(start).location

    # When the first acid is cut off
    else:
        acid_index_list = acid_index_list[::-1]
        current_location = protein.get_acid_index(end).location

    # Add acids
    _add_acids(protein, acid_index_list, end_location, current_location, 0)


def _add_acids(protein, acid_index_list: list, end_location: list, previous_location: list, depth: int):
    '''
    Adds acids from a list and returns the protein if a valid path is found
    '''
    # If the end of the list is reached, check if the path is valid
    if depth == len(acid_index_list):
        surrounding_locations = protein.neighbors(previous_location)
        # if there is no end location
        if not end_location:
            protein.state_space_visited()
            last_acid = protein.get_acid_index(protein.length - 1)
            last_acid.connections["next"] = ""

            # Set energy to zero after finding soluting, while energy bug exists
            protein.energy = 0
            return True

        # If the last placed acid can be connected to the rest of the protein
        elif end_location in surrounding_locations.values():
            protein.state_space_visited()
            direction = list(surrounding_locations.keys())[list(surrounding_locations.values()).index(end_location)]
            protein.add_acid_index(acid_index_list[depth-1] + 1, end_location, direction)

            # Set energy to zero after finding soluting
            protein.energy = 0
            return True

        else:
            protein.state_space_visited()
            return False

    #
    else:
        possible_sites = protein.possible_sites(previous_location)
        directions = list(protein.possible_sites(previous_location).keys())
        random.shuffle(directions)

        for direction in directions:
            location = possible_sites[direction]
            protein.add_acid_index(acid_index_list[depth], location, direction)
            complete = _add_acids(protein, acid_index_list, end_location, location, depth + 1)
            if complete:
                return True
            else:
                protein.remove_acid_index(acid_index_list[depth])
