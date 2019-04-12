# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np


class Acid:

    def __init__(self, type, position, connection):
        '''
        Initialise an amino acid
        '''
        self.type = type
        self.position = [position[0], position[1]] # [row,column]
        self.connections = [connection]

    def __str__(self):
        """
        Returns a string representation of the amino acid
        """
        arrows = {
            "" : "",
            "up" : "↑",
            "down" : "↓",
            "left" : "←",
            "right" : "→",
        }
        return f"{self.type}{arrows[self.connections[0]]}"

    def check_energy(self):
        pass

    def add_connection(self, connection):
        if not connection in self.connections:
            self.connections.append(connection)


class Protein:

    def __init__(self, protein_length):
        '''
        Initialise a n x n matrix
        '''
        matrix_size = 2 * protein_length - 1

        self.acids = np.zeros((matrix_size, matrix_size), dtype = Acid)

    def __str__(self):

        string_matrix = ""
        length = len(self.acids[0])

        for row in self.acids:
            string_matrix += f"[{row[0]}"
            for i in range(1, length):
                string_matrix += f" {row[i]}"

            string_matrix += "]\n"

        return string_matrix

    def add_acid(self, type, position, connection):
        acid = Acid(type, position, connection)
        self.acids[position[0], position[1]] = acid

    def visualise(self):
        pass


def matrix_location(i, protein_length):
	"""
	Retrieve the matrix location from number
	"""
	column = i % protein_length
	row = np.floor(i / protein_length)
	return [row, column]


if __name__ == "__main__":

    test_protein = [["H",0,0], ["P",0,1], ["P",1,1], ["H",2,1], ["H",2,0], ["C",2,-1], ["H",1,-1], ["P",0, -1], ["H",-1,-1]]
    length_total = len(test_protein)

    protein = Protein(length_total)
    start_location = length_total - 1

    for acid in test_protein:
        type = acid[0]
        row = start_location - acid[2]
        column = start_location + acid[1]
        protein.add_acid(type, [row, column], "left")

    print(protein)
