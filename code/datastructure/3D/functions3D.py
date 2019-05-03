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

def new_location(location, direction):#, matrix_length):
    '''
    Determines the matrix location in a certain direction from another location
    TO DO: If the new location lies outside the matrix, returns ...?
    '''
    matrix_length = 100000000000

    row, column, layer = location

    if direction == "up" and row - 1 >= 0:
        new_location = [row - 1, column, layer]

    elif direction == "down" and row + 1 < matrix_length:
        new_location = [row + 1, column, layer]

    elif direction == "left" and column - 1 >= 0:
        new_location = [row, column - 1, layer]

    elif direction == "right" and column + 1 < matrix_length:
        new_location = [row, column + 1, layer]

    elif direction == "in" and layer + 1 < matrix_length:
        new_location = [row, column, layer + 1]

    elif direction == "out" and layer - 1 >= 0:
        new_location = [row, column, layer - 1]

    else:
        # print("unknown direction or new location outside matrix")
        '''
        random walk prints one at the end
        greedy prints these a lot
        branch n bound prints these a lot
        >>> Error in remove_acid
        '''
        new_location = location

    return new_location
