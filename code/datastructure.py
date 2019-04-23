# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

def opposite(direction):

    opposite_directions = {
        "" : "",
        "up" : "down",
        "down" : "up",
        "left" : "right",
        "right" : "left"
        }

    return opposite_directions[direction]

def new_location(location, direction):

    if direction == "up":
        new_location = [location[0] - 1, location[1]]

    elif direction == "down":
        new_location = [location[0] + 1, location[1]]

    elif direction == "left":
        new_location = [location[0], location[1] - 1]

    elif direction == "right":
        new_location = [location[0], location[1] + 1]

    else:
        new_location = location

    return new_location

class Acid:

    def __init__(self, type, position, previous_connection):
        '''
        Initialise an amino acid
        '''
        self.type = type
        self.position = [position[0], position[1]] # [row,column]
        self.connections = {
            "previous" : previous_connection,
            "next" : ""
            }

    def __str__(self):
        '''
        Returns a string representation of the amino acid
        '''
        arrows = {
            "" : "",
            "first" : "▼",
            "up" : "↑",
            "down" : "↓",
            "left" : "←",
            "right" : "→",
        }

        return f"{self.type}{arrows[self.connections['next']]}"

    def add_connection(self, connection):
            self.connections["next"] = connection


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

    def visualise(self):
        pass


if __name__ == "__main__":

    # test_protein = [["H",0,0], ["P",0,1], ["P",1,1], ["H",2,1], ["H",2,0], ["C",2,-1], ["H",1,-1], ["P",0, -1], ["H",-1,-1]]

    test_protein = [
        ["H", 0, 0, ["first",""]],
        ["U", 1, 0, ["down","down"]],
        ["C", 2, 0, ["down","down"]],
        ["D", 3, 0, ["down","down"]],
        ["P", 4, 0, ["", "down"]]
    ]

    length_total = len(test_protein)

    protein = Protein(length_total)
    start_location = length_total - 1

    for acid in test_protein:
        type = acid[0]
        row = start_location + acid[1]
        column = start_location + acid[2]
        connections = acid[3]
        protein.add_acid(type, [row, column], connections[1])
        protein.acids[row, column].add_connection(connections[0])

    print("Before removal:")
    print(protein)

    protein.remove_acid([start_location + 3, start_location + 0])

    print("After removal:")
    print(protein)
