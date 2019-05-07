# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

from acid3D import Acid
#from graph import visualise as plot
from functions3D import opposite, new_location

class Protein:

    def __init__(self, protein_length, dimension):
        '''
        Initialise a list of n 'n x n' matrices of Acid objects
        '''
        matrix_size = int(protein_length / 1.)

        # Ensure odd matrix_size
        if matrix_size % 2 == 0:
            matrix_size += 1

        matrix_mid = int((matrix_size - 1) / 2)

        if dimension == "3D":
            layer_mid = matrix_mid
            layer_size = matrix_size
        else:
            layer_mid = 0
            layer_size = 1


        self.acids = np.zeros((layer_size, matrix_size, matrix_size), dtype = Acid)
        self.first_acid = [layer_mid, matrix_mid, matrix_mid]
        self.last_acid = self.first_acid
        self.energy = 0
        self.length = 0

    def __str__(self):
        '''
        Returns a string representation of the acid matrix
        '''

        string_matrix = ""
        matrix_length = len(self.acids)

        # For each column in each row, add the Acid object to the matrix string
        for i, layer in zip(range(len(self.acids)), self.acids):
            string_matrix += f"{i}\n"

            for row in layer:
                string_matrix += "["

                for column in row:
                    string_matrix += f" {column}"

                string_matrix += " ]\n"

        return string_matrix

    def add_acid(self, type, location, direction_new_acid):
        '''
        Adds a new acid object to the acid matrix
        '''
        layer, row, column = location
        acid = Acid(type, location, opposite(direction_new_acid))
        self.acids[layer, row, column] = acid
        self.last_acid = location
        self.length += 1

    def remove_acid(self, previous_energy):
        '''
        Removes an acid object from the acids matrix
        TO DO: Removes the last acid object from the matrix
        '''
        last_location = self.last_acid
        layer, row, column = last_location

        last_acid = self.acids[layer, row, column]
        last_connections = last_acid.connections
        layer_length = len(self.acids)
        matrix_length = len(self.acids[0])

        prev_connection = last_connections["previous"]
        
        prev_layer, prev_row, prev_column = new_location(last_location, prev_connection, layer_length, matrix_length)
        prev_acid = self.acids[prev_layer, prev_row, prev_column]

        prev_acid.connections["next"] = ""

        self.acids[layer, row, column] = 0
        self.last_acid = [prev_layer, prev_row, prev_column]
        self.energy = previous_energy
        self.length -= 1

    def neighbors(self, location):
        '''
        Gets all neighboring acid objects from a central acid
        and returns a dictionary of the location for each direction.
        TO DO: rework for one for loop and smaller matrices
        '''
        directions = ["up", "down", "left", "right", "in", "out"]
        neighbor_acids = {}

        # Get the locations of all neighbors
        for direction in directions:
            site = new_location(location, direction, len(self.acids), len(self.acids[0]))
            if site:
                neighbor_acids[direction] = site

        return neighbor_acids

    def check_energy(self, location, type):
        '''
        Calculates the energy of a newly placed Acid object and returns an integer
        '''
        layer, row, column = location

        # Checks if the location contains an actual Acid object
        central_acid = self.acids[layer, row, column]
        if not central_acid == 0:

            # If the acid is polar, the energy stays the same
            if type == "P":
                return 0

            elif type == "H" or type == "C":

                central_connections = central_acid.connections.values()

                # Get the neighboring locations
                neighbor_acids = self.neighbors(location)

                new_energy = 0

                # Loop over each neighbor and check the new energy
                for direction in neighbor_acids:
                    layer, row, column = neighbor_acids[direction]
                    acid = self.acids[layer, row, column]

                    if not acid == 0 and not direction in central_connections:

                        # If the neighbor pair is H-H or H-C, the energy decreases by 1
                        if type == "H":
                            if acid.type == "H" or acid.type == "C":
                                new_energy -= 1

                        # If the neighbor pair is C-H, the energy decreases by 1,
                        # and if it is C-C, the energy decreases by 5
                        else:
                            if acid.type == "H":
                                new_energy -= 1

                            elif acid.type == "C":
                                new_energy -= 5

                return new_energy

            else:
                print(f"Unknown amino acid type: '{type}'")
                exit(1)

        else:
            return 0

    def visualise(self, protein_string):
        '''
        Visualises the protein object in a 3D ? plot
        '''

        # Determine the middle (start) of the matrix
        matrix_length = len(self.acids)
        start_index = int((matrix_length - 1) / 2.)
        layer, row, column = [start_index, start_index, start_index]

        acid_data = []
        matrix_data = []

        # Matrix corner coordinates
        low = (0 - 1) - start_index
        high = (matrix_length) - start_index

        # Data for plotting the matrix borders
        matrix_data = [
            [low, low, low],
            [low, high, low],
            [low, high, low],
            [low, high, high],
            [high, low, low],
            [high, high, low],
            [high, low, high],
            [high, high, high]
        ]

        # Loop over each acid in the protein and add its info to the data list
        acid = self.acids[layer, row, column]

        while not acid.connections["next"] == "":

            acid = self.acids[layer, row, column]

            acid_type = acid.type
            acid_x = acid.position[0] - start_index
            acid_y = acid.position[1] - start_index
            acid_z = acid.position[2] - start_index

            acid_data.append([acid_type, acid_x, acid_y])
            layer, row, column = new_location([layer, row, column], acid.connections["next"], len(self.acids), len(self.acids[0]))

        # Plot the acid_data list
        print(acid_data, protein_string, self.energy)
        print(matrix_data)

if __name__ == "__main__":

    string = "HPHPHPHH"
    length = len(string)
    protein = Protein(length)

    print(protein)
