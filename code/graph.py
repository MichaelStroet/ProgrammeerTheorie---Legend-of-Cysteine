# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import matplotlib.pyplot as plt


def visualise(protein):

    colors = {
        "H" : "red",
        "P" : "blue",
        "C" : "yellow",
    }

    L_color = []
    L_label = []

    L_x = []
    L_y = []

    for acid in protein:
        L_color.append(colors[acid[0]])
        L_x.append(acid[1])
        L_y.append(acid[2])

    max_distance = max([max(L_x), max(L_y)]) + 1

    plt.figure("Folded protein", figsize = (6, 6))

    plt.plot(L_x, L_y, '-', color = "black")

    for i, color in enumerate(L_color):
        plt.plot(L_x[i], L_y[i], 'o', color = color, markersize = 10)

    plt.xlim([-max_distance, max_distance])
    plt.ylim([-max_distance, max_distance])

    plt.grid(axis = "both")
    plt.legend(loc = "upper right")

    plt.show()


if __name__ == "__main__":
    '''
    protein als txt file opslaan en hier parsen en plotten?
    '''
    test_protein = [["H",0,0], ["P",0,1], ["P",1,1], ["H",2,1], ["H",2,0], ["C",2,-1], ["H",1,-1], ["P",0, -1], ["H",-1,-1]]
    visualise(test_protein)
