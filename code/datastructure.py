# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

class protein():
    pass

    def __init__(self, protein_length):
        '''
        Initialise a n x n matrix
        '''
        matrix_size = 2 * protein_length - 1

        self.acids = np.zeros((matrix_size, matrix_size))
        self.acids[1][2] = 12

    def __str__(self):
        """Returns a string representation of the item"""

        test = self.acids.tostring()
        test2 = np.fromstring(test)
        print(test)
        print(test2)
        print(self.acids)
        return "nope"


class acid:
    pass

'''
Representatie?
    Matrix
    Coordinaten
'''


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

