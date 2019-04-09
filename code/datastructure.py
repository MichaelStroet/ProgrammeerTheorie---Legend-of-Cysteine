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

if __name__ == "__main__":
    lol = protein(5)
    print(lol)
