# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

class Acid:

    def __init__(self, type, location, previous_connection):
        '''
        Initialise an amino acid
        '''
        layer, row, column = location

        self.type = type
        self.position = [layer, row, column]
        self.connections = {
            "previous" : previous_connection,
            "next" : ""
            }


    def __str__(self):
        '''
        Returns a string representation of the amino acid
        '''

        arrows = {
            "" : " ",
            "first" : "▼",
            "in" : "X",
            "out" : "•",
            "up" : "↑",
            "down" : "↓",
            "left" : "←",
            "right" : "→",
        }

        return f"{self.type}{arrows[self.connections['next']]}"


    def add_connection(self, connection):
        '''
        Adds the next connection to the amino acid
        '''
        self.connections["next"] = connection
