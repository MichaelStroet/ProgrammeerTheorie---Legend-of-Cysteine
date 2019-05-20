# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

from acid import Acid
from graph2D import plot2D
from graph3D import plot3D
from functions import opposite, new_location

class Protein:

    def __init__(self, matrix_size, dimension):
        '''
        Initialise a list of m 'n x n' matrices of Acid objects
        '''

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
        self.layer_size = layer_size
        self.matrix_size = matrix_size
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

    def place_first_two(self, protein_string):
        '''
        Places the first two amino acids
        '''
        # Place the first acid
        location = self.first_acid
        self.add_acid(protein_string[0], location, "")
        self.get_acid(location).add_connection("down")

        # Place the second acid underneath the first
        location = [location[0], location[1] + 1, location[2]]
        self.add_acid(protein_string[1], location, "down")

    def get_acid(self, location):
        '''
        Finds and returns the object at that location in the matrix
        '''
        return self.acids[location[0], location[1], location[2]]

    def add_acid(self, type, location, direction_previous):
        '''
        Adds a new acid object to the acid matrix
        '''
        # Create the acid object
        acid = Acid(type, location, opposite(direction_previous))

        # Add the acid object to the matrix and update the protein properties
        self.acids[location[0], location[1], location[2]] = acid
        self.last_acid = location
        self.length += 1

    def remove_acid(self, previous_energy):
        '''
        Removes the last acid object from the matrix
        '''
        # Get the location and 'previous' connection from the last acid of the protein
        last_location = self.last_acid
        last_acid = self.get_acid(last_location)
        last_connection = last_acid.connections["previous"]

        # Get the location of the second to last acid location
        previous_location = new_location(last_location, last_connection, self.layer_size, self.matrix_size)
        prev_acid = self.get_acid(previous_location)

        # Set the 'next' conncection of the previous acid to none
        prev_acid.connections["next"] = ""

        # Remove the last acid and update the protein properties
        self.acids[last_location[0], last_location[1], last_location[2]] = 0
        self.last_acid = previous_location
        self.energy = previous_energy
        self.length -= 1

    def neighbors(self, location):
        '''
        Gets all neighboring acid objects from a central acid
        and returns a dictionary of the location for each direction.
        '''
        directions = ["up", "down", "left", "right", "in", "out"]
        neighbor_acids = {}

        # Get the locations of all neighbors
        for direction in directions:
            site = new_location(location, direction, self.layer_size, self.matrix_size)
            if site:
                neighbor_acids[direction] = site

        return neighbor_acids

    def possible_sites(self, location):
        '''
        Determines the possible sites for placing a new acid
        '''
        possible_sites = {}

        first_row = self.first_acid[1]
        current_row = location[1]

        # Get the acid objects surrounding the last-placed acid
        neighbors = self.neighbors(location)

        '''
        TO DO: First step into a new dimension is symmetrical!
        '''
        # Determine in which neighboring spots a new acid can be placed
        for direction, neighbor_location in neighbors.items():
            if self.get_acid(neighbor_location) == 0:
                # If the current protein is a straight line down, remove symmetrical options
                if current_row - first_row == self.length - 1:
                    if direction in ["down", "left", "out"]:
                        possible_sites[direction] = neighbor_location
                else:
                    possible_sites[direction] = neighbor_location

        return possible_sites

    def new_energy(self, location):
        '''
        Calculates the energy of an Acid object and updates the energy property
        '''
        # Checks if the location contains an actual Acid object
        central_acid = self.get_acid(location)
        if not central_acid == 0:

            type = central_acid.type

            # If the acid is polar, the energy stays the same
            if type == "P":
                return 0

            elif type == "H" or type == "C":

                central_connections = central_acid.connections.values()

                # Get the neighboring locations
                neighbor_acids = self.neighbors(location)

                # Loop over each neighbor and check the new energy
                for direction, location in neighbor_acids.items():
                    acid = self.get_acid(location)

                    if not acid == 0 and not direction in central_connections:

                        # If the neighbor pair is H-H, the energy decreases by 1,
                        # If the neighbor pair is H-C, the energy decreases by 1,
                        if type == "H":
                            if acid.type == "H" or acid.type == "C":
                                self.energy -= 1

                        # If the neighbor pair is C-H, the energy decreases by 1,
                        # If the neighbor pair is C-C, the energy decreases by 5
                        else:
                            if acid.type == "H":
                                self.energy -= 1

                            elif acid.type == "C":
                                self.energy -= 5

            else:
                print(f"Unknown amino acid type: '{type}'")
                exit(1)

        else:
            return 0

    def check_energy(self, location, type):
        '''
        Calculates the energy of an Acid object and returns an integer
        TO DO: Remove type and make clear this can check any random acid
        '''
        # Checks if the location contains an actual Acid object
        central_acid = self.get_acid(location)
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
                for direction, neighbor_location in neighbor_acids.items():
                    acid = self.get_acid(neighbor_location)

                    if not acid == 0 and not direction in central_connections:

                        # If the neighbor pair is H-H, the energy decreases by 1,
                        # If the neighbor pair is H-C, the energy decreases by 1,
                        if type == "H":
                            if acid.type == "H" or acid.type == "C":
                                new_energy -= 1

                        # If the neighbor pair is C-H, the energy decreases by 1,
                        # If the neighbor pair is C-C, the energy decreases by 5
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
        Visualises the protein object in a 2D or 3D plot
        '''
        # Set the first location to the first acid and get the begin indeces of the matrix
        location = self.first_acid
        start_layer = location[0]
        start_index = location[1]

        acid_data = []

        # Loop over each acid in the protein and add its info to the data list
        acid = self.get_acid(location)
        while not acid.connections["next"] == "":
            acid = self.get_acid(location)

            acid_type = acid.type

            # Determine the location relative to the first acid
            acid_x = acid.location[1] - start_index
            acid_y = acid.location[2] - start_index
            acid_z = acid.location[0] - start_layer

            acid_data.append([acid_type, acid_x, acid_y, acid_z])

            # Determine the location of the next acid
            location = new_location(location, acid.connections["next"], self.layer_size, self.matrix_size)

        # Plot the protein
        # In 2D
        if self.layer_size == 1:
            plot2D(acid_data, protein_string, self.energy)
        # In 3D
        else:
            plot3D(acid_data, protein_string, self.energy)

    def smallest_matrix(self):
        '''
        Determines the smallest matrix size in which the current protein can fit
        '''
        # Set the first location to the first acid and get the begin indeces of the matrix
        location = self.first_acid
        start_layer = location[0]
        start_index = location[1]

        acids_x = []
        acids_y = []
        acids_z = []

        # Loop over each acid in the protein and add its info to the data lists
        acid = self.get_acid(location)
        while not acid.connections["next"] == "":
            acid = self.get_acid(location)
            layer, row, column = location

            acids_x.append(column - start_index)
            acids_y.append(row - start_index)
            acids_z.append(layer - start_layer)

            # Adjust the layer, row and column for the next acid
            location = new_location(location, acid.connections["next"], self.layer_size, self.matrix_size)

        # Determine the minimal and maximum value of each dimension
        min_x, max_x = [min(acids_x), max(acids_x)]
        min_y, max_y = [min(acids_y), max(acids_y)]
        min_z, max_z = [min(acids_z), max(acids_z)]

        # Determine the largest distance from the first acid
        origin_distances = [abs(min_x), max_x, abs(min_y), max_y, abs(min_z), max_z]
        max_distance = max(origin_distances)

        # Return the minimal matrix size
        return (max_distance * 2) + 1
