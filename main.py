# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

# Add the directory structure to the path
import os, sys

directory = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

sys.path.append(os.path.join(directory, "data"))

from graph import visualise
from branch_n_bound import branch_n_bound# as bnb


def read_input():
    '''
    Parse text file
    '''

    with open("data/input.txt", "r") as f:
        file_content = f.read()
        print(file_content)
        print(len(file_content), file_content[2])



if __name__ == "__main__":
    pass
