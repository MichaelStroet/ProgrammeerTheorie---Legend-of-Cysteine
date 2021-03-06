# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def plot1D(protein_string):
    '''
    Draws a plot of a 'folded' protein in 1D
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
    protein_y = [0] * len(protein_string)

    # Fill the lists for each amino acid
    for i, acid in enumerate(protein_string):
        L_color.append(colors[acid])
        protein_x.append(i)

    # Determine the minimum and maximum values of x and y
    x_min = min(protein_x) - 1
    x_max = max(protein_x) + 1
    y_min = -0.5
    y_max = 0.5
    # Define the figure for the 1D line
    plt.figure("Line protein", figsize = (10,4))

    # Draw the acid connections
    plt.plot(protein_x, protein_y, '-', color = "black")

    # Draw the acids
    for i, color in enumerate(L_color):
        plt.plot(protein_x[i], protein_y[i], 'o', color = color, markersize = 14, markeredgecolor = "black")

    # Set the ticks and limits for each axis
    plt.xticks(range(x_min, x_max + 1))
    plt.xlim([x_min, x_max])

    plt.yticks([])
    plt.ylim([y_min, y_max])

    # Set the title
    plt.title(f"{protein_string}\nEnergy: unexpectedly 0")

    # Create the legend
    legend_elements = [Line2D([0], [0], marker='o', color='black', label='Hydrophobic', markerfacecolor='r'),
                        Line2D([0], [0], marker='o', color='black', label='Polar', markerfacecolor='b')]
    if "C" in protein_string:
        legend_elements.append(Line2D([0], [0], marker='o', color='black', label='Cysteine', markerfacecolor='y'))
    plt.legend(handles=legend_elements, loc = "upper left")
