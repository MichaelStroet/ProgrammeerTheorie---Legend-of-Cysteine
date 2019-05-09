# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import matplotlib.pyplot as plt

from dict_average import dict_average

def plot_matrix_sizes(matrix_sizes, used_size):

        smallest_matrix_sizes = {}
        average_matrix_sizes = {}
        largest_matrix_sizes = {}

        for energy, sizes in matrix_sizes.items():
            smallest_matrix_sizes[energy] = min(sizes.keys())
            average_matrix_sizes[energy] = dict_average(sizes)
            largest_matrix_sizes[energy] = max(sizes.keys())

        sorted_smallest_sizes = sorted(smallest_matrix_sizes.items())
        sorted_average_sizes = sorted(average_matrix_sizes.items())
        sorted_largest_sizes = sorted(largest_matrix_sizes.items())

        sorted_energy = []
        sorted_smallest = []
        sorted_average = []
        sorted_largest = []

        for i in range(len(matrix_sizes)):
            sorted_energy.append(sorted_smallest_sizes[i][0])

            sorted_smallest.append(sorted_smallest_sizes[i][1])
            sorted_average.append(sorted_average_sizes[i][1])
            sorted_largest.append(sorted_largest_sizes[i][1])

        x_min = min(sorted_energy)
        x_max = 0

        y_min = 0
        y_max = used_size + 1


        plt.figure("Matrix sizes per energy", figsize = (6, 6))

        line_width = 2
        plt.hlines(used_size, x_min, x_max, linewidth = line_width, linestyles = "dashed", color = "black", label = "Matrix used")
        plt.hlines(2 * used_size / 3., x_min, x_max, linewidth = 2 * line_width / 3., linestyles = "dashed", color = "black")
        plt.hlines(used_size / 3., x_min, x_max, linewidth = line_width / 3., linestyles = "dashed", color = "black")

        plt.plot(sorted_energy, sorted_largest, '-', color = "red", label = "Largest")
        plt.plot(sorted_energy, sorted_average, '-', color = "blue", label = "Average")
        plt.plot(sorted_energy, sorted_smallest, '-', color = "red", label = "Smallest")


        plt.xlabel("Energy")
        plt.xlim([x_min, x_max])

        plt.ylabel("Matrix size")
        plt.ylim([y_min, y_max])

        plt.title("Minimal matrix sizes per energy")

        plt.gca().invert_xaxis()

        plt.grid(axis = "both")

        plt.legend(loc = "upper right", bbox_to_anchor = (1, 1 - (1. / y_max)))
