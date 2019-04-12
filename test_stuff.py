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
from datastructure import protein, acid

def read_input():
    '''
    Parse text file
    '''

    with open("data/input.txt", "r") as f:
        file_content = f.read()
        file_lines = file_content.split()
        # print(f'lines: {file_lines}\nnumber of lines: {len(file_lines)}\nline 3: {file_lines[2]}')
    return file_lines


if __name__ == "__main__":

	proteins = read_input()
    print(proteins)
    branch_n_bound(proteins[0])
