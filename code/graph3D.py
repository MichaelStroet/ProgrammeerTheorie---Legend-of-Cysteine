from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def visualise3D(protein, matrix, protein_string, protein_energy):

    print(protein)
    print(matrix)
    print(protein_string)
    print(protein_energy)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = {
        "H" : "red",
        "P" : "blue",
        "C" : "yellow",
    }

    L_color = []
    L_label = []

    protein_x = []
    protein_y = []
    protein_z = [5] * len(protein_string)

    for acid in protein:
        L_color.append(colors[acid[0]])
        protein_x.append(acid[1])
        protein_y.append(acid[2])

    print(L_color)
    print(protein_x)
    print(protein_y)
    print(protein_z)

    ax.scatter(protein_x, protein_y, protein_z, c=L_color, marker='o')
    ax.plot(protein_x, protein_y, protein_z, c='black', marker='o')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    plt.title( '3D protein\n {}\n Energy: {}\n'.format(protein_string, protein_energy))

    plt.show()
