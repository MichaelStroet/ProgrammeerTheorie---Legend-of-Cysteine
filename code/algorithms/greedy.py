# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
This algorithm will fold a protein using a greedy algorithm
"""
import copy

from datastructure import Protein, Acid

def greedy_start(protein_string):
	'''
	The input is a string that represents the proteins amino acid sequence
	The output is a protein folded by a greedy algorithm
	'''

	# Use length to establish location of first amino acid in a matrix
	protein_length = len(protein_string)
	protein = Protein(protein_length)

	# Place the first two amino acids
	location = [protein_length - 1, protein_length - 1]
	protein.add_acid(protein_string[0], location, "")
	protein.acids[location[0], location[1]].add_connection("down")

	location = [location[0] + 1, location[1]]
	protein.add_acid(protein_string[1], location, "down")
	protein.acids[location[0], location[1]].add_connection("up")

	# Check if solution is found
	solution_found = False
	while not solution_found:
		clean_protein = copy.deepcopy(protein)
		solution_found = greedy_fold(clean_protein)


def greedy_fold(protein):
	print("greedy_fold, yes, that's me")
	return True
