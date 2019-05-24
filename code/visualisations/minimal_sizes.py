# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

from dict_average import dict_average
import matplotlib.pyplot as plt

def plot_matrix_sizes(matrix_sizes, used_size):
        '''
        Draws a plot of the matrix size range per energy
        '''
        # Dictionaries for the range of matrix sizes per energy
        smallest_matrix_sizes = {}
        average_matrix_sizes = {}
        largest_matrix_sizes = {}

        # Determine the smallest, largest and average matrix size per energy
        # and add them to the dictionaries at that energy
        for energy, sizes in matrix_sizes.items():
            smallest_matrix_sizes[energy] = min(sizes.keys())
            average_matrix_sizes[energy] = dict_average(sizes)
            largest_matrix_sizes[energy] = max(sizes.keys())

        # Create a list of the energies sorted by their value
        sorted_energies = [energy for energy in sorted(smallest_matrix_sizes.keys())]

        # Turn all dictionaries into lists of their matrix sizes sorted by energy
        sorted_smallest = [value for energy,value in sorted(smallest_matrix_sizes.items())]
        sorted_average = [value for energy,value in sorted(average_matrix_sizes.items())]
        sorted_largest = [value for energy,value in sorted(largest_matrix_sizes.items())]

        # Minimum and maximum values for the axes
        x_min = min(sorted_energies)
        x_max = 0
        y_min = 0
        y_max = used_size + 1

        # Define the matrix sizes figure
        plt.figure("Matrix sizes per energy", figsize = (6, 6))

        # Plot a horizontal line for the used matrix size
        plt.hlines(used_size, x_min, x_max, linewidth = 2, linestyles = "dashed", color = "black", label = "Matrix used")

        # Plot the range of matrix sizes for each energy
        plt.plot(sorted_energies, sorted_largest, '-', color = "red", label = "Largest")
        plt.plot(sorted_energies, sorted_average, '-', color = "blue", label = "Average")
        plt.plot(sorted_energies, sorted_smallest, '-', color = "red", label = "Smallest")

        # Define the x-axis properties
        plt.xlabel("Energy")
        plt.xticks(range(x_min, x_max + 1, 1))
        plt.xlim([x_min, x_max])

        # Define the y-axis properties
        plt.ylabel("Matrix size")
        plt.yticks(range(1, y_max, 2))
        plt.ylim([y_min, y_max])

        plt.title("Minimal matrix sizes per energy")

        plt.gca().invert_xaxis()
        plt.grid(axis = "both")
        plt.legend(loc = "lower left")
