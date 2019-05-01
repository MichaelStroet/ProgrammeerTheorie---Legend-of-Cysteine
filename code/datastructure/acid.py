# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

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
    	'''

    	'''

        self.connections["next"] = connection
