# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def plot2D(acid_data, protein_string, protein_energy):
    '''
    Draws a plot of a folded protein in 2D
    '''
    # Assign each amino acid a color
    colors = {
        "H" : "red",
        "P" : "blue",
        "C" : "yellow"
    }

    # Create lists to contain the color and coordinates of each amino acid
    L_color = []
    protein_x = []
    protein_y = []

    # Fill the lists for each amino acid
    for acid in acid_data:
        L_color.append(colors[acid[0]])
        protein_x.append(acid[1])
        protein_y.append(acid[2])

    # Determine the minimum and maximum values of x and y
    x_min = min(protein_x) - 1
    x_max = max(protein_x) + 1
    y_min = min(protein_y) - 1
    y_max = max(protein_y) + 1

    # Define the figure for the 2D protein
    plt.figure("2D folded protein", figsize = (x_max - x_min, y_max - y_min))

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
