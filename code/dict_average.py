# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

def dict_average(dict):
    '''
    Calculates the average key value for a dictionary with integer keys and values as frequency
    '''

    total_sum = 0

    for key, value in dict.items():
        total_sum += key * value

    values = dict.values()

    return total_sum / sum(values)
