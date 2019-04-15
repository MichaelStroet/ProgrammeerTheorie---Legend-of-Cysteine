# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

class Acid:

    def __init__(self, type, position, connection):
        '''
        Initialise an amino acid
        '''
        self.type = type
        self.position = [position[0], position[1]] # [row,column]
        self.connections = [connection]

    def __str__(self):
        '''
        Returns a string representation of the amino acid
        '''
        arrows = {
            "" : "",
            "up" : "↑",
            "down" : "↓",
            "left" : "←",
            "right" : "→",
        }
        return f"{self.type}{arrows[self.connections[0]]}"

    def add_connection(self, connection):
        if not connection in self.connections:
            self.connections.append(connection)


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
        length = len(self.acids[0])

        for row in self.acids:
            string_matrix += f"[{row[0]}"
            for i in range(1, length):
                string_matrix += f" {row[i]}"

            string_matrix += "]\n"

        return string_matrix

    def add_acid(self, type, position, connection):
        '''
        Adds an acid object to the acids matrix
        '''
        acid = Acid(type, position, connection)
        self.acids[position[0], position[1]] = acid
        self.length += 1

    def neighbors(self, location):
        '''
        Gets the four neighboring acid objects from a central acids
        '''

        loc_up = [location[0] - 1, location[1]]
        loc_down = [location[0] + 1, location[1]]
        loc_left = [location[0], location[1] - 1]
        loc_right = [location[0], location[1] + 1]

        directions = ["up", "down", "left", "right"]
        locations = [loc_up, loc_down, loc_left, loc_right]

        neighbor_acids = {}

        #print(f"row: {location[0]}, column: {location[1]}")
        for direction, location in zip(directions, locations):
            #print(f"direction: {direction}, location: {location}")

            if 0 <= location[0] <= (len(self.acids) - 1) and 0 <= location[1] <= (len(self.acids) - 1):
                acid = self.acids[location[0], location[1]]
                neighbor_acids[direction] = location

        #print(f"neighbor_acids: {neighbor_acids}")
        return neighbor_acids

    def check_energy(self, location, type):
        '''
        input is the location of the acid you want to check the energy of, type is the acid type "P"/"H"/"C"
        Calculates the energy of a amino acid and its unconnected neighbors
        '''

        # If acid is polair energy is 0
        if type == "P":
            return 0

        # If acid is hydrofobic energy
        elif type == "H" or type == "C":

            central_acid = self.acids[location[0], location[1]]
            acids = self.neighbors(location)
            print(acids)

            for direction in ["up", "down", "left", "right"]:
                location = acids[direction]
                acid = self.acids[location[0], location[1]]

                if acid == 0 or direction in acid.connections:
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

    def visualise(self):
        pass


if __name__ == "__main__":

    test_protein = [["H",0,0], ["P",0,1], ["P",1,1], ["H",2,1], ["H",2,0], ["C",2,-1], ["H",1,-1], ["P",0, -1], ["H",-1,-1]]
    length_total = len(test_protein)

    protein = Protein(length_total)
    start_location = length_total - 1

    for acid in test_protein:
        type = acid[0]
        row = start_location - acid[2]
        column = start_location + acid[1]
        protein.add_acid(type, [row, column], "left")

    protein.check_energy([start_location,start_location], "H")
    print(protein)
