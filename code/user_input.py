# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

def is_integer(string):
    '''
    Determines if the given string represents an integer
    '''
    try:
        int(string)
        return True
    except ValueError:
        return False

def is_float(string):
    '''
    Determines if the given string represents a float
    '''
    try:
        float(string)
        return True
    except ValueError:
        return False

def ask_integer(message):
    '''
    Asks the user for an integer
    '''
    # Keep asking until the user enters a integer
    user_input = input(message)
    while not is_integer(user_input):
        user_input = input(message)

    return int(user_input)

def ask_float(message):
    '''
    Asks the user for a float
    '''
    # Keep asking until the user enters a float
    user_input = input(message)
    while not is_float(user_input):
        user_input = input(message)

    return float(user_input)

def ask_number(lower_limit, upper_limit, answer_type, message):
    '''
    Asks the user for a valid integer or float in a certain range
    '''
    # Keep asking for a number until the user enters a valid integer
    if answer_type == "integer":
        number = ask_integer(message)
        while number < lower_limit or number > upper_limit:
            number = ask_integer(message)

    # Keep asking for a number until the user enters a valid float
    elif answer_type == "float":
        number = ask_float(message)
        while number < lower_limit or number > upper_limit:
            number = ask_float(message)

    else:
        print(f"Error: Unknown type {answer_type}")
        exit(1)

    print(f">{number}\n")

    return number

def ask_matrix_size(protein_length):

        # Calculate the Length / 2 matriz size
        length_2div3 = int(np.ceil(2 * protein_length / 3.))
        length_1div2 = int(np.ceil(protein_length / 2.))
        length_1div3 = int(np.ceil(protein_length / 3.))
        length_1div4 = int(np.ceil(protein_length / 4.))

        # Ask the user for the matrix size
        lower_limit = int(np.ceil(protein_length**0.5))
        upper_limit = int(2 * protein_length - 1)

        print(f"Protein length: {protein_length}")
        print(f"2/3 of length : {length_2div3}")
        print(f"1/2 of length : {length_1div2}")
        print(f"1/3 of length : {length_1div3}")
        print(f"1/4 of length : {length_1div4}\n")

        matrix_size = ask_number(lower_limit, upper_limit, "integer", f"What matrix_size to use [{lower_limit}-{upper_limit}]?: ")

        # Ensure odd matrix_size
        if matrix_size % 2 == 0:
            matrix_size += 1
            
        return matrix_size

def print_list(list):
    '''
    Prints all elements of a list with indeces starting from 1
    '''

    for i, element in zip(range(len(list)), list):
        print(f"{i + 1}: {element}")
    print()

def choose(options, message):
    '''
    Asks the user to make a choice from a list of options
    '''

    # Print the options
    print_list(options)

    # Keep asking until the user enters a valid number
    choice = ask_integer(message) - 1
    while choice < 0 or choice > len(options) - 1:
        choice = ask_integer(message) - 1

    print(f">{options[choice]}\n")

    return options[choice]

def get_choices(save_results, show_results, dimensions, algorithms, proteins):
    '''
    Asks the user to choose from multiple lists of options and returns the answers as a list
    '''

    save = choose(save_results, f"Do you want to save results to file [1-{len(save_results)}]?: ")
    show = choose(show_results, f"Do you want to show/print the results [1-{len(show_results)}]?: ")
    dimension = choose(dimensions, f"Choose the dimensions [1-{len(dimensions)}]: ")
    algorithm = choose(algorithms, f"Choose an algorithm [1-{len(algorithms)}]: ")
    protein = choose(proteins, f"Choose a protein [0-{len(proteins)}]: ")

    return [save, show, dimension, algorithm, protein]
