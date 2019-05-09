# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import matplotlib.pyplot as plt

from dict_average import dict_average

def plot_matrix_sizes(matrix_sizes):

        average_matrix_sizes = {}

        for energy, sizes in matrix_sizes.items():
            average_matrix_sizes[energy] = dict_average(sizes)

        sorted_sizes = sorted(average_matrix_sizes.items(), reverse = True)

        sorted_energies = []
        sorted_averages = []
        for i in range(len(sorted_sizes)):
            sorted_energies.append(sorted_sizes[i][0])
            sorted_averages.append(sorted_sizes[i][1])

        plt.figure("Matrix sizes per energy", figsize = (6, 6))

        plt.plot(sorted_energies, sorted_averages, '-')

        plt.gca().invert_xaxis()

        plt.xlabel("Energy")
        plt.ylabel("Matrix size")

        plt.title("Average minimal matrix sizes")

        plt.grid(axis = "both")
