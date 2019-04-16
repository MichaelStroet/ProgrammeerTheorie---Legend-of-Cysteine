# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np
import copy

from datastructure import Protein, Acid
'''
09/04
ಠ_ಠ
16/04
 new version
'''


def branch_n_bound(protein_string):
    global protein_str, length_total, prob_below_average, prob_above_average
    protein_str = protein_string
    length_total = len(protein_string)

    #create protein matrix
    protein = Protein(length_total)
    print(protein)

    energy_min_all = 0
    energy_min_partial = [0] * length_total
    average_list = [[] for i in range(length_total)]

    #set probabilities for pruning
    prob_below_average = 0.8
    prob_above_average = 0.5

    #place first & second amino acid underneath [row, column]
    start_location = [length_total - 1, length_total - 1]
    protein.add_acid(protein_string[0], start_location,"")
    previous_location = start_location
    location = [previous_location[0] + 1, previous_location[1]]
    protein.add_acid(protein_string[1], location, "down")
    previous_location = location

    print(protein)

    new_protein = copy.deepcopy(protein)

    #call searching function
    searching(new_protein, energy_min_all, energy_min_partial, average_list, previous_location)

def searching(protein, energy_min_all, energy_min_partial, average_list, previous_location):

        print("length:",protein.length)

        #see possible_sites for monomer k (see whether matrix box left, up & right are empty, if so store adresses in list)

        locations = protein.neighbors(previous_location)
        print("loc: ",locations)
        possible_sites = {}

        for direction in locations:
            location = locations[direction]
            acid = protein.acids[location[0],location[1]]
            print(acid)

            if acid == 0:
                possible_sites[direction] = location


        print("possible sites are",possible_sites)

        if len(possible_sites) > 0:

            #calculate energy of current partial protein for each site (when pseudo placing)
            for key_direction in possible_sites:

                new_protein = copy.deepcopy(protein)
                amino_acid = protein_str[new_protein.length]

                print("amino: ",amino_acid)
                print("direction: ",key_direction)

                previous_acid = new_protein.acids[previous_location[0], previous_location[1]]
                print("previous: ",previous_acid, " loc:", previous_location)
                previous_acid.add_connection(key_direction)

                location = possible_sites[key_direction]


                new_protein.add_acid(amino_acid, location, key_direction)

                print("possible location: ",location)

                # Add the acid object to the protein and connect it to the previous acid

                new_energy = new_protein.check_energy(location, amino_acid)
                new_protein.energy += new_energy
                print("energy:",new_energy)

                #update list for average energy & calculate average
                print(new_protein.length)
                average_list[new_protein.length - 1].append(new_protein.energy)
                energy_average_partial = np.average(average_list[new_protein.length - 1])
                print(average_list, energy_average_partial)

                #place the monomer and update the energy

                #if it is the last monomer
                if new_protein.length == length_total:
                    print("last\n",new_protein)

                    #previous_location = location

                    #update lowest energy among all completed proteins
                    if new_protein.energy < energy_min_all:
                        energy_min_all = new_protein.energy

                #if it is a polar monomer
                elif amino_acid == "P":
                    print("p")
                    print("placed at: ",location)
                    print(new_protein)

                    print(previous_location)
                    searching(new_protein, energy_min_all, energy_min_partial, average_list, location)

                #if it is a hydrophobic monomer
                else:

                    #if the curent energy is equal to or below the lowest energy of the partial protein
                    if new_protein.energy <= energy_min_partial[new_protein.length - 1]:
                        energy_min_partial[new_protein.length - 1] = new_protein.energy
                        print("min partial: ",energy_min_partial)
                        print("h\n",new_protein)

                        #previous_location = location
                        searching(new_protein, energy_min_all, energy_min_partial, average_list, location)

                    #if the curent energy is equal to or below the average energy of all partial proteins
                    elif new_protein.energy <= energy_average_partial:
                        r = np.random.random()

                        if r > prob_below_average:
                            print("h\n",new_protein)

                            #previous_location = location
                            searching(new_protein, energy_min_all, energy_min_partial, average_list, location)

                    #if the curent energy is bigger than the average energy of all partial proteins
                    else:
                        r = np.random.random()
                        if r > prob_above_average:
                            print("h\n",new_protein)

                            #previous_location = location
                            searching(new_protein, energy_min_all, energy_min_partial, average_list, location)

        else:
            print("no locations")

        print(energy_min_partial)


if __name__ == "__main__":
    branch_n_bound("HHPHHHPH")



'''
Pseudo-code Branch & Bound algorithm

--------------------------------------------------------------------------------

Mao Chen, Wen-Qi Huang,
A Branch and Bound Algorithm for the Protein Folding Problem in the HP Lattice Model,
Genomics, Proteomics & Bioinformatics,
Volume 3, Issue 4,
2005,
Pages 225-230

--------------------------------------------------------------------------------

Energy of the protein E = - Sum(i, n, 1) Sum(j, i-1, 1) (sigma_i sigma_j)
    where sigma = 1 if monomer is hydrophobic (H)

We want to know the lowest energy state and configuration
    => Minimalise E / Maximise unconnected H-H neighbors

Variables:
    k     : Length of the partial protein
    Mk    : Total possible sites (or nodes) at length k
    E_k   : Energy of the current partial protein of length k
    E_min : Lowest energy among all completed proteins (length k = n)
    U_k   : Lowest energy of partial protein of length k
    Z_k   : Average energy of all partial proteins of length k
    p_1   : Threshold value for pruning nodes where E_k > Z_k
    p_2   : Threshold value for pruning nodes where U_k < E_k <= Z_k


Initial values variables:
    k     : 3
    Mk    : not initialised
    E_k   : 0
    E_min : 0
    U_k   : 0
    Z_k   : 0
    p_1   : Predetermined constant (0.8)
    p_2   : Predetermined constant (0.5)

Pseudo-code:
    Place first two monomers                                                    # Position monomers k = 1 & 2 not important
    k_0 = 3

    Call the recursive function Searching(E_k, k)

    ------------------------

    Searching(E_k-1, k)

        Compute M_k

        if not M_k == 0:                                                        # Protein is not yet finished, k < n

            for each site a in M_k:

                Compute new E_k for monomer k at a

                if k == n:                                                      # Protein is now finished, k == n
                    place monomer k at a

                    if E_k < E_min:                                             # New lowest energy configuration found
                        E_min = E_k

                        ¿Een datastructuur voor visualisatie opslaan hier?
                        (niet noodzakelijk dezelfde als in graph.py)

                elif monomer k == P:                                            # next monomer is Polar
                    place monomer k at a
                    Call Searching(E_k, k+1)

                else:                                                           # next monomer is Hydrophobic

                    if E_k <= U_k:                                              # New energy is lower than the lowest energy yet, very promising!
                        place monomer k at a
                        Call Searching(E_k, k+1)

                    elif E_k <= Z_k:                                            # New energy is between the lowest and average energies, less promising
                        draw uniformly random number r in range [0,1]

                        if r > p_2:
                            place monomer k at a
                            Call Searching(E_k, k+1)

                    else:                                                       # New energy is higher than the average energie, not promising
                        draw uniformly random number r in range [0,1]

                        if r > p_1:
                            place monomer k at a
                            Call Searching(E_k, k+1)

--------------------------------------------------------------------------------

Stuff missing in pseudo-code: (Heb ik iets gemist?)
    Update U_k and Z_k
    ...


'''
