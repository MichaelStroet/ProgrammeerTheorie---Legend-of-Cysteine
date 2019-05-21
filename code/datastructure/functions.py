# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

def opposite(direction):
    '''
    Returns the opposite direction of the given direction
    '''
    opposite_directions = {
    "" : "",
    "up" : "down",
    "down" : "up",
    "left" : "right",
    "right" : "left",
    "in" : "out",
    "out" : "in"
    }

    return opposite_directions[direction]
    

def new_location(location, direction, layer_length, matrix_length):
    '''
    Determines the matrix location in a certain direction from another location
    TO DO: If the new location lies outside the matrix, returns ...?
    '''
    layer, row, column = location

    if direction == "":
        return location

    elif direction == "up" and row - 1 >= 0:
        return [layer, row - 1, column]

    elif direction == "down" and row + 1 < matrix_length:
        return [layer, row + 1, column]

    elif direction == "left" and column - 1 >= 0:
        return [layer, row, column - 1]

    elif direction == "right" and column + 1 < matrix_length:
        return [layer, row, column + 1]

    elif direction == "in" and layer + 1 < layer_length:
        return [layer + 1, row, column]

    elif direction == "out" and layer - 1 >= 0:
        return [layer - 1, row, column]

    else:
        return False
