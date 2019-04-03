# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import matplotlib.pyplot as plt


def draw_graph(protein):

    L_x = []
    L_y = []

    for acid in protein:
        L_x.append(acid[0])
        L_y.append(acid[1])

    max_distance = max([max(L_x), max(L_y)]) + 1

    plt.figure("Folded protein", figsize = (6, 6))

    plt.plot(L_x, L_y, 'b-')
    plt.plot(L_x, L_y, 'bo')

    plt.xlim([-max_distance, max_distance])
    plt.ylim([-max_distance, max_distance])

    plt.grid(axis = "both")

    plt.show()


if __name__ == "__main__":
    test_protein = [[0,0], [0,1], [1,1], [2,1], [2,0], [2,-1], [1,-1], [0, -1], [-1,-1]]
    draw_graph(test_protein)
