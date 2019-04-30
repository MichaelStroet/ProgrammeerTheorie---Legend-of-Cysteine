# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
This algorithm will fold a protein using a greedy algorithm
Greedy in this case means always placing an amino acid at the location that results in the lowest energy
"""
import copy
import random
import numpy as np

from datastructure import Protein, Acid

def greedy(protein_string, N_tries):
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
	protein.acids[location[0], location[1]].add_connection("down")

	location = [location[0] + 1, location[1]]
	protein.add_acid(protein_string[1], location, "down")

	energy_min = 0

	# Try to fold N_tries protein greedy like
	for i in range(N_tries):
		#if (i + 1) % 1000 == 0:
		#	print(f"{i + 1}th protein folded")

		# Start with a clean protein	
		protein_clean = copy.deepcopy(protein)
		(solution_found, protein_result) = greedy_fold(protein_clean, protein_string, protein_length, location)

		if solution_found:
			if protein_result.energy < energy_min:
				energy_min = protein_result.energy
				protein_min = protein_result

				#print(f"found new lowest energy: {energy_min}")
	return protein_min

def greedy_fold(protein, p_string, p_len, loc_current):
	'''
	The input is the protein matrix, string and length 
	and the location of the last placed amino acid
	The ouput is a folded protein
	'''
		
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

			# Every next location's energy is collected after pseudo placing
			for direction, loc_next in locs_next.items():
				previous_acid = protein.acids[loc_current[0], loc_current[1]]
				previous_acid.add_connection(direction)

				# Acid is placed, energy is stored, acid is removed again
				protein.add_acid(acid_type, loc_next, direction)
				energy[direction] = protein.check_energy(loc_next, acid_type)
				protein.remove_acid(loc_next, previous_energy)

			# Compare energy, lowest else random
			energy_mean = np.mean(list(energy.values()))
			for key, value in energy.items():
				if value <= energy_mean:
					locs_possible.append(key)

			# chooses a random direction from the possible locations then adds that acid
			loc_choice = random.choice(list(locs_possible))
			location = locs_next[loc_choice]

			# Add the acid object to the protein and connect it to the previous amino acids
			previous_acid.add_connection(loc_choice)
			protein.add_acid(acid_type, location, loc_choice)
			protein.energy += energy[loc_choice]

			# Change the current location
			loc_current = location

		# Protein incomplete, abort folding
		else:
			break
		
	# Return the folded protein
	if protein.length == p_len and protein.energy < 0:
		return(True, protein)
	else:
		return(False, protein)
