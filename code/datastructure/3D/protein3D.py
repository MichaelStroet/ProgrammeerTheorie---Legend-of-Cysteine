# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

from acid3D import Acid
#from graph import visualise as plot
#from functions import opposite, new_location

class Protein:

    def __init__(self, protein_length):
        '''
        Initialise a n x n matrix for Acid object
        '''
        matrix_size = 2 * protein_length - 1

        self.acids = np.zeros((matrix_size, matrix_size, matrix_size), dtype = Acid)
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

    def add_acid(self, type, position, direction_new_acid):
        '''
        Adds a new acid object to the acid matrix
        '''
        acid = Acid(type, position, opposite(direction_new_acid))
        self.acids[position[0], position[1]] = acid
        self.length += 1

    def remove_acid(self, location, previous_energy):
        '''
        Removes an acid object from the acids matrix
        TO DO: Removes the last acid object from the matrix
        '''
        acid_connections = self.acids[location[0], location[1]].connections

        for key in ["previous", "next"]:
            connection = acid_connections[key]
            neighbor_location = new_location(location, connection)
            neighbor_acid = self.acids[neighbor_location[0], neighbor_location[1]]

            neighbor_acid.connections["next"] = ""

        self.acids[location[0], location[1]] = 0
        self.energy = previous_energy
        self.length -= 1

    def neighbors(self, location):
        '''
        Gets all neighboring acid objects from a central acid
        and returns a dictionary of the location for each direction.
        TO DO: rework for one for loop and smaller matrices
        '''
        directions = ["up", "down", "left", "right"]
        locations = []

        # Get the locations of all neighbors
        for direction in directions:
            locations.append(new_location(location, direction))#, matrix_length))

        neighbor_acids = {}

        # Loop over each direction and its location
        for direction, location in zip(directions, locations):

            # If the new location lies within the matrix, add the object to the dictionary
            if 0 <= location[0] <= (len(self.acids) - 1) and 0 <= location[1] <= (len(self.acids) - 1):
                acid = self.acids[location[0], location[1]]
                neighbor_acids[direction] = location

        return neighbor_acids

    def check_energy(self, location, type):
        '''
        Calculates the energy of a newly placed Acid object and returns an integer
        '''

        # Checks if the location contains an actual Acid object
        central_acid = self.acids[location[0], location[1]]
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
                    acid = self.acids[location[0], location[1]]

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
        location = [start_index, start_index]

        acid_data = []

        # Loop over each acid in the protein and add its info to the data list
        acid = self.acids[location[0], location[1]]

        while not acid.connections["next"] == "":

            acid = self.acids[location[0], location[1]]

            acid_type = acid.type
            acid_x = acid.position[0] - start_index
            acid_y = acid.position[1] - start_index

            acid_data.append([acid_type, acid_x, acid_y])
            location = new_location(location, acid.connections["next"])

        # Plot the acid_data list
        plot(acid_data, protein_string, self.energy)

if __name__ == "__main__":

    string = "HPHPHPHH"
    length = len(string)
    protein = Protein(length)

    print(protein)
