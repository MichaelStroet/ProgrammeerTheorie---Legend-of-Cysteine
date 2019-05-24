# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import copy
import random
import numpy as np

from acid import Acid

from functions import new_location

def hillclimber(protein, iterations, cut_acids):
    """
    This algorithm will decrease the energy state of a random protein
    by refolding parts of the protein structure
    The input is a random start_position of a protein, the number of iterations and the number of acids to cut away
    """
    print(protein)
    iterations = 1
    cut_acids = 4
    new_protein = copy.deepcopy(protein)
    acid_locations = [acid.location for acid in protein.acid_list]
    acid_index = len(protein.acid_list) - 1

    # every iteration a change is made to the folded protein
    for i in range(0, iterations):

        # determine cuts in the protein, leaving atleast one acid
        cut_start = random.randint(-1, acid_index - cut_acids)
        cut_end = cut_start + cut_acids + 1

        # remove the acids in between the cuts
        remove_acids(new_protein, cut_start, cut_end)

        # add previously removed acids
        add_acids(new_protein, cut_start, cut_end)

        # calculate energy for new protein
        acid_locations = [acid.location for acid in protein.acid_list]
        for acid_location in acid_locations:
            new_protein.new_energy(acid_location)
            print(new_protein.energy, protein.energy)
        new_protein.energy = int(new_protein.energy / 2)

        # compare the energy between the old and new protein
        print("new protein and its energy:", new_protein, new_protein.energy)
        if new_protein.energy < protein.energy:
            print("lets keep this one")
            new_protein = copy.deepcopy(new_protein)
            protein = copy.deepcopy(new_protein)
        else:
            print("discard this one, it's rubbisch!")
            new_protein = copy.deepcopy(protein)

        print([acid.connections for acid in protein.acid_list])

def remove_acids(protein, cut_start, cut_end):
    '''
    Removes acids between two points
    '''
    print([cut_start, cut_end])
    for i in range(cut_start + 1 , cut_end):
        protein.remove_acid_index(i)

def add_acids(protein, start, end):
    '''
    Adds acids that were previously removed between the start and end point
    '''
    acid_index_list = list(range(start + 1, end))
    end_location = None

    # if there is a start and end acid outside of the cut
    if start >= 0 and end <= protein.length - 1:
        end_location = protein.get_acid_index(end).location
        current_location = protein.get_acid_index(start).location

    # when the last acid is cut off 
    elif start >= 0:
        current_location = protein.get_acid_index(start).location

    # when the first acid is cut off
    else:
        acid_index_list = acid_index_list[::-1]
        current_location = protein.get_acid_index(end).location
    
    # 
    _add_acids(protein, acid_index_list, end_location, current_location, 0)


def _add_acids(protein, acid_index_list: list, end_location: list, previous_location: list, depth: int):
    # print("acids:", acid_index_list, "end_location", end_location, "previous_location", previous_location, "depth", depth)
    if depth == len(acid_index_list):
        print("depth, energy:",protein, protein.energy)
        surrounding_locations = protein.neighbors(previous_location)
        if not end_location:
            print("valid path found without end")
            protein.energy = 0
            return True

        elif end_location in surrounding_locations.values():
            print("valid path found")
            direction = list(surrounding_locations.keys())[list(surrounding_locations.values()).index(end_location)]
            print(direction)
            protein.add_acid_index(acid_index_list[depth-1] + 1, end_location, direction)
            protein.energy = 0
            return True

        else:
            print("return traveler, for thou arth lost")
            return False

    # when
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