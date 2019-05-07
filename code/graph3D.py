from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D



def visualise3D(protein, matrix, protein_string, protein_energy):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    print(protein)

    colors = {
        "H" : "red",
        "P" : "blue",
        "C" : "yellow",
    }

    L_color = []

    protein_x = []
    protein_y = []
    protein_z = []

    for acid in protein:
        L_color.append(colors[acid[0]])
        protein_x.append(acid[1])
        protein_y.append(acid[2])
        protein_z.append(acid[3])


    ax.scatter(protein_x, protein_y, protein_z, c=L_color, marker='o')
    ax.plot(protein_x, protein_y, protein_z, c='black', marker='o')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    plt.title( '3D protein\n {}\n Energy: {}\n'.format(protein_string, protein_energy))


    legend_elements = [Line2D([0], [0], marker='o', color='black', label='Hydrophobic', markerfacecolor='r'),
                        Line2D([0], [0], marker='o', color='black', label='Polar', markerfacecolor='b')]
    if "C" in protein_string:
        legend_elements.append(Line2D([0], [0], marker='o', color='black', label='Cysteine', markerfacecolor='y'))

    ax.legend(handles=legend_elements, loc = "upper left")


    x_min = min(protein_x) - 1
    x_max = max(protein_x) + 1
    y_min = min(protein_y) - 1
    y_max = max(protein_y) + 1
    z_min = min(protein_z) - 1
    z_max = max(protein_z) + 1

    plt.xticks(range(x_min, x_max + 1))
    plt.xlim([x_min, x_max])

    plt.yticks(range(y_min, y_max + 1))
    plt.ylim([y_min, y_max])

    #ax.zticks(range(z_min, z_max + 1))
    ax.set_zlim([z_min, z_max])

    #ax.set_zlim(-2, 2)

    plt.show()
