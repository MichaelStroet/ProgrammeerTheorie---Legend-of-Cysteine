# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

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
