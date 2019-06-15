# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

"""
The Protein class is a matrix that will contain several acids that make up the
protein. It has several attributes of which the most important are its length,
energy and the acids it contains.
It contains several fuctions to access specific locations within this matrix,
add new acids, access pre-placed acids and (re)move them, calculate the energy...
"""
import numpy as np

from acid import Acid
from functions import opposite, new_location
from graph2D import plot2D
from graph3D import plot3D


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
        self.acid_list = []
        self.first_acid = [layer_mid, matrix_mid, matrix_mid]
        self.last_acid = self.first_acid
        self.layer_size = layer_size
        self.matrix_size = matrix_size
        self.energy = 0
        self.length = 0
        self.visited_states = 0

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
        self.acid_list.append(acid)
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
        self.acid_list.pop()
        self.last_acid = previous_location
        self.energy = previous_energy
        self.length -= 1

    def get_acid_index(self, index):
        '''
        Returns an acid object from a list
        '''
        return self.acid_list[index]

    def remove_acid_index(self, index):
        '''
        Removes an acid object and updates the energy
        '''
        acid = self.get_acid_index(index)
        self.energy -= self.calculate_energy(acid.location)
        self._update_acid_location(acid, None)

    def add_acid_index(self, index, location, direction):
        '''
        Adds an acid object based on an index
        '''
        acid = self.get_acid_index(index)
        self._update_acid_location(acid, location)
        self.energy += self.calculate_energy(acid.location)
        # Update connections
        self._update_acid_connections(index, direction)

    def _update_acid_connections(self, index: int, direction: str):
        '''
        Updates the connections of the acids
        '''
        acid = self.get_acid_index(index)

        # change the next connection of the previous acid
        if self.get_acid_index(index - 1).location:
            acid.connections["previous"] = opposite(direction)
            previous_acid = self.get_acid_index(index - 1)
            previous_acid.connections["next"] = direction

        # change the previous connection of the next acid
        elif self.get_acid_index(index + 1).location:
            acid.connections["next"] = opposite(direction)
            next_acid = self.get_acid_index(index + 1)
            next_acid.connections["previous"] = direction

    def _update_acid_location(self, acid, location):
        '''
        Updates locations for an acid
        '''
        # update matrix location
        if acid.location:
            z, y, x = acid.location
            self.acids[z, y, x] = 0

        # update acid location
        acid.location = location

        if location:
            z, y, x = location
            self.acids[z, y, x] = acid

    def neighbors(self, location):
        '''
        Gets all neighbouring acid objects from a central acid
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

        # Determine in which neighboring spots a new acid can be placed
        for direction, neighbor_location in neighbors.items():
            if self.get_acid(neighbor_location) == 0:
                # If the current protein is a straight line down, remove symmetrical options
                if current_row - first_row == self.length - 1:
                    if direction in ["down", "right", "out"]:
                        possible_sites[direction] = neighbor_location
                else:
                    possible_sites[direction] = neighbor_location

        return possible_sites

    def calculate_energy(self, location):
        '''
        Calculates the energy of an Acid object
        '''
        # Checks if the location contains an actual Acid object
        central_acid = self.get_acid(location)
        energy = 0

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
                        neighbor_type = acid.type

                        # If the neighbor pair is #-P, the energy doesn't change
                        if neighbor_type == "P":
                            energy -= 0

                        # If the neighbor pair is H-H or C-H, the energy decreases by 1
                        elif neighbor_type == "H":
                            energy -= 1

                        # If the neighbor pair is C-C, the energy decreases by 5
                        # If the neighbor pair is C-H, the energy decreases by 1
                        elif neighbor_type == "C":
                            if type == "C":
                                energy -= 5
                            else:
                                energy -= 1

                        else:
                            exit(f"Error: Unknown amino acid type '{neighbor_type}'")

            else:
                exit(f"Error: Unknown amino acid type '{type}'")

        return energy

    def new_energy(self, location):
        '''
        Updates the energy of the protein
        '''
        self.energy += self.calculate_energy(location)

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

        # Loop over each acid in the protein and add its info to the data lists
        acids_z = [acid.location[0] - start_layer for acid in self.acid_list]
        acids_y = [acid.location[1] - start_index for acid in self.acid_list]
        acids_x = [acid.location[2] - start_index for acid in self.acid_list]

        # Determine the minimal and maximum value of each dimension
        min_x, max_x = [min(acids_x), max(acids_x)]
        min_y, max_y = [min(acids_y), max(acids_y)]
        min_z, max_z = [min(acids_z), max(acids_z)]

        # Determine the largest distance from the first acid
        origin_distances = [abs(min_x), max_x, abs(min_y), max_y, abs(min_z), max_z]
        max_distance = max(origin_distances)

        # Return the minimal matrix size
        return (max_distance * 2) + 1

    def state_space_visited(self):
        self.visited_states += 1

    def competition_format(self):

        direction_to_number = {
            "up" : 2,
            "down" : -2,
            "left" : -1,
            "right" : 1,
            "in" : 3,
            "out" : -3
        }

        steps = []

        location = self.first_acid

        # Loop over each acid in the protein and add the next step to the list
        acid = self.get_acid(location)
        next_connection = acid.connections["next"]

        while not next_connection == "":

            steps.append(direction_to_number[next_connection])

            # Determine the location of the next acid
            location = new_location(location, acid.connections["next"], self.layer_size, self.matrix_size)

            acid = self.get_acid(location)
            next_connection = acid.connections["next"]

        print(steps)
        return str(steps)[1:-1]
