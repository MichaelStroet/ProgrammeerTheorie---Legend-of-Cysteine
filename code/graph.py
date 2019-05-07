# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D



def visualise(protein, matrix, protein_string, protein_energy):
    '''

    '''
    print(matrix)
    colors = {
        "H" : "red",
        "P" : "blue",
        "C" : "yellow",
    }

    L_color = []
    #L_label = []

    protein_x = []
    protein_y = []

    for acid in protein:
        L_color.append(colors[acid[0]])
        protein_x.append(acid[1])
        protein_y.append(acid[2])

    x_min = min(protein_x) - 1
    x_max = max(protein_x) + 1
    y_min = min(protein_y) - 1
    y_max = max(protein_y) + 1

    plt.figure("Folded protein", figsize = (x_max - x_min, y_max - y_min))

    plt.plot(protein_x, protein_y, '-', color = "black")

    for i, color in enumerate(L_color):
        plt.plot(protein_x[i], protein_y[i], 'o', color = color, markersize = 14, markeredgecolor = "black")

    plt.xticks(range(x_min, x_max + 1))
    plt.xlim([x_min, x_max])

    plt.yticks(range(y_min, y_max + 1))
    plt.ylim([y_min, y_max])

    plt.title(f"{protein_string}\nEnergy: {protein_energy}")

    plt.grid(axis = "both")
    #plt.legend(loc = "upper right")
    legend_elements = [Line2D([0], [0], marker='o', color='black', label='Hydrophobic', markerfacecolor='r'),
                        Line2D([0], [0], marker='o', color='black', label='Polar', markerfacecolor='b')]
    if "C" in protein_string:
        legend_elements.append(Line2D([0], [0], marker='o', color='black', label='Cysteine', markerfacecolor='y'))

    plt.legend(handles=legend_elements, loc = "upper left")


    matrix_x = []
    matrix_y = []

    for corner in matrix:
        matrix_x.append(corner[0])
        matrix_y.append(corner[1])

    matrix_min = min(matrix_x)
    matrix_max = max(matrix_x)

    plt.figure("matrix view", figsize = (6,6))

    plt.plot(protein_x, protein_y, '-', color = "black")
    plt.plot(matrix_x, matrix_y, '--', color = "black", linewidth = 7)

    for i, color in enumerate(L_color):
        plt.plot(protein_x[i], protein_y[i], 'o', color = color, markersize = 14, markeredgecolor = "black")

    plt.xticks(range(matrix_min, matrix_max + 1))
    plt.xlim([matrix_min, matrix_max])

    plt.yticks(range(matrix_min, matrix_max + 1))
    plt.ylim([matrix_min, matrix_max])

    plt.title(f"{protein_string}\nEnergy: {protein_energy}")

    plt.grid(axis = "both")
    #plt.legend(loc = "upper right")

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
