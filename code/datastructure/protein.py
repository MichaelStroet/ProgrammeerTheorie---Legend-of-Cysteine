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
        Initialise a n x n matrix
        '''
        matrix_size = 2 * protein_length - 1

        self.acids = np.zeros((matrix_size, matrix_size), dtype = Acid)
        self.energy = 0
        self.length = 0


    def __str__(self):
        '''
        Returns a string representation of the acids matrix
        '''
        string_matrix = ""
        length = len(self.acids)

        for row in self.acids:
            string_matrix += f"[{row[0]}"
            for i in range(1, length):
                string_matrix += f" {row[i]}"

            string_matrix += "]\n"

        return string_matrix


    def add_acid(self, type, position, direction_new_acid):
        '''
        Adds an acid object to the acids matrix
        '''

        acid = Acid(type, position, opposite(direction_new_acid))
        self.acids[position[0], position[1]] = acid
        self.length += 1


    def remove_acid(self, location, previous_energy):
        '''
        Removes an acid object from the acids matrix
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
        Gets the four neighboring acid objects from a central acids, returns dict
        '''

        directions = ["up", "down", "left", "right"]
        locations = []

        for direction in directions:
            locations.append(new_location(location, direction))

        neighbor_acids = {}

        for direction, location in zip(directions, locations):

            if 0 <= location[0] <= (len(self.acids) - 1) and 0 <= location[1] <= (len(self.acids) - 1):
                acid = self.acids[location[0], location[1]]
                neighbor_acids[direction] = location

        return neighbor_acids


    def check_energy(self, location, type):
        '''
        input is the location of the acid you want to check the energy of, type is the acid type: "P"/"H"/"C"
        Calculates the energy of an amino acid and its unconnected neighbors
        '''

        # If acid is polair energy does not change
        if type == "P":
            return 0

        # If acid is hydrofobic energy is decreased by -1 (type = "H") or -5 (type = "C")
        elif type == "H" or type == "C":

            central_acid = self.acids[location[0], location[1]]
            central_connections = central_acid.connections.values()
            acids = self.neighbors(location)

            for direction in ["up", "down", "left", "right"]:

                if direction in acids:
                    location = acids[direction]
                    acid = self.acids[location[0], location[1]]

                    if acid == 0 or direction in central_connections:
                        del acids[direction]

            new_energy = 0

            for direction in acids:
                location = acids[direction]
                acid = self.acids[location[0], location[1]]

                if type == "H":
                    if acid.type == "H" or acid.type == "C":
                        new_energy -= 1

                else:
                    if acid.type == "H":
                        new_energy -= 1

                    elif acid.type == "C":
                        new_energy -= 5

            return new_energy

        else:
            print(f"Unknown amino acid type: '{type}'")
            exit(1)


    def visualise(self, protein_string):
        '''

        '''

        length_protein = int((len(self.acids) + 1) / 2.)

        location = [length_protein - 1, length_protein - 1]
        acid = self.acids[location[0], location[1]]

        acid_data = []

        while not acid.connections["next"] == "":

            acid = self.acids[location[0], location[1]]

            acid_type = acid.type
            acid_x = acid.position[0] - length_protein + 1
            acid_y = acid.position[1] - length_protein + 1

            acid_data.append([acid_type, acid_x, acid_y])
            location = new_location(location, acid.connections["next"])

        plot(acid_data, protein_string, self.energy)
