# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

# Add the directory structure to the path
import os, sys
import time

directory = os.path.dirname(os.path.realpath(__file__))

# Add the code paths
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

# Add the data path
sys.path.append(os.path.join(directory, "data"))

# Import algorithms
from random_walk import random_walk
from greedy import greedy
from branch_n_bound import branch_n_bound

# Import auxilary functions
from graph import visualise, dictionary_hist
from datastructure import Protein
from datastructure import Acid


def read_input():
	'''
	Parse text file containing proteins represented as a string
	Returns a list containing a single protein (represented as a string) per list entry
	'''

	# Opens a datafile as a list with strings
	with open("data/input.txt", "r") as f:
		file_content = f.read()
		file_lines = file_content.split()
	return file_lines


if __name__ == "__main__":

	algorithms = ["random walk", "greedy", "probabilty-based branch-n-bound"]
	for i, algorithm in zip(range(len(algorithms)), algorithms):
		print(f"{i + 1}: {algorithm}")
	print()

	chosen_algorithm = int(input("Choose an algorithm: ")) - 1
	print(algorithms[chosen_algorithm] + '\n')

	proteins = read_input()
	for i, protein in zip(range(len(proteins)), proteins):
		print(f"{i + 1}: {protein}")
	print()

	chosen_protein = int(input("Choose a protein: ")) - 1
	print(proteins[chosen_protein] + '\n')

	if chosen_algorithm == 0:
		N_tries = int(input("How many proteins to fold? "))
		print(f"{N_tries}\n")

		start_time = time.time()
		protein, dict = random_walk(proteins[chosen_protein], N_tries)
		end_time = time.time() - start_time

	elif chosen_algorithm == 1:
		N_tries = int(input("How many proteins to fold? "))
		print(f"{N_tries}\n")

		start_time = time.time()
		protein, dict = greedy(proteins[chosen_protein], N_tries)
		end_time = time.time() - start_time

	elif chosen_algorithm == 2:
		# to do: ask for probabilities

		start_time = time.time()
		protein = branch_n_bound(proteins[chosen_protein])
		end_time = time.time() - start_time

	else:
		print(f"Error: Unknown algorthm '{algorithms[chosen_algorithm]}'")
		exit(1)


	if protein and end_time:
		print(protein)
		print("Elapsed time: " + time.strftime('%H:%M:%S', time.gmtime(end_time)))

		if dict:
			dictionary_hist(dict)
