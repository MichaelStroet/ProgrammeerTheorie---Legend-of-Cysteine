# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
This algorithm will fold a protein using a greedy algorithm
"""
import copy
import random
import numpy as np

from datastructure import Protein, Acid

def greedy(protein_string):
	'''
	The input is a string that represents the proteins amino acid sequence
	The output is a protein folded by a greedy algorithm
	'''

	# Use protein length to establish location of first amino acid in a matrix
	protein_length = len(protein_string)
	protein = Protein(protein_length)

	# Place the first two amino acids
	location = [protein_length - 1, protein_length - 1]
	protein.add_acid(protein_string[0], location, "")
	protein.acids[location[0], location[1]].add_connection("first")

	location = [location[0] + 1, location[1]]
	protein.add_acid(protein_string[1], location, "down")
	protein.acids[location[0], location[1]].add_connection("up")

	# Until solution is found, fold a protein greedy like
	solution_found = False
	while not solution_found:
		protein_clean = copy.deepcopy(protein)
		(solution_found, protein_result) = greedy_fold(protein_clean, protein_string, protein_length, location)
	print(protein_result)

def greedy_fold(protein, p_string, p_len, loc_current):
	'''
	The input is the protein matrix, string and length 
	and the location of the last placed amino acid
	The ouput is a folded protein
	'''
	print("line 46: protein matrix, its string, lenght and location of second placed protein\n", protein, p_string, p_len, loc_current)
		
	# Every direction for the following amino acid
	for acid_index in range(2, p_len):

		# Clean slate for location based items
		locs_next = {}
		locs_possible = []
		energy = {}

		# Check the type of the to be placed acid an its possible locations
		acid_type = p_string[acid_index]
		directions = protein.neighbors(loc_current)

		# Check if any directions are a valid location for amino acid placement
		for direction, loc_new in directions.items():

			# Remember the next possible locations
			if protein.acids[loc_new[0], loc_new[1]] == 0:
				locs_next[direction] = loc_new

		# Check the energy of every next location
		if len(locs_next) > 0:
			previous_energy = protein.energy
			#print("line 69: dict of next locations and the prev energy\n", locs_next, previous_energy)

			# Every next location's energy is collected after pseudo placing
			for direction, loc_next in locs_next.items():
				previous_acid = protein.acids[loc_current[0], loc_current[1]]
				previous_acid.add_connection(direction)
				#print("line 75: direction and next location\n", direction, loc_next)

				# Acid is placed, energy is stored, acid is removed again
				protein.add_acid(acid_type, loc_next, direction)
				# print(protein)
				energy[direction] = protein.check_energy(loc_next, acid_type)
				protein.remove_acid(loc_next, previous_energy)
				#print("line85: pseudo location and type of acid\n", loc_next, acid_type)

			# Compare energy, lowest else random
			energy_mean = np.mean(list(energy.values()))
			for key, value in energy.items():
				if value <= energy_mean:
					locs_possible.append(key)
			#print("Line 92: locations", locs_possible)

			#print("line 94: energy dict and energy mean\n", energy, energy_mean)

			# chooses a random direction from the possible locations then adds that acid
			loc_choice = random.choice(list(locs_possible))
			location = locs_next[loc_choice]

			# Add the acid object to the protein and connect it to the previous amino acids
			protein.add_acid(acid_type, location, loc_choice)
			protein.energy += energy[loc_choice]

			# Change the current location
			loc_current = location
			#print("line97: random direction of possible locations\n", loc_choice, location)
		# Protein incomplete, abort folding
		else:
			print("line 100:\n No locations found")
			break
		#print("line 101: type of acid to be placed, its possible directions and energy dict\n", acid_type, "\n", directions, "\n", energy)
	
	if protein.length == p_len and protein.energy < 0:
		return(True, protein)

	else:
		return(False, protein)
