# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

# Add the directory structure to the path
import os, sys

directory = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

# Add the data
sys.path.append(os.path.join(directory, "data"))

# Import classes
from graph import visualise
from branch_n_bound import branch_n_bound
from random_walk import random_walk
from datastructure import Protein, Acid


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
    proteins = read_input()
    branch_n_bound("HHPH")
