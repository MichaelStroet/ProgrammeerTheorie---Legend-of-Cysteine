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

	# Until solution is found fold a protein greedy like
	solution_found = False
	while not solution_found:
		protein_clean = copy.deepcopy(protein)
		solution_found = greedy_fold(protein_clean, protein_string, protein_length, location)


def greedy_fold(protein, p_string, p_len, loc_current):
	'''
	The input is the protein matrix, string and length 
	and the location of the last placed amino acid
	The ouput is a folded protein
	'''
	print("line 44: \ngreedy_fold, yes, that's me")
	print("line 45: \n", protein, p_string, p_len, loc_current)
	# add dictionary for possible next locations
	locs_next = {}

	# Every direction for following amino acid
	for acid_index in range(2, p_len):
		acid_type = p_string[acid_index]
		directions = protein.neighbors(loc_current)

		# Check if any directions are a valid location for amino acid placement
		for direction, loc_new in directions.items():

			# Remember the possible next locations
			if protein.acids[loc_new[0], loc_new[1]] == 0:
				locs_next[direction] = loc_new

		# Check the energy of every next location
		if len(locs_next) > 0:
			print("line 63:\n", locs_next)
			for direction, loc_next in locs_next.items():
				print("line65:\n", loc_next, acid_type)

		# Protein incomplete, abort folding
		else:
			print("line 67:\n No locations found")
		print("line 68:\n", acid_type, "\n", directions)

	return True
