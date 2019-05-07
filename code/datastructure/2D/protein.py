# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

from acid import Acid
from graph import visualise as plot
from functions import opposite, new_location

class Protein:

    def __init__(self, protein_length):
        '''
        Initialise a n x n matrix of Acid objects
        '''
        matrix_size = int(protein_length / 1.)

        # Ensure odd matrix_size
        if matrix_size % 2 == 0:
            matrix_size += 1

        matrix_mid = int(matrix_size/2)

        self.acids = np.zeros((matrix_size, matrix_size), dtype = Acid)
        self.last_acid = [0, 0]
        self.energy = 0
        self.length = 0
        self.first_acid = [matrix_mid, matrix_mid]  

    def __str__(self):
        '''
        Returns a string representation of the acid matrix
        '''

        string_matrix = ""
        matrix_length = len(self.acids)

        # For each column in each row, add the Acid object to the matrix string
        for row in self.acids:
            string_matrix += f"[{row[0]}"
            for i in range(1, matrix_length):
                string_matrix += f" {row[i]}"

            string_matrix += "]\n"

        return string_matrix

    def add_acid(self, type, location, direction_new_acid):
        '''
        Adds a new acid object to the acid matrix
        '''
        row, column = location

        acid = Acid(type, location, opposite(direction_new_acid))
        self.acids[row, column] = acid
        self.last_acid = location
        self.length += 1

    def remove_acid(self, previous_energy):
        '''
        Removes an acid object from the acids matrix
        TO DO: Removes the last acid object from the matrix
        '''
        row, column = self.last_acid
        acid_connections = self.acids[row, column].connections

        previous_connection = acid_connections["previous"]

        previous_row, previous_column = new_location([row, column], previous_connection, len(self.acids))
        previous_acid = self.acids[previous_row, previous_column]

        previous_acid.connections["next"] = ""

        self.acids[row, column] = 0
        self.last_acid = [previous_row, previous_column]
        self.energy = previous_energy
        self.length -= 1

    def neighbors(self, location):
        '''
        Gets all neighboring acid objects from a central acid
        and returns a dictionary of the location for each direction.
        TO DO: rework for one for loop and smaller matrices
        '''
        directions = ["up", "down", "left", "right"]
        neighbor_acids = {}

        # Get the locations of all neighbors
        for direction in directions:
            site = new_location(location, direction, len(self.acids))
            if site:
                neighbor_acids[direction] = site

        return neighbor_acids

    def check_energy(self, location, type):
        '''
        Calculates the energy of a newly placed Acid object and returns an integer
        '''
        row, column = location

        # Checks if the location contains an actual Acid object
        central_acid = self.acids[row, column]
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
                    location = neighbor_acids[direction]
                    acid = self.acids[row, column]

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
        Visualises the protein object in a 2D matplotlib plot
        '''

        # Determine the middle (start) of the matrix
        matrix_length = len(self.acids)

        start_index = int((matrix_length - 1) / 2.)
        row, column = [start_index, start_index]

        acid_data = []
        matrix_data = []

        # Matrix corner coordinates
        low = (0 - 1) - start_index
        high = (matrix_length) - start_index

        # Data for plotting the matrix borders
        matrix_data = [
            [low, low],
            [low, high],
            [high, high],
            [high, low],
            [low, low]
        ]

        # Loop over each acid in the protein and add its info to the data list
        acid = self.acids[row, column]

        while not acid.connections["next"] == "":

            acid = self.acids[row, column]

            acid_type = acid.type
            acid_x = acid.position[0] - start_index
            acid_y = acid.position[1] - start_index

            acid_data.append([acid_type, acid_x, acid_y])
            row, column = new_location([row, column], acid.connections["next"], len(self.acids))

        # Plot the acid_data list
        plot(acid_data, matrix_data, protein_string, self.energy)
