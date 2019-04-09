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

        self.acids = np.zeros((matrix_size, matrix_size))

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


if __name__ == "__main__":
    lol = protein(5)
    print(lol)

    hihi = acid("H", 13, "up")
    print(hihi)

    '''
    lol.add_acid(hihi)
    print(lol)
    '''
