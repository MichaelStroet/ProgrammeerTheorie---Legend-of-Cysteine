# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


'''
This function draws two plots of a folded protein in 2D
'''
def visualise(protein, matrix, protein_string, protein_energy):

    # Assign each amino acid a color
    colors = {
        "H" : "red",
        "P" : "blue",
        "C" : "yellow",
    }

    # Create lists to contain the color and coordinates of each amino acid
    L_color = []
    protein_x = []
    protein_y = []

    # Fill the lists for each amino acid
    for acid in protein:
        L_color.append(colors[acid[0]])
        protein_x.append(acid[1])
        protein_y.append(acid[2])

    # Determine the minimum and maximum values of x and y
    x_min = min(protein_x) - 1
    x_max = max(protein_x) + 1
    y_min = min(protein_y) - 1
    y_max = max(protein_y) + 1

    '''
    Figure n.1: Folded protein
    This figure shows a closeup of the folded protein
    '''
    plt.figure("Folded protein", figsize = (x_max - x_min, y_max - y_min))

    # Draw the protein
    plt.plot(protein_x, protein_y, '-', color = "black")

    for i, color in enumerate(L_color):
        plt.plot(protein_x[i], protein_y[i], 'o', color = color, markersize = 14, markeredgecolor = "black")

    # Set the ticks and limits for each axis
    plt.xticks(range(x_min, x_max + 1))
    plt.xlim([x_min, x_max])

    plt.yticks(range(y_min, y_max + 1))
    plt.ylim([y_min, y_max])

    # Set the title
    plt.title(f"{protein_string}\nEnergy: {protein_energy}")

    plt.grid(axis = "both")

    # Create the legend
    legend_elements = [Line2D([0], [0], marker='o', color='black', label='Hydrophobic', markerfacecolor='r'),
                        Line2D([0], [0], marker='o', color='black', label='Polar', markerfacecolor='b')]
    if "C" in protein_string:
        legend_elements.append(Line2D([0], [0], marker='o', color='black', label='Cysteine', markerfacecolor='y'))
    plt.legend(handles=legend_elements, loc = "upper left")

    '''
    Figure n.2: Matrix view
    This figure shows the protein within the whole matrix
    '''

    # Create lists to hold the matrix' x and y values
    matrix_x = []
    matrix_y = []

    # Fill lists
    for corner in matrix:
        matrix_x.append(corner[0])
        matrix_y.append(corner[1])

    # Determine the minimum and maximum of x and y
    matrix_min = min(matrix_x)
    matrix_max = max(matrix_x)

    plt.figure("Matrix view", figsize = (6,6))

    # Draw the protein
    plt.plot(protein_x, protein_y, '-', color = "black")
    plt.plot(matrix_x, matrix_y, '--', color = "black", linewidth = 7)

    for i, color in enumerate(L_color):
        plt.plot(protein_x[i], protein_y[i], 'o', color = color, markersize = 14, markeredgecolor = "black")

    # Set the ticks and limits
    plt.xticks(range(matrix_min, matrix_max + 1))
    plt.xlim([matrix_min, matrix_max])

    plt.yticks(range(matrix_min, matrix_max + 1))
    plt.ylim([matrix_min, matrix_max])

    # Set the title
    plt.title(f"{protein_string}\nEnergy: {protein_energy}")

    plt.grid(axis = "both")

    # Create the legend
    legend_elements = [Line2D([0], [0], marker='o', color='black', label='Hydrophobic', markerfacecolor='r'),
                        Line2D([0], [0], marker='o', color='black', label='Polar', markerfacecolor='b')]
    if "C" in protein_string:
        legend_elements.append(Line2D([0], [0], marker='o', color='black', label='Cysteine', markerfacecolor='y'))
    plt.legend(handles=legend_elements, loc = "upper left")


def dictionary_hist(dictionary):
    '''

    '''

    print(dictionary.keys())
    print(list(dictionary.keys()))

    plt.bar(x = list(dictionary.keys()), height = dictionary.values(), width = 0.8)


if __name__ == "__main__":
    '''
    protein als txt file opslaan en hier parsen en plotten?
    '''
    test_protein = [["H",0,0], ["P",0,1], ["P",1,1], ["H",2,1], ["H",2,0], ["C",2,-1], ["H",1,-1], ["P",0, -1], ["H",-1,-1]]
    visualise(test_protein)
    plt.show()
