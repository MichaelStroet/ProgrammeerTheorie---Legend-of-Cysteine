# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import copy
import numpy as np
import matplotlib.pyplot as plt

from datastructure import Protein, Acid

def random_walk(protein_string):

    protein_length = len(protein_string)
    protein = Protein(protein_length)

    location = [protein_length - 1, protein_length - 1]

    #place first & second amino acid underneath [row, column]
    protein.add_acid(protein_string[0], location, "")
    location = [location[0] + 1, location[1]]
    protein.add_acid(protein_string[1], location, "up")

    length_partial = 3

#     while not solution_found:
#         new_protein = copy.deepcopy(protein, protein_string, length_partial)
#
#         (solution_found, protein_result) = walk(new_protein)
#
#     print(solution_found)
#     print(protein_result)
#
# def walk(protein, protein_string, length_partial):

    print(protein)
