# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

class protein():

    def __init__(self, protein_length):
        '''
        Initialise a n x n matrix
        '''
        matrix_size = 2 * protein_length - 1

        self.acids = np.zeros((matrix_size, matrix_size), dtype = acid)
        self.acids[2][2] = 12

    def __str__(self):

        print(self.acids)
        return ""


class acid:

    def __init__(self, type, position, connection):
        '''
        Initialise an amino acid
        '''
        self.type = type
        self.position = position
        self.connections = [connection]

    def __str__(self):
        """
        Returns a string representation of the amino acid
        """

        return f"Amino acid of type {self.type} at matrix point {self.position} and is connected to other acids in the {self.connections} direction(s)."



def matrix_location(i, protein_length):
	"""
	Retrieve the matrix location from number
	"""
	column = i % protein_length
	row = np.floor(i / protein_length)
	return(column, row)


if __name__ == "__main__":
    location = 12
    protein_length = 5
    matrix = protein(protein_length)
    print(matrix)
    print(matrix_location(location, protein_length))

    aminozuur = acid("H", location, "up")
    print(aminozuur)

    print(matrix.acids[2][2])
    print(matrix.acids[2, 2])

    matrix.acids[1,1] = aminozuur
    print(matrix.acids)
