# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def plot3D(acid_data, protein_string, protein_energy):
    '''
    Draws a plot of a folded protein in 3D
    '''
    # Define the figure for the 3D protein
    fig = plt.figure("3D folded protein")
    ax = fig.add_subplot(111, projection='3d')

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
    protein_z = []

    # Fill the lists for each amino acid
    for acid in acid_data:
        L_color.append(colors[acid[0]])
        protein_x.append(acid[1])
        protein_y.append(acid[2])
        protein_z.append(acid[3])

    # Draw the protein
    ax.scatter(protein_x, protein_y, protein_z, c=L_color, marker='o', s =70, depthshade=False)
    ax.plot(protein_x, protein_y, protein_z, c='black', marker='o', markersize=11)

    # Label axes
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    # Set the title
    plt.title( '3D protein\n {}\n Energy: {}\n'.format(protein_string, protein_energy))

    # Create the legend
    legend_elements = [Line2D([0], [0], marker='o', markersize=8, color='black', label='Hydrophobic', markerfacecolor='r'),
                        Line2D([0], [0], marker='o', markersize=8, color='black', label='Polar', markerfacecolor='b')]
    if "C" in protein_string:
        legend_elements.append(Line2D([0], [0], marker='o', markersize=8, color='black', label='Cysteine', markerfacecolor='y'))
    ax.legend(handles=legend_elements, loc = "upper left")

    # Determine the minimum and maximum values of x, y and z
    x_min = min(protein_x) - 1
    x_max = max(protein_x) + 1
    y_min = min(protein_y) - 1
    y_max = max(protein_y) + 1
    z_min = min(protein_z) - 1
    z_max = max(protein_z) + 1

    # Set the ticks and limits for each axis
    plt.xticks(range(x_min, x_max + 1))
    plt.xlim([x_min, x_max])

    plt.yticks(range(y_min, y_max + 1))
    plt.ylim([y_min, y_max])

    ax.set_zticks(range(z_min, z_max + 1))
    ax.set_zlim([z_min, z_max])
